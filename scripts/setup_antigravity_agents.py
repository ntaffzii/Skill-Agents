#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
สคริปต์สำหรับติดตั้ง Custom Agents (architect, implementer)
จาก .agents/agents/ ลงในระบบ Antigravity ระดับ Global (~/.gemini/config/agents/)
"""

import shutil
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def save_agents(workspace_root: Path | None = None, home_dir: Path | None = None) -> int:
    root = workspace_root or Path(__file__).resolve().parent.parent
    home = home_dir or Path.home()

    local_agents_dir = root / ".agents" / "agents"
    global_agents_dir = home / ".gemini" / "config" / "agents"
    agent_files = ("architect.md", "implementer.md")

    print("==================================================")
    print(" 🤖 เริ่มติดตั้ง Antigravity Custom Agents...")
    print("==================================================\n")

    missing = [name for name in agent_files if not (local_agents_dir / name).is_file()]
    if missing:
        print(f"❌ ไม่พบไฟล์ต้นฉบับใน {local_agents_dir}: {', '.join(missing)}")
        return 1

    global_agents_dir.mkdir(parents=True, exist_ok=True)
    for name in agent_files:
        src = local_agents_dir / name
        dst = global_agents_dir / name
        shutil.copy2(src, dst)
        print(f"✅ คัดลอก {name}")
        print(f"   {src} -> {dst}")

    print("\n🎉 ติดตั้ง Antigravity Agents เรียบร้อยแล้ว!")
    return 0


if __name__ == "__main__":
    raise SystemExit(save_agents())
