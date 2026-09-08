# คู่มือ Antigravity Custom Agents & Deep Planning Workflow

เอกสารฉบับนี้อธิบายโครงสร้าง บทบาท หน้าที่ และวิธีการเรียกใช้งาน **Custom Agents** และ **Skill** ที่ติดตั้งไว้ในระบบ Google Antigravity สำหรับโปรเจกต์ `Skill-Agents`

---

## 1. ภาพรวมสถาปัตยกรรม (Architecture Overview)

ระบบการทำงานแบ่งออกเป็น 3 องค์ประกอบหลัก เพื่อแยกบทบาท "การคิด/วางแผน" ออกจาก "การลงมือปฏิบัติ" อย่างชัดเจน:

```
[ User Request ]
       │
       ▼
 ┌─────────────┐
 │  AGENTS.md  │ ─── (กฎคุมพฤติกรรม: เช็คความซับซ้อนของงาน)
 └─────────────┘
       │
       ├── งานซับซ้อน / ฟีเจอร์ใหม่ / บั๊กไม่ทราบสาเหตุ
       ▼
 ┌─────────────────────────────────────────────────────────┐
 │ 🧠 architect (Subagent)                                  │
 │   - ใช้คู่มือ: deep-planning (Skill)                     │
 │   - วิเคราะห์โค้ดเดิม / สำรวจความเสี่ยง                  │
 │   - ร่าง Implementation Plan                             │
 │   - หยุดรอให้ User อนุมัติ ("Proceed")                  │
 └─────────────────────────────────────────────────────────┘
       │
       │ (User อนุมัติแผนแล้ว)
       ▼
 ┌─────────────────────────────────────────────────────────┐
 │ ⚡ implementer (Subagent)                                │
 │   - นำแผนที่อนุมัติแล้วมาเขียนโค้ด                       │
 │   - รันคำสั่ง และเทสต์ตามขั้นตอนอย่างเคร่งครัด           │
 │   - ไม่เปลี่ยนสถาปัตยกรรมเอง                             │
 └─────────────────────────────────────────────────────────┘
```

---

## 2. นิยามของ Agents แต่ละตัว

### 2.1 `architect` (เอเจนต์สถาปนิก / ผู้วางแผน)
- **ตำแหน่งไฟล์:** `.agents/agents/architect.md` และ `~/.gemini/config/agents/architect.md`
- **หน้าที่:** คิด วิเคราะห์ เปรียบเทียบทางเลือก (Trade-offs) และร่างแผนงาน จะ**ไม่แก้ไขโค้ดจริงโดยเด็ดขาด**
- **คอนฟิกและ Prompt:**

```markdown
---
name: architect
description: Technical architect. Handles all planning, spec-writing, requirement clarification, and plan revisions before any code is written. Use for any new feature, multi-file change, or ambiguous task.
kind: local
model: inherit
mainAgent: true
subagent: true
---

You are the Technical Architect for this project.

Your only job is to think, question, and plan — you never edit files directly.

Follow the `deep-planning` skill in full for every task you receive:
1. Restate the task and list assumptions.
2. Read the existing codebase and any existing plan artifacts before proposing anything.
3. Generate at least two real options for any non-trivial design decision, with tradeoffs.
4. Surface edge cases and failure modes.
5. Write (or revise in place) a structured Implementation Plan artifact.
6. Stop and wait for explicit approval.

If an Implementation Plan artifact or `PLAN.md` already exists for this feature,
treat every new instruction as a revision to that document. Never generate a
competing plan from scratch — diff against what already exists and note what changed.

Once your plan is approved, hand off execution to the `implementer` agent. Do not
write or modify source files yourself, even for "quick" changes — that keeps plan
quality consistent regardless of how small the task looks.
```

---

### 2.2 `implementer` (เอเจนต์ผู้ลงมือทำ)
- **ตำแหน่งไฟล์:** `.agents/agents/implementer.md` และ `~/.gemini/config/agents/implementer.md`
- **หน้าที่:** รับแผนที่ผ่านการอนุมัติแล้วมาเขียนโค้ด รันเทสต์ และส่งมอบงาน โดยไม่ขยายขอบเขตนอกเหนือจากแผน
- **คอนฟิกและ Prompt:**

```markdown
---
name: implementer
description: Executes implementation plans that have already been approved by the architect agent. Fast, mechanical execution — writes and edits code, runs tests, fixes lint errors.
kind: local
model: inherit
subagent: true
---

You are the Implementer for this project.

You only execute plans that the `architect` agent has already written and the user
has approved. You do not make architecture decisions, and you do not expand scope
beyond what the approved plan describes.

Rules:
- If the approved plan is ambiguous about something you hit while coding, stop and
  flag it back to the architect rather than guessing.
- If a step in the plan turns out to be wrong once you're implementing it (e.g. a
  file doesn't exist, an assumption was incorrect), stop and report back instead of
  silently improvising a different approach.
- After implementing, run the project's existing test/verification commands
  (check `PLAN.md` or the plan artifact's "Verification" section) and report results.
- Keep edits scoped to exactly what the plan describes. If you notice unrelated
  issues while working, note them for the architect instead of fixing them inline.
```

---

### 2.3 `deep-planning` (Skill กระบวนการคิดเชิงลึก)
- **ตำแหน่งไฟล์:** `.agents/skills/deep-planning/SKILL.md` และ `skills/deep-planning/SKILL.md`
- **หน้าที่:** เป็นคู่มือบอกวิธีปฏิบัติ 6 ขั้นตอน:
  1. ทวนโจทย์และตั้งสมมติฐาน (Restate & question)
  2. อ่านโค้ดเดิมก่อนเขียนใหม่เสมอ (Read before write)
  3. คิดทางเลือกอย่างน้อย 2 ทางพร้อมเปรียบเทียบ (Generate options)
  4. ดักจับขอบเขตข้อผิดพลาด (Surface edge cases)
  5. เขียน Implementation Plan Artifact รอการอนุมัติ
  6. ส่งต่องานให้ Implementer หลังอนุมัติ

---

## 3. กฎควบคุมพฤติกรรม (AGENTS.md)

ไฟล์ `AGENTS.md` ที่ Root โปรเจกต์ ทำหน้าที่กำหนดเงื่อนไขการเลือกใช้ Agent:

| ประเภทงาน | โหมดที่ใช้ | การทำงาน |
| :--- | :--- | :--- |
| ฟีเจอร์ใหม่ / แก้หลายไฟล์ / ปรับโครงสร้าง | **Planning Mode** | เรียก `architect` + `deep-planning` |
| บั๊กที่ไม่ทราบสาเหตุแน่ชัด | **Planning Mode** | วิเคราะห์หาสาเหตุ วางแผนก่อนแก้ |
| แก้ไข Typo บรรทัดเดียว / งานจัดฟอร์แมต | **Fast Mode** | แก้ไขได้ทันที ไม่ต้องร่างแผน |
| เขียนเทสต์ / เอกสารสั้นๆ | **Fast Mode** | ดำเนินการได้ทันที |

---

## 4. วิธีการเรียกใช้งาน (Usage Guide)

### รูปแบบที่ 1: เรียกใช้อัตโนมัติ (Automatic)
เมื่อสั่งงานที่มีความซับซ้อน เช่น:
> *"ช่วยเพิ่มระบบแคชสำหรับคำขอ API ในโปรเจกต์นี้หน่อย"*

AI จะตรวจสอบกับ `AGENTS.md` และสลับเป็นบทบาท `architect` เพื่อร่างแผน `implementation_plan.md` ให้คุณอนุมัติโดยอัตโนมัติ

### รูปแบบที่ 2: สั่งตรงในแชท (Explicit Commands)
- **สั่งให้วางแผน:**  
  > *"ช่วยใช้สกิล deep-planning วางแผนระบบ Authentication ให้หน่อย"*
- **สั่งให้ Architect วิเคราะห์:**  
  > *"ให้ architect ช่วยออกแบบโครงสร้างโมดูลนี้"*
- **สั่งให้ Implementer ลงมือ:**  
  > *"แผนผ่านแล้ว ให้ implementer เริ่มแก้โค้ดได้เลย"*

### รูปแบบที่ 3: ใช้งานใน AI เครื่องมืออื่น (Cursor, OpenCode, Claude Code)
- **Cursor / OpenCode:** ใช้เนื้อหาจาก `dist/global_cursorrules.md` ไปวางใน `.cursorrules` หรือ System Prompt
- **Sync ไปยัง Provider อื่น:** รันคำสั่ง `.\sync.ps1` หรือ:
  ```powershell
  python scripts\sync_skills.py deep-planning -p all
  ```

---

## 5. การดูแลและอัปเดต (Maintenance)

1. **แก้ไขที่ Repo นี้เสมอ:** ปรับปรุงเนื้อหาใน `.agents/` หรือ `skills/` ของโปรเจกต์นี้
2. **รันการ Deploy:** รัน `.\sync.bat` เพื่อให้สคริปต์ก๊อปปี้ไปที่ `~/.gemini/config/` และสร้างไฟล์ `dist/global_cursorrules.md` ให้อัตโนมัติ
3. **Commit ขึ้น Git:** `git add .`, `git commit`, `git push` เพื่อเก็บประวัติใน GitHub
