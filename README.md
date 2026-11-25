# Skill Agents

Personal AI-agent skills, workflows, prompts, custom agents, and cross-provider sync tools for working with AI coding assistants and local LLMs.

This repo is the **skill, agent, and workflow layer**. It gives AI assistants reusable `SKILL.md` playbooks, ordered workflows, custom subagent definitions, and a standalone desktop/CLI installer to sync them across tools.

For executable MCP tools, use the companion repo:

[ntaffzii/ai-desk-tools](https://github.com/ntaffzii/ai-desk-tools)

```text
Skill-Agents       = skills, workflows, custom agents, sync GUI/CLI, docs, examples
ai-desk-tools      = MCP server, Python tools, tests, runtime safety policy
local-llm          = llama.cpp Router, FastAPI Orchestrator, Docker deployment
```

Recommended Local LLM repository name: `ntaffzii/local-llm-orchestrator`.

## Who This Is For

Use this repo if you want an AI agent to:

- follow reusable `SKILL.md` instructions across domain tasks (engineering, UX/UI, Thai locale, trading, research, Obsidian)
- use workflow playbooks such as `ship-feature`, `debug-regression`, or `daily-personal-agent`
- work across Antigravity IDE, Claude Code, OpenCode, Qwen Code, ZCode, Codex CLI, LM Studio, and local LLMs
- sync skills, custom agents, and global rules to another machine in one click (via standalone `.exe` or cross-platform launchers)
- route tasks to the right skill/workflow before loading context
- keep personal automation safe with draft-only and read-only defaults

## Install Skills

### Option 1: Standalone Windows Desktop App (GitHub Releases — No Python Required)

For users on another machine who do not want to install Python or `git clone`:

1. Download `SkillAgentsSync.exe` (or `SkillAgentsSync-windows-x64.zip`) from the [GitHub Releases](https://github.com/ntaffzii/Skill-Agents/releases/latest) page.
2. Double-click to launch the **PySide6 3-View GUI**:
   - **1. ติดตั้ง & ซิงค์:** Pick skills via 2-line cards (with descriptions, sub-skill counts, and local install badges), auto-detect installed AI providers on your machine, and sync or dry-run in one click.
   - **2. คลัง Skills & คู่มือ:** Browse the skill/sub-skill tree, read formatted `SKILL.md` documentation, and inspect supporting files (`references/`, `scripts/`, `templates/`).
   - **3. สถานะ & ผลลัพธ์:** Inspect an Installed Matrix across all 7 providers (double-click installed cells to open the folder) and review structured sync/dry-run results.
3. When run outside a cloned repository, the app automatically fetches the latest `skills/`, `.agents/`, and `AGENTS.md` from GitHub (`main`).

> **Windows SmartScreen Note:** Because the release binary is unsigned, Windows may show a SmartScreen prompt on first launch (`More info` -> `Run anyway`). You can verify integrity against `SHA256SUMS.txt` in each release.

### Option 2: Automatic Sync CLI & GUI from Repo

This repo includes cross-platform sync launchers (`sync.bat`, `sync.ps1`, `sync.sh`) that automatically detect `.venv`, `py`, `python3`, `python`, or `uv`:

```powershell
# Launch PySide6 Desktop GUI (first-time setup: uv pip install --python .\.venv\Scripts\python.exe ".[gui]")
.\sync ui

# Quick one-word shortcuts
.\sync all                   # Sync all skills to all providers (safe: does not overwrite rules/agents)
.\sync full                  # Sync all skills + Antigravity agents/rules + dist/global_cursorrules.md
.\sync thai antigravity      # Sync specific skill to specific provider
.\sync --all -p antigravity,claude --dry-run

# Interactive 3-step menu
.\sync
```

On macOS / Linux:

```bash
chmod +x sync.sh
./sync.sh all
./sync.sh ui
```

Supported providers:

| Key | Provider | CLI Alias | Global Skills Path |
| :-- | :-- | :-- | :-- |
| `1` | Antigravity IDE | `antigravity`, `gemini` | `~/.gemini/config/skills/` |
| `2` | Claude Code | `claude` | `~/.claude/skills/` |
| `3` | OpenCode Interpreter | `opencode` | `~/.opencode/skills/` |
| `4` | Qwen Code | `qwen` | `~/.qwen/skills/` |
| `5` | ZCode | `zcode` | `~/.zcode/skills/` |
| `6` | Codex CLI | `codex` | `~/.codex/skills/` |
| `7` | LM Studio | `lmstudio` | `~/.lmstudio/skills/` |

Full usage guide: [docs/SYNC_SKILLS_GUIDE.md](docs/SYNC_SKILLS_GUIDE.md)

### Manual Install

If you prefer to copy files manually:

```bash
# Claude Code
cp -R skills/* ~/.claude/skills/

# Antigravity IDE
cp -R skills/* ~/.gemini/config/skills/
```

On Windows PowerShell:

```powershell
# Antigravity IDE
Copy-Item -Recurse .\skills\* "$env:USERPROFILE\.gemini\config\skills\"

# Claude Code
Copy-Item -Recurse .\skills\* "$env:USERPROFILE\.claude\skills\"
```

## Companion Repo & Quick Start

Clone this repo:

```bash
git clone https://github.com/ntaffzii/Skill-Agents.git
cd Skill-Agents
```

Read first:

- [QUICKSTART.md](QUICKSTART.md)
- [docs/COMPLETE_LOCAL_AI_SYSTEM.md](docs/COMPLETE_LOCAL_AI_SYSTEM.md)
- [docs/PROJECT_GUIDE.md](docs/PROJECT_GUIDE.md)
- [docs/USAGE_FOR_PERSONAL_AND_OTHERS.md](docs/USAGE_FOR_PERSONAL_AND_OTHERS.md)

Then clone the companion MCP tools repo when needed:

```bash
git clone https://github.com/ntaffzii/ai-desk-tools.git
cd ai-desk-tools
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Configure LM Studio, Claude Desktop, or another MCP client to run `ai-desk-tools/server.py`.

## Local LLM Usage

For LM Studio, Ollama, llama.cpp, vLLM, or any local LLM that does not have native skill loading, use:

[examples/local-llm-agent-prompt.md](examples/local-llm-agent-prompt.md)

Recommended flow:

```text
User request
  -> skill-runtime.route_request
  -> prompt-improver if unclear
  -> skill-runtime.build_agent_context
  -> use recommended toolset/tools
  -> answer with verification
```

The `skill-runtime` and `prompt-improver` tools live in [ntaffzii/ai-desk-tools](https://github.com/ntaffzii/ai-desk-tools).

## LM Studio MCP Setup

1. Clone and install [ntaffzii/ai-desk-tools](https://github.com/ntaffzii/ai-desk-tools)
2. Open LM Studio
3. Go to `Program > Install > Edit mcp.json`
4. Add a server pointing to `ai-desk-tools/server.py`

Example config: [examples/lm-studio-mcp-config.json](examples/lm-studio-mcp-config.json)

For model/provider settings, see:

- [config.json](config.json)
- [docs/CONFIG_JSON_GUIDE.md](docs/CONFIG_JSON_GUIDE.md)
- [docs/LOCAL_LLM_SETTINGS.md](docs/LOCAL_LLM_SETTINGS.md)
- [docs/PROMPT_IMPROVER_LOCAL_MODEL.md](docs/PROMPT_IMPROVER_LOCAL_MODEL.md)

Recommended prompt-improver model when available: `LFM2.5-8B-A1B` (recommended, not required).

## Repo Layout

```text
Skill-Agents/
  .agents/         custom agent definitions (architect, implementer) and workspace skills
  .github/         GitHub Actions release workflow (Windows .exe / .zip)
  Skill.md/        portable model-neutral skills
  skills/          local skill folders with SKILL.md
  workflows/       ordered workflow playbooks
  data/            tools/toolsets/workflows/skills-index registry metadata
  dist/            compiled adapter outputs (global_cursorrules.md)
  docs/            guides and usage docs
  examples/        prompts and MCP client examples
  scripts/         sync engine, PySide6 GUI, release builder, and validators
  AGENTS.md        project-wide agent operating rules
  config.json      provider/model/preset reference
  pyproject.toml   Python project metadata and optional [gui] / [build] extras
  sync.bat         Windows CMD sync wrapper
  sync.ps1         Windows PowerShell sync wrapper
  sync.sh          macOS / Linux sync wrapper
```

## Main Workflows

- `ship-feature` - implement and verify a feature end to end
- `debug-regression` - reproduce, diagnose, fix, and verify a regression
- `review-pr` - review a diff or PR with findings first
- `obsidian-vault-cleanup` - organize Obsidian notes safely
- `create-new-skill` - create a new reusable skill
- `build-mcp-tool` - design a new MCP tool
- `research-report` - create sourced research reports
- `daily-personal-agent` - build a personal daily plan
- `personal-knowledge-sync` - connect Obsidian, Notion, memory, and RAG

## Skill Categories

- `deep-planning/` - structured planning workflow before code changes
- `engineering/` - diagnose, TDD, code review, architecture review, UI design engineering, UX/UI design assessment
- `research/` - news, GitHub skill research, project discovery, claim/citation integrity check, repo-tour
- `productivity/` - handoff, prompt improvement, reports, automation, inbox triage, grill-with-docs
- `project-docs-prep/` - scaffold AI-agent-ready project documentation (5 numbered specs + `AGENTS.md`, `DESIGN.md`, `CLAUDE.md`, `README.md`)
- `obsidian/` - Markdown, Canvas, vault workflow, Notion bridge
- `misc/` - skill and MCP tool management
- `seo-website-evaluator/` - 6-category SEO and AI Search (GEO) audit
- `thai/` - Thai-locale domain knowledge (tax invoices, government letters, PDPA, ID/PromptPay validation, dates, translation, resumes)
- `trading/` - market regime, position sizing, risk gates, portfolio review, trade journaling (not financial advice)
- `personal/` - private/personal preferences and daily-agent workflow
- `in-progress/` - draft skills
- `deprecated/` - retired skills with replacement guidance

## Portable Skill.md

`Skill.md/` contains portable skills that can be copied into other agents:

- `universal-agent-operating-system`
- `model-portability-adapter`
- `tool-agnostic-mcp-routing`
- `cross-model-handoff`

Use these when a provider does not support native skill folders.

## Common Prompts

Daily planning:

```text
Use daily-personal-agent. Build today's plan from my Obsidian notes, Notion context, memory, calendar, inbox, chat, and open issues. Draft replies but do not send anything.
```

Obsidian to Notion:

```text
Use personal-knowledge-sync. Treat Obsidian as source of truth. Draft Notion payloads only and preserve tags, wikilinks, aliases, and source paths.
```

Code work:

```text
Use ship-feature. Inspect docs, repo index, tests, CI, and git before editing. Verify with the narrowest test.
```

Review:

```text
Use review-pr. Inspect the diff and related files. Report findings first with severity, file, and line reference.
```

Local LLM routing:

```text
Use skill-runtime first. Route this request, improve it only if unclear, then load selected workflow and skills.
```

## Documentation

### Getting Started

- [QUICKSTART.md](QUICKSTART.md)
- [docs/ONBOARDING.md](docs/ONBOARDING.md)
- [docs/PROJECT_GUIDE.md](docs/PROJECT_GUIDE.md)
- [docs/USAGE_FOR_PERSONAL_AND_OTHERS.md](docs/USAGE_FOR_PERSONAL_AND_OTHERS.md)

### Skills & Agents

- [docs/SYNC_SKILLS_GUIDE.md](docs/SYNC_SKILLS_GUIDE.md) — cross-platform sync CLI, 3-view PySide6 GUI, and GitHub Releases
- [docs/ANTIGRAVITY_AGENTS_GUIDE.md](docs/ANTIGRAVITY_AGENTS_GUIDE.md) — `architect` / `implementer` custom agents and `deep-planning` workflow
- [docs/NEW_SKILLS_GUIDE.md](docs/NEW_SKILLS_GUIDE.md) — guide to recently added skills
- [docs/SKILL_RUNTIME_FLOW.md](docs/SKILL_RUNTIME_FLOW.md)
- [docs/TOUR.md](docs/TOUR.md)

### Configuration & Setup

- [docs/CONFIG_JSON_GUIDE.md](docs/CONFIG_JSON_GUIDE.md)
- [docs/LOCAL_LLM_SETTINGS.md](docs/LOCAL_LLM_SETTINGS.md)
- [docs/PROMPT_IMPROVER_LOCAL_MODEL.md](docs/PROMPT_IMPROVER_LOCAL_MODEL.md)
- [docs/COMPLETE_LOCAL_AI_SYSTEM.md](docs/COMPLETE_LOCAL_AI_SYSTEM.md)

### Tools & Integrations

- [docs/TOOLS_INVENTORY.md](docs/TOOLS_INVENTORY.md)
- [docs/MCP_API_SERVER.md](docs/MCP_API_SERVER.md)
- [docs/WEB_CAPTURE_PROVIDERS.md](docs/WEB_CAPTURE_PROVIDERS.md)
- [docs/FINANCE_MARKET_PROVIDERS.md](docs/FINANCE_MARKET_PROVIDERS.md)
- [docs/RECOMMENDED_NEXT_TOOLS.md](docs/RECOMMENDED_NEXT_TOOLS.md)
- [NOTICE.md](NOTICE.md)

## Build & Release

Build the standalone Windows executable locally:

```powershell
uv pip install --python .\.venv\Scripts\python.exe ".[gui,build]"
.\scripts\build_release.ps1
```

Artifacts are written to `dist/release/`:

- `SkillAgentsSync.exe`
- `SkillAgentsSync-windows-x64.zip`
- `SHA256SUMS.txt`

To trigger an automated GitHub Release via [.github/workflows/release.yml](.github/workflows/release.yml):

```bash
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

## Validate

From the combined workspace (when `mcp-tools/` is present):

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\validate-all.ps1
```

Or validate skills directly:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\validate-skills.ps1
```

This validates:

- tool registry metadata, toolsets, and workflows
- `skills/**/SKILL.md` and `Skill.md/**/SKILL.md`
- `data/skills-index.json` (regenerate with `scripts/generate-skills-index.ps1` after adding/renaming/removing a skill)
- MCP tool Python syntax and tests when `mcp-tools/` is present

## Attribution

This repo is original work inspired by public agent-skill and MCP repositories. It is not an official fork, template, distribution, or endorsement of those projects.

See [NOTICE.md](NOTICE.md) for attribution and license notes.

## License

See [LICENSE](LICENSE).
