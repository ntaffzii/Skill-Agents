#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Core skill-sync engine and CLI for Skill-Agents (stdlib only)."""

from __future__ import annotations

import argparse
import io
import os
import re
import shutil
import ssl
import sys
import tempfile
import urllib.error
import urllib.request
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

DEFAULT_GITHUB_REPO = "ntaffzii/Skill-Agents"
DEFAULT_GITHUB_BRANCH = "main"
IGNORED_NAMES = frozenset(
    {"__pycache__", ".DS_Store", "Thumbs.db", "graphify-out", ".git"}
)
IGNORED_SUFFIXES = (".pyc", ".pyo")
IGNORE_PATTERNS = shutil.ignore_patterns(
    "__pycache__",
    "*.pyc",
    "*.pyo",
    ".DS_Store",
    "Thumbs.db",
    "graphify-out",
    ".git",
)
REMOTE_ALLOWED_PREFIXES = ("skills/", ".agents/")
REMOTE_ALLOWED_FILES = {"AGENTS.md"}


@dataclass(frozen=True)
class ProviderSpec:
    key: str
    slug: str
    name: str
    short_name: str
    root_rel: tuple[str, ...]
    skills_rel: tuple[str, ...]

    def root_dir(self, home_dir: Path | None = None) -> Path:
        base = home_dir or get_home_dir()
        return base.joinpath(*self.root_rel)

    def skills_dir(self, home_dir: Path | None = None) -> Path:
        base = home_dir or get_home_dir()
        return base.joinpath(*self.skills_rel)


PROVIDERS: tuple[ProviderSpec, ...] = (
    ProviderSpec("1", "antigravity", "Antigravity IDE", "Antigravity", (".gemini",), (".gemini", "config", "skills")),
    ProviderSpec("2", "claude", "Claude Code", "Claude", (".claude",), (".claude", "skills")),
    ProviderSpec("3", "opencode", "OpenCode Interpreter", "OpenCode", (".opencode",), (".opencode", "skills")),
    ProviderSpec("4", "qwen", "Qwen Code", "Qwen", (".qwen",), (".qwen", "skills")),
    ProviderSpec("5", "zcode", "ZCode", "ZCode", (".zcode",), (".zcode", "skills")),
    ProviderSpec("6", "codex", "Codex CLI", "Codex", (".codex",), (".codex", "skills")),
    ProviderSpec("7", "lmstudio", "LM Studio", "LM Studio", (".lmstudio",), (".lmstudio", "skills")),
)

PROVIDERS_BY_KEY: dict[str, ProviderSpec] = {p.key: p for p in PROVIDERS}

PROVIDER_ALIASES: dict[str, str] = {
    "antigravity": "1",
    "gemini": "1",
    "claude": "2",
    "opencode": "3",
    "qwen": "4",
    "zcode": "5",
    "codex": "6",
    "lmstudio": "7",
    "all": "all",
}
for _p in PROVIDERS:
    PROVIDER_ALIASES[_p.key] = _p.key


@dataclass(frozen=True)
class SubSkillInfo:
    name: str
    path: Path
    description: str
    markdown_body: str
    files: tuple[str, ...]


@dataclass(frozen=True)
class SkillInfo:
    name: str
    path: Path
    description: str
    markdown_body: str
    subskills: tuple[str, ...]
    subskill_details: tuple[SubSkillInfo, ...]
    files: tuple[str, ...]
    preview_text: str


@dataclass(frozen=True)
class SyncRecord:
    item: str
    provider: str
    action: str  # installed | updated | dry-run | skipped | failed
    dest_path: str
    message: str = ""


@dataclass
class SyncResult:
    synced: list[str] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)
    failed: list[str] = field(default_factory=list)
    touched_dirs: list[Path] = field(default_factory=list)
    records: list[SyncRecord] = field(default_factory=list)


LogCallback = Callable[[str], None]


def get_home_dir() -> Path:
    """Resolve user home dynamically so tests and cross-platform callers stay isolated."""
    if os.name == "nt":
        userprofile = os.environ.get("USERPROFILE")
        if userprofile:
            return Path(userprofile)
    home_env = os.environ.get("HOME")
    if home_env:
        return Path(home_env)
    return Path.home()


def find_local_repo_root() -> Path | None:
    """Return local Skill-Agents repository root if running inside one, else None."""
    candidates: list[Path] = []
    if not getattr(sys, "frozen", False):
        candidates.append(Path(__file__).resolve().parent.parent)
    candidates.append(Path.cwd())

    for candidate in candidates:
        if (candidate / "skills").is_dir() and (candidate / "AGENTS.md").is_file():
            return candidate
    return None


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    """Extract simple YAML frontmatter key/value pairs and return (meta, body)."""
    match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n?", text, flags=re.DOTALL)
    if not match:
        return {}, text

    raw_yaml = match.group(1)
    body = text[match.end() :]
    meta: dict[str, str] = {}
    for line in raw_yaml.splitlines():
        if ":" not in line or line.startswith((" ", "\t", "-")):
            continue
        key, val = line.split(":", 1)
        meta[key.strip()] = val.strip().strip('"').strip("'")
    return meta, body


def _list_clean_files(folder: Path) -> tuple[str, ...]:
    """Return sorted relative posix paths of non-junk files under folder."""
    files: list[str] = []
    for root, dirs, filenames in os.walk(folder):
        dirs[:] = sorted(d for d in dirs if d not in IGNORED_NAMES)
        root_path = Path(root)
        for fname in sorted(filenames):
            if fname in IGNORED_NAMES or fname.endswith(IGNORED_SUFFIXES):
                continue
            rel = (root_path / fname).relative_to(folder).as_posix()
            files.append(rel)
    return tuple(files)


def _read_skill_markdown(folder: Path) -> tuple[str, str, str]:
    """Read SKILL.md from folder and return (description, markdown_body, raw_text)."""
    skill_md = folder / "SKILL.md"
    if not skill_md.is_file():
        return "", "", ""
    raw_text = skill_md.read_text(encoding="utf-8", errors="replace")
    meta, body = parse_frontmatter(raw_text)
    return meta.get("description", ""), body.strip(), raw_text


def discover_skills(source_root: Path) -> list[SkillInfo]:
    """Discover top-level skill directories and nested sub-skills under <source_root>/skills."""
    skills_dir = source_root / "skills"
    if not skills_dir.is_dir():
        return []

    results: list[SkillInfo] = []
    for entry in sorted(skills_dir.iterdir(), key=lambda p: p.name.lower()):
        if not entry.is_dir() or entry.name.startswith("."):
            continue

        description, body, raw_text = _read_skill_markdown(entry)

        subskill_details: list[SubSkillInfo] = []
        sub_md_files = sorted(
            (sub for sub in entry.rglob("SKILL.md") if sub.parent != entry),
            key=lambda p: p.parent.name.lower(),
        )
        for sub_md in sub_md_files:
            sub_dir = sub_md.parent
            sub_desc, sub_body, sub_raw = _read_skill_markdown(sub_dir)
            sub_files = _list_clean_files(sub_dir)
            subskill_details.append(
                SubSkillInfo(
                    name=sub_dir.name,
                    path=sub_dir,
                    description=sub_desc or f"Sub-skill ภายใต้ {entry.name}",
                    markdown_body=sub_body or sub_raw or f"# {sub_dir.name}",
                    files=sub_files,
                )
            )

        sub_names = tuple(s.name for s in subskill_details)
        if not description and sub_names:
            description = f"หมวดหมู่รวม {len(sub_names)} sub-skills: {', '.join(sub_names[:4])}" + (
                " ..." if len(sub_names) > 4 else ""
            )

        if not body and subskill_details:
            lines = [f"# {entry.name}", "", f"หมวดหมู่นี้ประกอบด้วย **{len(subskill_details)} sub-skills**:", ""]
            for sub in subskill_details:
                lines.append(f"- **{sub.name}** — {sub.description}")
            body = "\n".join(lines)

        preview_text = raw_text or body or f"# {entry.name}\n\n(ไม่พบไฟล์ SKILL.md)"
        results.append(
            SkillInfo(
                name=entry.name,
                path=entry,
                description=description or "ไม่มีคำอธิบายใน SKILL.md",
                markdown_body=body or preview_text,
                subskills=sub_names,
                subskill_details=tuple(subskill_details),
                files=_list_clean_files(entry),
                preview_text=preview_text,
            )
        )
    return results


def detect_providers(home_dir: Path | None = None) -> dict[str, bool]:
    """Return mapping of provider key -> whether its root directory exists on disk."""
    home = home_dir or get_home_dir()
    return {p.key: p.root_dir(home).exists() for p in PROVIDERS}


def inspect_installed_skills(
    skill_names: list[str],
    home_dir: Path | None = None,
) -> dict[str, dict[str, bool]]:
    """Return {skill_name: {provider_key: is_installed}} for the current machine."""
    home = home_dir or get_home_dir()
    provider_dirs = {p.key: p.skills_dir(home) for p in PROVIDERS}
    matrix: dict[str, dict[str, bool]] = {}
    for skill_name in skill_names:
        matrix[skill_name] = {
            key: (base_dir / skill_name).is_dir()
            for key, base_dir in provider_dirs.items()
        }
    return matrix


def parse_provider_selection(raw: str | None) -> list[str]:
    """Parse comma-separated provider names/numbers or 'all' into canonical keys."""
    if not raw or not raw.strip():
        return [p.key for p in PROVIDERS]

    tokens = [tok.strip().lower() for tok in raw.split(",") if tok.strip()]
    if not tokens or "all" in tokens or "a" in tokens:
        return [p.key for p in PROVIDERS]

    keys: list[str] = []
    for tok in tokens:
        if tok not in PROVIDER_ALIASES:
            valid = ", ".join(sorted(k for k in PROVIDER_ALIASES if not k.isdigit()))
            raise ValueError(f"ไม่รู้จัก provider '{tok}' (รองรับ: {valid})")
        canonical = PROVIDER_ALIASES[tok]
        if canonical == "all":
            return [p.key for p in PROVIDERS]
        if canonical not in keys:
            keys.append(canonical)
    return keys


def _build_ssl_context() -> ssl.SSLContext:
    """Create an SSL context that works in both normal Python and frozen PyInstaller apps."""
    ctx = ssl.create_default_context()
    try:
        import certifi  # type: ignore

        ca_path = certifi.where()
        if ca_path and Path(ca_path).is_file():
            ctx.load_verify_locations(cafile=ca_path)
    except Exception:
        pass
    if os.name == "nt":
        try:
            ctx.load_default_certs(ssl.Purpose.SERVER_AUTH)
        except Exception:
            pass
    return ctx


def fetch_repo_from_github(
    repo: str = DEFAULT_GITHUB_REPO,
    branch: str = DEFAULT_GITHUB_BRANCH,
    dest_dir: Path | None = None,
    *,
    timeout: int = 45,
    log_cb: LogCallback | None = None,
) -> Path:
    """Download GitHub zip archive and safely extract skills/, .agents/, and AGENTS.md."""
    log = log_cb or (lambda _msg: None)
    url = f"https://github.com/{repo}/archive/refs/heads/{branch}.zip"
    target_root = Path(dest_dir) if dest_dir else Path(tempfile.mkdtemp(prefix="skill-agents-"))
    target_root.mkdir(parents=True, exist_ok=True)
    resolved_root = target_root.resolve()

    log(f"🌐 กำลังดาวน์โหลดจาก {url} ...")
    req = urllib.request.Request(url, headers={"User-Agent": "Skill-Agents-Sync/1.0"})
    ssl_ctx = _build_ssl_context()
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ssl_ctx) as resp:
            data = resp.read()
    except urllib.error.URLError as exc:
        raise RuntimeError(f"ไม่สามารถดาวน์โหลดจาก GitHub ได้: {exc}") from exc

    extracted_files = 0
    with zipfile.ZipFile(io.BytesIO(data)) as zf:
        for member in zf.infolist():
            if member.is_dir():
                continue
            parts = Path(member.filename).parts
            if len(parts) < 2:
                continue
            rel_path = Path(*parts[1:])
            rel_posix = rel_path.as_posix()
            if not (
                rel_posix in REMOTE_ALLOWED_FILES
                or any(rel_posix.startswith(prefix) for prefix in REMOTE_ALLOWED_PREFIXES)
            ):
                continue

            out_path = (resolved_root / rel_path).resolve()
            if resolved_root not in out_path.parents and out_path != resolved_root:
                raise RuntimeError(f"ตรวจพบ path ไม่ปลอดภัยใน zip: {member.filename}")

            out_path.parent.mkdir(parents=True, exist_ok=True)
            with zf.open(member, "r") as src, open(out_path, "wb") as dst:
                shutil.copyfileobj(src, dst)
            extracted_files += 1

    if extracted_files == 0 or not (resolved_root / "skills").is_dir():
        raise RuntimeError("ไม่พบโฟลเดอร์ skills/ ในไฟล์ที่ดาวน์โหลดจาก GitHub")

    log(f"✅ โหลดไฟล์จาก GitHub สำเร็จ ({extracted_files} ไฟล์)")
    return resolved_root


def resolve_skill_paths(source_root: Path, skill_targets: list[str]) -> list[Path]:
    """Resolve list of skill names or filesystem paths into existing skill directories."""
    skills_base = source_root / "skills"
    resolved: list[Path] = []
    for item in skill_targets:
        candidate = Path(item)
        if not candidate.is_dir():
            candidate = skills_base / item
        if not candidate.is_dir():
            raise FileNotFoundError(f"ไม่พบโฟลเดอร์ Skill: {item}")
        resolved.append(candidate)
    return resolved


def sync_skills(
    source_root: Path,
    skill_targets: list[str] | None,
    provider_keys: list[str],
    *,
    home_dir: Path | None = None,
    dry_run: bool = False,
    log_cb: LogCallback | None = None,
) -> SyncResult:
    """Copy selected skill folders to the chosen AI provider global directories."""
    log = log_cb or print
    home = home_dir or get_home_dir()
    result = SyncResult()

    if not skill_targets:
        discovered = discover_skills(source_root)
        skill_paths = [s.path for s in discovered]
    else:
        skill_paths = resolve_skill_paths(source_root, skill_targets)

    if not skill_paths:
        log("❌ ไม่พบโฟลเดอร์ Skill สำหรับซิงค์")
        return result

    for src_path in skill_paths:
        skill_name = src_path.name
        log(f"\n🚀 กำลังซิงค์ Skill: [{skill_name}]" + (" (Dry Run)" if dry_run else ""))
        for key in provider_keys:
            spec = PROVIDERS_BY_KEY.get(key)
            if not spec:
                continue
            target_base = spec.skills_dir(home)
            target_skill_dir = target_base / skill_name
            existed = target_skill_dir.exists()
            try:
                if dry_run:
                    note = "จะอัปเดตของเดิม" if existed else "ติดตั้งใหม่"
                    log(f"  [Dry Run] {spec.name:<22} -> {target_skill_dir} ({note})")
                    result.synced.append(f"{skill_name} -> {spec.name}")
                    result.records.append(
                        SyncRecord(skill_name, spec.name, "dry-run", str(target_skill_dir), note)
                    )
                    continue

                target_base.mkdir(parents=True, exist_ok=True)
                if existed:
                    shutil.rmtree(target_skill_dir)
                shutil.copytree(src_path, target_skill_dir, ignore=IGNORE_PATTERNS)
                action = "updated" if existed else "installed"
                note = "อัปเดตสำเร็จ" if existed else "ติดตั้งใหม่สำเร็จ"
                result.synced.append(f"{skill_name} -> {spec.name}")
                result.records.append(
                    SyncRecord(skill_name, spec.name, action, str(target_skill_dir), note)
                )
                if target_base not in result.touched_dirs:
                    result.touched_dirs.append(target_base)
                log(f"  ✅ [สำเร็จ] {spec.name:<22} -> {target_skill_dir}")
            except Exception as exc:
                result.failed.append(f"{skill_name} -> {spec.name}: {exc}")
                result.records.append(
                    SyncRecord(skill_name, spec.name, "failed", str(target_skill_dir), str(exc))
                )
                log(f"  ❌ [ล้มเหลว] {spec.name:<22} -> {exc}")

    return result


def sync_antigravity_extras(
    source_root: Path,
    *,
    home_dir: Path | None = None,
    dry_run: bool = False,
    log_cb: LogCallback | None = None,
) -> SyncResult:
    """Copy .agents/agents/*.md and AGENTS.md to Antigravity global config."""
    log = log_cb or print
    home = home_dir or get_home_dir()
    result = SyncResult()

    global_config = home / ".gemini" / "config"
    agents_src = source_root / ".agents" / "agents"
    agents_dst = global_config / "agents"
    rules_src = source_root / "AGENTS.md"
    rules_dst = global_config / "rules" / "global_agents.md"

    log("\n🤖 กำลังซิงค์ Antigravity Agents & Global Rules" + (" (Dry Run)" if dry_run else ""))
    if agents_src.is_dir():
        for md_file in sorted(agents_src.glob("*.md")):
            dst_file = agents_dst / md_file.name
            existed = dst_file.exists()
            try:
                if dry_run:
                    note = "จะอัปเดตของเดิม" if existed else "ติดตั้งใหม่"
                    log(f"  [Dry Run] Agent {md_file.name:<18} -> {dst_file}")
                    result.records.append(
                        SyncRecord(f"agent:{md_file.name}", "Antigravity IDE", "dry-run", str(dst_file), note)
                    )
                else:
                    agents_dst.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(md_file, dst_file)
                    if agents_dst not in result.touched_dirs:
                        result.touched_dirs.append(agents_dst)
                    action = "updated" if existed else "installed"
                    log(f"  ✅ [สำเร็จ] Agent {md_file.name:<18} -> {dst_file}")
                    result.records.append(
                        SyncRecord(f"agent:{md_file.name}", "Antigravity IDE", action, str(dst_file), "พร้อมใช้งาน")
                    )
                result.synced.append(f"agent:{md_file.name}")
            except Exception as exc:
                result.failed.append(f"agent:{md_file.name}: {exc}")
                result.records.append(
                    SyncRecord(f"agent:{md_file.name}", "Antigravity IDE", "failed", str(dst_file), str(exc))
                )
                log(f"  ❌ [ล้มเหลว] Agent {md_file.name}: {exc}")
    else:
        result.skipped.append(".agents/agents")
        result.records.append(
            SyncRecord("agents", "Antigravity IDE", "skipped", str(agents_dst), "ไม่พบโฟลเดอร์ .agents/agents")
        )
        log(f"  ℹ️ ข้าม Agents (ไม่พบโฟลเดอร์ {agents_src})")

    if rules_src.is_file():
        existed = rules_dst.exists()
        try:
            if dry_run:
                note = "จะอัปเดตของเดิม" if existed else "ติดตั้งใหม่"
                log(f"  [Dry Run] Global Rules         -> {rules_dst}")
                result.records.append(
                    SyncRecord("rules:global_agents.md", "Antigravity IDE", "dry-run", str(rules_dst), note)
                )
            else:
                rules_dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(rules_src, rules_dst)
                if rules_dst.parent not in result.touched_dirs:
                    result.touched_dirs.append(rules_dst.parent)
                action = "updated" if existed else "installed"
                log(f"  ✅ [สำเร็จ] Global Rules         -> {rules_dst}")
                result.records.append(
                    SyncRecord("rules:global_agents.md", "Antigravity IDE", action, str(rules_dst), "พร้อมใช้งาน")
                )
            result.synced.append("rules:global_agents.md")
        except Exception as exc:
            result.failed.append(f"rules:global_agents.md: {exc}")
            result.records.append(
                SyncRecord("rules:global_agents.md", "Antigravity IDE", "failed", str(rules_dst), str(exc))
            )
            log(f"  ❌ [ล้มเหลว] Global Rules: {exc}")
    else:
        result.skipped.append("AGENTS.md")
        result.records.append(
            SyncRecord("rules:global_agents.md", "Antigravity IDE", "skipped", str(rules_dst), "ไม่พบ AGENTS.md")
        )
        log(f"  ℹ️ ข้าม Global Rules (ไม่พบ {rules_src})")

    return result


def build_cursor_rules(
    source_root: Path,
    output_dir: Path | None = None,
    *,
    dry_run: bool = False,
    log_cb: LogCallback | None = None,
) -> Path | None:
    """Compile AGENTS.md + deep-planning SKILL.md into dist/global_cursorrules.md."""
    log = log_cb or print
    agents_file = source_root / "AGENTS.md"
    skill_file = source_root / ".agents" / "skills" / "deep-planning" / "SKILL.md"
    if not skill_file.is_file():
        skill_file = source_root / "skills" / "deep-planning" / "SKILL.md"

    if not agents_file.is_file() or not skill_file.is_file():
        log("  ℹ️ ข้ามการสร้าง dist/global_cursorrules.md (ไม่พบ AGENTS.md หรือ deep-planning)")
        return None

    target_root = output_dir or find_local_repo_root()
    if target_root is None:
        log("  ℹ️ ข้ามการสร้าง dist/global_cursorrules.md (ไม่ได้รันในโฟลเดอร์ repo)")
        return None

    out_path = target_root / "dist" / "global_cursorrules.md"
    if dry_run:
        log(f"  [Dry Run] Cursor Rules Adapter -> {out_path}")
        return out_path

    agents_content = agents_file.read_text(encoding="utf-8").strip()
    _, skill_body = parse_frontmatter(skill_file.read_text(encoding="utf-8"))

    compiled = (
        "# Global Agent Rules\n"
        f"{agents_content}\n\n"
        "---\n\n"
        "# Available Skills\n\n"
        "## 1. deep-planning\n"
        "**Use for:** Any non-trivial coding task — new features, multi-file changes, "
        "architecture decisions, bug fixes with unclear root cause.\n\n"
        "**Instructions:**\n"
        f"{skill_body.lstrip()}"
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(compiled, encoding="utf-8")
    log(f"  ✅ [สำเร็จ] Cursor Rules Adapter -> {out_path}")
    return out_path


def run_sync_pipeline(
    source_root: Path,
    skill_targets: list[str] | None,
    provider_keys: list[str],
    *,
    mode: str = "skills",
    home_dir: Path | None = None,
    output_dir: Path | None = None,
    dry_run: bool = False,
    log_cb: LogCallback | None = None,
) -> SyncResult:
    """Run skills sync and optional full Antigravity + Cursor dist setup."""
    log = log_cb or print
    combined = SyncResult()

    def _merge(sub: SyncResult) -> None:
        combined.synced.extend(sub.synced)
        combined.skipped.extend(sub.skipped)
        combined.failed.extend(sub.failed)
        combined.records.extend(sub.records)
        for d in sub.touched_dirs:
            if d not in combined.touched_dirs:
                combined.touched_dirs.append(d)

    _merge(
        sync_skills(
            source_root,
            skill_targets,
            provider_keys,
            home_dir=home_dir,
            dry_run=dry_run,
            log_cb=log,
        )
    )

    if mode == "full":
        _merge(
            sync_antigravity_extras(
                source_root,
                home_dir=home_dir,
                dry_run=dry_run,
                log_cb=log,
            )
        )

        dist_path = build_cursor_rules(
            source_root,
            output_dir=output_dir,
            dry_run=dry_run,
            log_cb=log,
        )
        if dist_path is not None:
            combined.synced.append(f"dist:{dist_path.name}")
            combined.records.append(
                SyncRecord(
                    "dist:global_cursorrules.md",
                    "Cursor / OpenCode",
                    "dry-run" if dry_run else "updated",
                    str(dist_path),
                    "สร้าง Adapter เรียบร้อย",
                )
            )
        else:
            combined.skipped.append("dist:global_cursorrules.md")
            combined.records.append(
                SyncRecord(
                    "dist:global_cursorrules.md",
                    "Cursor / OpenCode",
                    "skipped",
                    "-",
                    "ข้าม (ไม่ได้รันในโฟลเดอร์ repo)",
                )
            )

    log("\n🎉 ดำเนินการเสร็จสิ้น!")
    return combined


def launch_gui(force_github: bool = False) -> int:
    """Launch the PySide6 desktop GUI."""
    try:
        from sync_gui import run_gui  # type: ignore
    except ImportError:
        scripts_dir = str(Path(__file__).resolve().parent)
        if scripts_dir not in sys.path:
            sys.path.insert(0, scripts_dir)
        try:
            from sync_gui import run_gui  # type: ignore
        except ImportError as exc:
            print(
                "❌ ไม่สามารถเปิดโหมด GUI ได้เนื่องจากยังไม่ได้ติดตั้ง PySide6\n"
                "วิธีติดตั้ง: uv sync --extra gui  หรือ  pip install PySide6-Essentials\n"
                "หรือดาวน์โหลดไฟล์ .exe สำเร็จรูปได้จากหน้า GitHub Releases ของโปรเจกต์\n"
                f"รายละเอียด: {exc}"
            )
            return 1
    return run_gui(force_github=force_github)


def _interactive_cli(source_root: Path, dry_run: bool) -> int:
    print("\n=======================================================")
    print(" 🛠️  โปรแกรมซิงค์ Skill ไปยัง AI Providers (Interactive)")
    print("=======================================================\n")

    skills = discover_skills(source_root)
    if not skills:
        print("❌ ไม่พบโฟลเดอร์สกิลในโฟลเดอร์ 'skills/'")
        return 1

    print("📌 [ขั้นตอนที่ 1/3] เลือกรูปแบบการซิงค์:")
    print("   [1] เฉพาะ Skills (แนะนำ — ปลอดภัย ไม่ทับ Rules/Agents เดิม)")
    print("   [2] ครบชุด Full Setup (Skills + Antigravity Agents/Rules + dist)")
    mode_choice = input("\n👉 เลือกโหมด [1/2] (Enter = 1): ").strip()
    mode = "full" if mode_choice == "2" else "skills"

    print("\n📌 [ขั้นตอนที่ 2/3] เลือก Skill ที่ต้องการส่ง:")
    for idx, info in enumerate(skills, 1):
        print(f"   [{idx}] {info.name}")
    print(f"   [A] เลือกทุก Skill ทั้งหมด ({len(skills)} สกิล)")

    skill_choice = input("\n👉 เลือกหมายเลข Skill (คั่นด้วย comma ได้, Enter = ทั้งหมด): ").strip().lower()
    if skill_choice in ("", "a", "all"):
        selected_skills: list[str] | None = None
    else:
        selected_skills = []
        for part in skill_choice.split(","):
            part = part.strip()
            if part.isdigit() and 1 <= int(part) <= len(skills):
                name = skills[int(part) - 1].name
                if name not in selected_skills:
                    selected_skills.append(name)
            else:
                print(f"❌ ตัวเลือกไม่ถูกต้อง: {part}")
                return 1

    detected = detect_providers()
    print("\n📌 [ขั้นตอนที่ 3/3] เลือก AI Provider ปลายทาง:")
    print("   [A] ส่งไปยังทุก Provider ทั้งหมด (Recommended)")
    for spec in PROVIDERS:
        badge = "พบในเครื่อง" if detected.get(spec.key) else "จะสร้างใหม่"
        print(f"   [{spec.key}] {spec.name:<22} ({badge})")

    provider_choice = input("\n👉 เลือก Provider (คั่นด้วย comma ได้ เช่น 1,2 หรือ Enter = ทั้งหมด): ").strip()
    try:
        selected_providers = parse_provider_selection(provider_choice or "all")
    except ValueError as exc:
        print(f"❌ {exc}")
        return 1

    res = run_sync_pipeline(
        source_root,
        selected_skills,
        selected_providers,
        mode=mode,
        dry_run=dry_run,
    )
    return 1 if res.failed else 0


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="ซิงค์ Skill, Custom Agents และ Global Rules ไปยัง AI Providers",
    )
    parser.add_argument(
        "target",
        nargs="?",
        help="ชื่อ skill, พาธโฟลเดอร์ หรือทางลัด: all | full | ui",
    )
    parser.add_argument(
        "provider_pos",
        nargs="?",
        help="Provider ทางลัดแบบไม่ต้องใส่ -p เช่น antigravity, claude, all",
    )
    parser.add_argument("--all", action="store_true", help="ซิงค์ทุก skill ใน skills/")
    parser.add_argument(
        "--mode",
        choices=("skills", "full"),
        default=None,
        help="โหมด: skills (เฉพาะสกิล) หรือ full (สกิล + Antigravity agents/rules + dist)",
    )
    parser.add_argument(
        "-p",
        "--provider",
        help="เลือก Provider คั่นด้วย comma ได้ เช่น antigravity,claude หรือ all",
    )
    parser.add_argument(
        "--from-github",
        action="store_true",
        help=f"ดึงไฟล์ล่าสุดจาก GitHub ({DEFAULT_GITHUB_REPO}@{DEFAULT_GITHUB_BRANCH}) แทนไฟล์ในเครื่อง",
    )
    parser.add_argument("--dry-run", action="store_true", help="จำลองผลลัพธ์โดยไม่เขียนไฟล์จริง")
    parser.add_argument("--gui", action="store_true", help="เปิดหน้าจอ UX & UI (PySide6)")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)

    target_lower = (args.target or "").strip().lower()
    if args.gui or target_lower in ("ui", "gui"):
        return launch_gui(force_github=args.from_github)

    temp_dir: tempfile.TemporaryDirectory[str] | None = None
    try:
        local_root = None if args.from_github else find_local_repo_root()
        if local_root is not None:
            source_root = local_root
        else:
            temp_dir = tempfile.TemporaryDirectory(prefix="skill-agents-")
            source_root = fetch_repo_from_github(dest_dir=Path(temp_dir.name), log_cb=print)

        if target_lower == "all" or args.all or target_lower == "full":
            mode = args.mode or ("full" if target_lower == "full" else "skills")
            raw_provider = args.provider or args.provider_pos or "all"
            try:
                provider_keys = parse_provider_selection(raw_provider)
            except ValueError as exc:
                print(f"❌ {exc}")
                return 1
            res = run_sync_pipeline(
                source_root,
                None,
                provider_keys,
                mode=mode,
                dry_run=args.dry_run,
            )
            return 1 if res.failed else 0

        if args.target:
            raw_provider = args.provider or args.provider_pos or "all"
            try:
                provider_keys = parse_provider_selection(raw_provider)
            except ValueError as exc:
                print(f"❌ {exc}")
                return 1
            mode = args.mode or "skills"
            res = run_sync_pipeline(
                source_root,
                [args.target],
                provider_keys,
                mode=mode,
                dry_run=args.dry_run,
            )
            return 1 if res.failed else 0

        return _interactive_cli(source_root, dry_run=args.dry_run)
    except Exception as exc:
        print(f"❌ เกิดข้อผิดพลาด: {exc}")
        return 1
    finally:
        if temp_dir is not None:
            temp_dir.cleanup()


if __name__ == "__main__":
    raise SystemExit(main())
