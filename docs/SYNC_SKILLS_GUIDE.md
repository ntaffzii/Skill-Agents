# SYNC_SKILLS — คู่มือการใช้คำสั่งซิงค์สกิลไปยัง AI Providers

คู่มือนี้อธิบายการใช้งาน `sync_skills.py` และคำสั่ง `.\sync` สำหรับคัดลอกสกิลจากคลัง `skills/` ในโปรเจกต์นี้ไปยัง AI Providers ต่างๆ บนเครื่องของคุณโดยอัตโนมัติ

---

## สกิลถูกนำไปวางที่ไหน?

| AI Provider | Global Path |
| :-- | :-- |
| **Antigravity IDE** | `~/.gemini/config/skills/<ชื่อสกิล>/` |
| **Claude Code (CLI)** | `~/.claude/skills/<ชื่อสกิล>/` |
| **OpenCode Interpreter** | `~/.opencode/skills/<ชื่อสกิล>/` |

> **หมายเหตุ:** `~` หมายถึง `C:\Users\<ชื่อผู้ใช้ของคุณ>` บน Windows

---

## ไฟล์ที่เกี่ยวข้อง

```text
skill-agents/
├── sync.bat              ← ทางลัดสำหรับ Windows Command Prompt
├── sync.ps1              ← ทางลัดสำหรับ PowerShell
└── scripts/
    └── sync_skills.py    ← สคริปต์หลักที่ทำงานจริง
```

---

## วิธีใช้งาน

### 1. แบบ Interactive (เมนูโต้ตอบ) — แนะนำสำหรับผู้เริ่มต้น ⭐

เปิด Terminal แล้วพิมพ์:

```powershell
.\sync
```

ระบบจะแสดงเมนู **2 ขั้นตอน** ให้เลือกแบบโต้ตอบ:

```text
=======================================================
 🛠️  โปรแกรมซิงค์ Skill ไปยัง AI Providers (Interactive)
=======================================================

📌 [ขั้นตอนที่ 1/2] เลือก Skill ที่ต้องการส่ง:
   [1] thai
   [2] trading
   [3] engineering
   ...
   [A] เลือกทุก Skill ทั้งหมด (10 สกิล)

👉 กรุณาเลือกหมายเลข Skill (หรือกด Enter เพื่อเลือกทั้งหมด):

📌 [ขั้นตอนที่ 2/2] เลือก AI Provider ปลายทาง:
   [A] ส่งไปยังทุก Provider ทั้งหมด (Recommended)
   [1] Antigravity IDE  (~/.gemini/config/skills)
   [2] Claude Code      (~/.claude/skills)
   [3] OpenCode         (~/.opencode/skills)

👉 กรุณาเลือก Provider (หรือกด Enter เพื่อเลือกทุกตัว):
```

---

### 2. แบบระบุชื่อสกิล One-liner (เร็วที่สุด)

ส่งสกิลชื่อที่ต้องการไปยังทุก Provider พร้อมกันทันที:

```powershell
.\sync <ชื่อสกิล>
```

**ตัวอย่าง:**

```powershell
.\sync thai
.\sync trading
.\sync engineering
```

---

### 3. แบบระบุทั้งสกิลและ Provider

ส่งสกิลที่ต้องการไปยัง Provider ที่เจาะจง:

```powershell
.\sync <ชื่อสกิล> <ชื่อ provider>
```

**ชื่อ Provider ที่รองรับ:** `antigravity`, `claude`, `opencode`

**ตัวอย่าง:**

```powershell
# ส่งสกิล thai ไปแค่ Antigravity IDE เท่านั้น
.\sync thai antigravity

# ส่งสกิล trading ไปแค่ Claude Code เท่านั้น
.\sync trading claude

# ส่งสกิล engineering ไปแค่ OpenCode เท่านั้น
.\sync engineering opencode
```

---

### 4. แบบ Python CLI โดยตรง

สำหรับผู้ที่ต้องการควบคุมเต็มรูปแบบผ่านคำสั่ง Python:

```powershell
# Interactive menu
python scripts/sync_skills.py

# ระบุสกิล
python scripts/sync_skills.py thai

# ระบุสกิล + Provider
python scripts/sync_skills.py thai -p antigravity
python scripts/sync_skills.py trading -p claude
```

---

## ตัวอย่างผลลัพธ์เมื่อทำงานสำเร็จ

```text
🚀 กำลังส่งโฟลเดอร์ Skill: [thai] ...
  ✅ [สำเร็จ] Antigravity IDE        -> C:\Users\natth\.gemini\config\skills\thai
  ✅ [สำเร็จ] Claude Code            -> C:\Users\natth\.claude\skills\thai
  ✅ [สำเร็จ] OpenCode Interpreter   -> C:\Users\natth\.opencode\skills\thai
🎉 ดำเนินการเรียบร้อยแล้ว!
```

---

## คำถามที่พบบ่อย (FAQ)

### Q: ถ้ารันซ้ำจะเกิดอะไรขึ้น?

A: สคริปต์จะ**ลบโฟลเดอร์สกิลเก่าออกแล้วคัดลอกใหม่ทั้งหมด** ทุกครั้งที่รัน — ใช้ได้อย่างปลอดภัย ไม่มีการซ้อนทับหรือข้อมูลค้างเก่า

### Q: ถ้า Provider ยังไม่ได้ติดตั้ง จะเกิดอะไรขึ้น?

A: สคริปต์จะ**สร้างโฟลเดอร์ให้อัตโนมัติ** แม้ว่า Provider นั้นจะยังไม่ได้ติดตั้งในเครื่อง — ไม่มี Error

### Q: สกิลที่อยู่ในโฟลเดอร์ `skills/` แต่ไม่มี `SKILL.md` จะถูกซิงค์ไหม?

A: สคริปต์คัดลอกทั้งโฟลเดอร์ ไม่ว่าจะมี `SKILL.md` หรือไม่ — แต่ AI Provider ส่วนใหญ่จะ**ตรวจพบเฉพาะโฟลเดอร์ที่มี `SKILL.md` และ YAML Frontmatter ครบถ้วน** เท่านั้น

### Q: ต้องการเพิ่ม Provider ใหม่ได้ไหม?

A: ได้ครับ — แก้ไข `PROVIDERS_MAP` ในไฟล์ `scripts/sync_skills.py` โดยเพิ่ม entry ใหม่:

```python
PROVIDERS_MAP = {
    ...
    "4": ("Cursor AI", HOME / ".cursor" / "rules"),  # เพิ่ม Provider ใหม่
}
```

---

## ไฟล์ที่เกี่ยวข้องในโปรเจกต์

| ไฟล์ | คำอธิบาย |
| :-- | :-- |
| [sync.bat](../sync.bat) | ทางลัดรันบน Windows CMD |
| [sync.ps1](../sync.ps1) | ทางลัดรันบน PowerShell |
| [scripts/sync_skills.py](../scripts/sync_skills.py) | สคริปต์หลัก Python |
