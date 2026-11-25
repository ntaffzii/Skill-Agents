# SYNC_SKILLS — คู่มือการใช้คำสั่งซิงค์สกิลและหน้าจอ GUI

คู่มือนี้อธิบายการใช้งาน `sync_skills.py`, คำสั่งทางลัด (`.\sync`, `./sync.sh`), หน้าจอ GUI (`PySide6`), และการดาวน์โหลดจาก **GitHub Releases** ไปใช้บนเครื่องอื่นโดยไม่ต้องติดตั้ง Python

---

## สกิลถูกนำไปวางที่ไหน?

| AI Provider | Global Path |
| :-- | :-- |
| **Antigravity IDE** | `~/.gemini/config/skills/<ชื่อสกิล>/` |
| **Claude Code (CLI)** | `~/.claude/skills/<ชื่อสกิล>/` |
| **OpenCode Interpreter** | `~/.opencode/skills/<ชื่อสกิล>/` |
| **Qwen Code** | `~/.qwen/skills/<ชื่อสกิล>/` |
| **ZCode** | `~/.zcode/skills/<ชื่อสกิล>/` |
| **Codex CLI** | `~/.codex/skills/<ชื่อสกิล>/` |
| **LM Studio** | `~/.lmstudio/skills/<ชื่อสกิล>/` |

> **โหมด Full Setup:** นอกจากสกิลแล้ว ยังซิงค์ `.agents/agents/*.md` ไปที่ `~/.gemini/config/agents/`, `AGENTS.md` ไปที่ `~/.gemini/config/rules/global_agents.md`, และสร้าง `dist/global_cursorrules.md` (เมื่อรันในโฟลเดอร์ repo)

---

## ไฟล์ที่เกี่ยวข้อง

```text
skill-agents/
├── sync.bat                  ← ทางลัด Windows CMD (ตรวจหา Python อัตโนมัติ)
├── sync.ps1                  ← ทางลัด PowerShell (ตรวจหา Python อัตโนมัติ)
├── sync.sh                   ← ทางลัด macOS / Linux
└── scripts/
    ├── sync_skills.py        ← แกนหลัก CLI & Sync Engine (stdlib ล้วน)
    ├── sync_gui.py           ← หน้าจอ Desktop UX & UI (PySide6)
    └── build_release.ps1     ← สคริปต์ build ไฟล์ .exe / .zip สำหรับ Release
```

---

## วิธีใช้งาน

### 1. ดาวน์โหลดจาก GitHub Releases (สำหรับเครื่องอื่นที่ไม่มี Python / ไม่ได้ Clone)

1. ไปที่หน้า **Releases** ของ GitHub repo แล้วดาวน์โหลด `SkillAgentsSync.exe` หรือ `SkillAgentsSync-windows-x64.zip`
2. ดับเบิลคลิกเปิดโปรแกรม — ตัวแอปจะดึงรายการ `skills/` ล่าสุดจาก GitHub ให้อัตโนมัติ และตรวจจับ AI Apps ที่มีอยู่ในเครื่องให้ก่อน
3. กดเลือก/ค้นหา Skills และ Providers ที่ต้องการ แล้วกดปุ่ม **ติดตั้ง** (มีปุ่ม **จำลองผล (Dry Run)** และปุ่ม **เปิดโฟลเดอร์ปลายทาง** หลังติดตั้งเสร็จ)

---

### 2. เปิดหน้าจอ GUI จากใน Repo (`.\sync ui`)

ต้องติดตั้ง optional dependency `[gui]` ครั้งแรกก่อน:

```powershell
uv pip install --python .\.venv\Scripts\python.exe ".[gui]"
.\sync ui
```

หรือดึงข้อมูลสดจาก GitHub แทนไฟล์ในเครื่อง:

```powershell
.\sync ui --from-github
```

---

### 3. คำสั่ง CLI แบบสั้น (One-word Shortcuts)

```powershell
# ซิงค์ทุก Skill ไปยังทุก Provider (โหมด Skills เท่านั้น — ปลอดภัย)
.\sync all

# ซิงค์ครบชุด: Skills + Antigravity Agents/Rules + dist/global_cursorrules.md
.\sync full

# ซิงค์เฉพาะสกิลและระบุ Provider (รองรับหลายตัวคั่นด้วย comma)
.\sync thai antigravity
.\sync trading -p antigravity,claude

# จำลองผลโดยไม่เขียนไฟล์จริง
.\sync all --dry-run

# ดึงไฟล์ล่าสุดจาก GitHub โดยตรง (ใช้ได้แม้ไม่ได้รันจากโฟลเดอร์ repo)
python scripts/sync_skills.py all --from-github
```

บน macOS / Linux:

```bash
chmod +x sync.sh
./sync.sh all
./sync.sh ui
```

---

### 4. เมนู Interactive (3 ขั้นตอน)

เปิด Terminal แล้วพิมพ์ `.\sync` (หรือดับเบิลคลิก `sync.bat`):

1. เลือกโหมด: `[1] เฉพาะ Skills` (แนะนำ) หรือ `[2] ครบชุด Full Setup`
2. เลือก Skill: กด Enter เพื่อเลือกทั้งหมด หรือพิมพ์หมายเลขคั่นด้วย comma (เช่น `1,3`)
3. เลือก AI Provider: ระบบจะแสดงสถานะ `พบในเครื่อง` / `จะสร้างใหม่` ให้เห็นชัดเจน

---

## การ Build และออก GitHub Release

- **Build ในเครื่อง Windows:**
  ```powershell
  uv pip install --python .\.venv\Scripts\python.exe ".[gui,build]"
  .\scripts\build_release.ps1
  ```
  ผลลัพธ์จะอยู่ที่ `dist/release/SkillAgentsSync.exe`, `SkillAgentsSync-windows-x64.zip`, และ `SHA256SUMS.txt`
- **ปล่อย Release อัตโนมัติบน GitHub:** สร้างและ push tag ที่ขึ้นต้นด้วย `v` (เช่น `git tag v1.0.0 && git push origin v1.0.0`) เพื่อให้ GitHub Actions (`.github/workflows/release.yml`) build และเผยแพร่บนหน้า Releases ให้อัตโนมัติ
