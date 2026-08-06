import os
import sys
import shutil
import argparse
from pathlib import Path

# ตำแหน่ง Home Directory ของผู้ใช้งานระบบ
HOME = Path.home()

# ตำแหน่งเป้าหมาย Global ของ Provider ต่างๆ
PROVIDERS_MAP = {
    "1": ("Antigravity IDE", HOME / ".gemini" / "config" / "skills"),
    "2": ("Claude Code", HOME / ".claude" / "skills"),
    "3": ("OpenCode Interpreter", HOME / ".opencode" / "skills"),
}

# Alias mapping สำหรับคำสั่ง CLI เช่น --provider antigravity
PROVIDER_ALIASES = {
    "antigravity": "1",
    "gemini": "1",
    "claude": "2",
    "opencode": "3",
    "all": "all",
}

def sync_skill(skill_path_or_name, selected_provider_keys=None):
    """
    คัดลอกโฟลเดอร์ Skill ไปยังโฟลเดอร์ของ AI Provider ที่เลือก
    """
    workspace_dir = Path(__file__).resolve().parent.parent
    skills_base_dir = workspace_dir / "skills"

    # ระบุตำแหน่งโฟลเดอร์ Skill ต้นทาง
    source_path = Path(skill_path_or_name)
    if not source_path.exists():
        source_path = skills_base_dir / skill_path_or_name

    if not source_path.exists() or not source_path.is_dir():
        print(f"❌ ไม่พบโฟลเดอร์ Skill ที่ตำแหน่ง: {skill_path_or_name}")
        return

    skill_name = source_path.name
    print(f"\n🚀 กำลังส่งโฟลเดอร์ Skill: [{skill_name}] ...")

    # กำหนด Provider เป้าหมาย
    if not selected_provider_keys or "all" in selected_provider_keys:
        target_keys = PROVIDERS_MAP.keys()
    else:
        target_keys = [k for k in selected_provider_keys if k in PROVIDERS_MAP]

    for key in target_keys:
        provider_name, target_base = PROVIDERS_MAP[key]
        target_skill_dir = target_base / skill_name

        try:
            target_base.mkdir(parents=True, exist_ok=True)
            
            if target_skill_dir.exists():
                shutil.rmtree(target_skill_dir)
            
            shutil.copytree(source_path, target_skill_dir)
            print(f"  ✅ [สำเร็จ] {provider_name:<22} -> {target_skill_dir}")
        except Exception as e:
            print(f"  ❌ [ล้มเหลว] {provider_name:<22} -> เกิดข้อผิดพลาด: {e}")

    print("🎉 ดำเนินการเรียบร้อยแล้ว!\n")

def list_skills():
    workspace_dir = Path(__file__).resolve().parent.parent
    skills_base_dir = workspace_dir / "skills"
    if not skills_base_dir.exists():
        return []
    return [d.name for d in skills_base_dir.iterdir() if d.is_dir()]

def main():
    parser = argparse.ArgumentParser(description="ซิงค์ Skill ไปยัง AI Providers")
    parser.add_argument("skill", nargs="?", help="ชื่อโฟลเดอร์ Skill ที่ต้องการซิงค์")
    parser.add_argument("-p", "--provider", help="เลือก Provider เช่น antigravity, claude, opencode, all")
    args = parser.parse_args()

    available_skills = list_skills()

    # กรณีระบุผ่าน CLI Argument
    if args.skill:
        selected_provider_keys = []
        if args.provider:
            p_lower = args.provider.lower()
            if p_lower in PROVIDER_ALIASES:
                target_alias = PROVIDER_ALIASES[p_lower]
                if target_alias != "all":
                    selected_provider_keys = [target_alias]
                else:
                    selected_provider_keys = ["all"]
        
        sync_skill(args.skill, selected_provider_keys)
        return

    # กรณีรันแบบ Interactive Menu
    print("\n=======================================================")
    print(" 🛠️  โปรแกรมซิงค์ Skill ไปยัง AI Providers (Interactive)")
    print("=======================================================\n")

    if not available_skills:
        print("❌ ไม่พบโฟลเดอร์สกิลในโฟลเดอร์ 'skills/' ของโปรเจกต์นี้")
        sys.exit(0)

    # Step 1: เลือก Skill
    print("📌 [ขั้นตอนที่ 1/2] เลือก Skill ที่ต้องการส่ง:")
    for idx, name in enumerate(available_skills, 1):
        print(f"   [{idx}] {name}")
    print(f"   [A] เลือกทุก Skill ทั้งหมด ({len(available_skills)} สกิล)")

    skill_choice = input("\n👉 กรุณาเลือกหมายเลข Skill (หรือกด Enter เพื่อเลือกทั้งหมด): ").strip().lower()
    
    selected_skills = []
    if skill_choice in ['a', 'all', '']:
        selected_skills = available_skills
    elif skill_choice.isdigit() and 1 <= int(skill_choice) <= len(available_skills):
        selected_skills = [available_skills[int(skill_choice) - 1]]
    else:
        print("❌ ตัวเลือกไม่ถูกต้อง ยกเลิกการทำงาน")
        sys.exit(0)

    # Step 2: เลือก Provider
    print("\n📌 [ขั้นตอนที่ 2/2] เลือก AI Provider ปลายทาง:")
    print("   [A] ส่งไปยังทุก Provider ทั้งหมด (Recommended)")
    print("   [1] Antigravity IDE  (~/.gemini/config/skills)")
    print("   [2] Claude Code      (~/.claude/skills)")
    print("   [3] OpenCode         (~/.opencode/skills)")

    provider_choice = input("\n👉 กรุณาเลือก Provider (หรือกด Enter เพื่อเลือกทุกตัว): ").strip().lower()

    selected_providers = []
    if provider_choice in ['a', 'all', '']:
        selected_providers = ["all"]
    elif provider_choice in PROVIDERS_MAP:
        selected_providers = [provider_choice]
    else:
        print("❌ ตัวเลือกไม่ถูกต้อง ส่งไปยังทุก Provider โดยอัตโนมัติ")
        selected_providers = ["all"]

    # ดำเนินการซิงค์
    for skill_name in selected_skills:
        sync_skill(skill_name, selected_providers)

if __name__ == "__main__":
    main()
