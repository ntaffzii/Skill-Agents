# วิธีใช้งาน Skill-Agents จริง (คู่มือฉบับละเอียด หลังทดสอบแล้ว)

อ้างอิงจากเนื้อหาจริงใน `QUICKSTART.md`, `docs/DAILY_USAGE.md`, `docs/USAGE_FOR_PERSONAL_AND_OTHERS.md` ของ repo คุณ + ผลทดสอบจริงที่ทำไปก่อนหน้า

## 0. โครงสร้างที่ต้องเข้าใจก่อน

```
skills/      = วิธีคิด/กฎ/มาตรฐาน (ไฟล์ SKILL.md ล้วน ใช้งานได้ทันที ไม่ต้องติดตั้งอะไร)
workflows/   = ลำดับงาน ผูกหลาย skill เข้าด้วยกัน (เช่น ship-feature, debug-regression)
mcp-tools/   = โค้ดเครื่องมือจริง (อยู่คนละ repo: ai-desk-tools) ต้องติดตั้งแยก
data/*.json  = registry เชื่อม skill ↔ workflow ↔ tool เข้าด้วยกัน
```

จุดสำคัญที่ทดสอบแล้ว: **ใช้แค่ `skills/` และ `workflows/` ก็ทำงานได้เต็มที่แล้ว** โดยไม่ต้องมี `mcp-tools`/`ai-desk-tools` เลย เพราะ skill ถูกออกแบบให้ไม่ hardcode ชื่อ tool ตายตัว — ถ้าไม่มี MCP tool มันแค่ทำงานแบบ manual/draft แทน (เช่น `diagnose`/`tdd` ใช้ terminal ธรรมดาก็รันได้ตามที่ทดสอบไปแล้ว)

มี 2 ระดับการใช้งาน เลือกตามที่ต้องการ:

## วิธีที่ 1: ใช้แค่ Skills + Workflows (ไม่ต้องติดตั้งอะไรเพิ่ม) — แนะนำเริ่มจากตรงนี้

### กับ Claude Code (CLI)

```powershell
Copy-Item -Recurse .\skills\* "$env:USERPROFILE\.claude\skills\"
```

จากนั้นในการคุยกับ Claude Code พิมพ์ตรงๆ:

```text
Use code-review. Review the diff in src/cart.py.
```
```text
Use diagnose. This test is failing: <paste error/log>. Find root cause before fixing.
```
```text
Use tdd. Implement a function that validates email format. Red-green-refactor.
```

### กับ Codex-style client

```powershell
Copy-Item -Recurse .\skills\* "$env:USERPROFILE\.codex\skills\"
```

### กับ Cowork mode (ที่กำลังคุยอยู่ตอนนี้)

Cowork มีระบบ skill ของตัวเอง (ติดตั้งผ่าน Settings > Capabilities) ไม่ได้อ่านโฟลเดอร์ `~/.claude/skills` แบบเดียวกับ Claude Code CLI โดยตรง วิธีที่ใช้ได้จริงใน Cowork ตอนนี้คือ **วาง `SKILL.md` เป็นคำสั่งในแชท** เช่น

```text
ทำตามคำสั่งนี้:
<paste เนื้อหาทั้งหมดใน skills/engineering/diagnose/SKILL.md>

งาน: <ปัญหาที่เจอจริง>
```

หรือถ้าอยากให้ผมช่วยแบบไม่ต้อง paste ทุกครั้ง สามารถบอกผมได้เลยว่า "ทำงานนี้แบบ diagnose skill" แล้วอธิบายบริบท ผมจะทำตาม workflow เดียวกับที่ทดสอบให้ดูไปแล้ว (reproduce → minimize → hypothesize → instrument → fix → verify)

### กับ ChatGPT / Gemini / provider อื่นที่ไม่รองรับ skill loader

Paste `SKILL.md` เป็น system prompt/instruction ตรงๆ ตามที่ `docs/USAGE_FOR_PERSONAL_AND_OTHERS.md` แนะนำ หรือใช้ `Skill.md/universal-agent-operating-system` + `Skill.md/tool-agnostic-mcp-routing` เป็น instruction กลางที่ portable ข้าม provider

## วิธีที่ 2: ใช้เต็มระบบ พร้อม MCP Tools จริง (ต้องมี ai-desk-tools)

ทำบนเครื่อง Windows ของคุณเอง (ไม่ใช่ใน Cowork sandbox เพราะ Cowork ไม่ใช่ MCP client ที่รัน stdio server ของคุณเองได้):

```powershell
git clone https://github.com/ntaffzii/ai-desk-tools.git
cd ai-desk-tools
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
playwright install chromium   # ถ้าจะใช้ browser/Playwright tools
```

ตั้ง token เท่าที่ใช้จริงก่อน (ดูตัวเต็มใน `.env.example`):

```powershell
$env:NOTION_TOKEN="..."
$env:GITHUB_TOKEN="..."
$env:FIGMA_TOKEN="..."
```

เชื่อมกับ Claude Desktop — แก้ path ให้ตรงเครื่องจริง:

```json
{
  "mcpServers": {
    "ai-desk-tools": {
      "command": "C:\\Users\\natth\\Documents\\ai-desk-tools\\.venv\\Scripts\\python.exe",
      "args": ["C:\\Users\\natth\\Documents\\ai-desk-tools\\server.py"]
    }
  }
}
```

**อย่า commit token จริงลง GitHub** — ใช้ `.env.example` เป็นแค่ template

### 💡 ข้อควรระวังเรื่องสภาพแวดล้อม Python (Virtual Environment)
หากคุณพบข้อผิดพลาด `ModuleNotFoundError: No module named 'mcp'` แสดงว่าคุณกำลังใช้ Python ตัวหลักของเครื่อง (Global Python) แทนที่จะใช้ตัวที่ติดตั้งแพ็กเกจไว้ใน Virtual Environment (`.venv`)
* **วิธีแก้ไขในการรันแบบใช้คำสั่งเดี่ยว**: ให้เรียกใช้ Python Path ของ `.venv` โดยตรง เช่น:
  ```powershell
  # รัน server
  .\mcp-tools\.venv\Scripts\python.exe .\mcp-tools\server.py
  # รัน portal
  .\mcp-tools\.venv\Scripts\python.exe .\mcp-tools\run_portal.py
  ```
* **วิธีแก้ไขโดยเปิดใช้งาน Environment**:
  ```powershell
  cd mcp-tools
  .\.venv\Scripts\Activate.ps1
  python server.py
  ```

### 🖥️ การจัดการผ่าน Web Portal (เลือกเปิด/ปิดเครื่องมือเพื่อลด Token)
เพื่อลด Context Bloat และประหยัดจำนวน Token ที่จะส่งไปยัง LLM (ลดจากประมาณ ~90,000 tokens เหลือเพียง ~10,000 tokens) คุณสามารถใช้ Web Portal เพื่อควบคุมได้ดังนี้:

1. **รันตัว Web Portal Server**:
   ```powershell
   # ใช้ python จาก .venv รันสคริปต์
   .\mcp-tools\.venv\Scripts\python.exe .\mcp-tools\run_portal.py
   ```
2. **เข้าใช้งาน Dashboard**:
   * เปิดเบราว์เซอร์ไปที่ [http://localhost:8000](http://localhost:8000)
   * คุณจะพบหน้า Dashboard ที่แสดงจำนวน Token สะสม
3. **ปรับแต่งเครื่องมือ**:
   * **เลือก Preset Toolsets**: เช่น เลือก `Coding Basic` เพื่อเปิดเฉพาะกลุ่มเครื่องมือสำหรับเขียนโค้ดทั่วไป
   * **เลือกแบบเจาะจง (Custom)**: สามารถคลิกเปิด/ปิดการโหลดรายกลุ่มเครื่องมือ (Tool Groups) ได้ด้วยตนเอง
   * คลิกปุ่ม **Save Config** ที่ด้านล่าง ระบบจะเซฟการตั้งค่าไว้ที่ [active_config.json](file:///e:/Dev/Projects/project-work/agents-llm-github/skill-agents/mcp-tools/config/active_config.json)
4. **รีสตาร์ทตัว Client**:
   * ในการเปลี่ยนเครื่องมือ เนื่องจาก Client อย่าง Claude Desktop จะจำสารบัญเครื่องมือเฉพาะตอนเปิดรันครั้งแรกเท่านั้น
   * เมื่อเซฟค่าบนหน้าเว็บแล้ว ให้ทำการ **Restart Connection** ใน Claude Desktop (หรือปิดแอปพลิเคชันให้สนิทแล้วเปิดใหม่) เพื่อให้ระบบอัปเดตเครื่องมือเซ็ตล่าสุดเข้าไปยัง LLM

---


## 1. สูตร Prompt ที่ใช้ได้จริง (ยิ่งชัดยิ่งดี)

```text
Use <workflow หรือ skill>.
Use <toolset> if available.
Goal: <สิ่งที่ต้องการ>
Context: <ไฟล์/ข้อมูลที่เกี่ยวข้อง>
Constraints: <ข้อห้าม>
Output: <รูปแบบผลลัพธ์ที่ต้องการ>
```

ตัวอย่างจริงที่ผ่านการ cross-check แล้วว่าชื่อ skill/workflow ตรงกับที่มีอยู่จริงใน repo:

| ต้องการทำอะไร | Prompt |
|---|---|
| แก้บั๊ก | `Use debug-regression. Reproduce first with diagnose, then prove with a regression test before fixing.` |
| รีวิวโค้ด/PR | `Use review-pr. Report findings first with severity, file, and line reference.` |
| เขียนฟีเจอร์ใหม่ | `Use ship-feature. Inspect docs, tests, and git before editing. Verify with the narrowest test.` |
| ทำ UI/frontend | `Use build-ui. Implement, then verify with browser/Playwright checks across viewports.` |
| จัดระเบียบ Obsidian vault | `Use obsidian-vault-workflow. Organize these notes, preserve tags and wikilinks.` |
| Sync Obsidian → Notion | `Use personal-knowledge-sync. Treat Obsidian as source of truth. Draft Notion payloads only.` |
| แผนงานประจำวัน | `Use daily-personal-agent. Draft replies but do not send anything.` |
| ปรับปรุง prompt ที่เขียนไม่ชัด | `Use prompt-improvement. Rewrite this prompt: <วาง prompt เดิม>` |
| สร้าง skill ใหม่ | `Use create-new-skill workflow with skill-management skill.` |

## 2. กฎความปลอดภัยที่ repo กำหนดไว้ (ควรทำตามจริง)

- ใส่คำว่า **"Draft only"** เวลาให้ agent แตะ email/chat/Notion/issue tracker — อย่าให้ auto-send
- ใส่คำว่า **"Read-only"** เวลาถามเรื่อง database หรือ private workspace
- ให้ Obsidian เป็น source of truth ถ้ายังไม่มั่นใจเรื่อง sync กับ Notion
- ตรวจ payload/script ที่ agent generate ก่อนรันเองเสมอ (โดยเฉพาะจาก `user-runner`)
- อย่า commit token, `.env`, หรือ screenshot ที่มีข้อมูล private

## 3. เช็คสุขภาพ repo หลังแก้ไขทุกครั้ง

จากเครื่องที่มีทั้ง `Skill-Agents` และ `ai-desk-tools` (หรือ mcp-tools อยู่ใต้ root เดียวกัน):

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\validate-all.ps1
```

ถ้ามีแค่ `Skill-Agents` เดี่ยวๆ (ไม่มี `mcp-tools`) ให้รันเฉพาะส่วน skill แทน (ตัวที่จับบั๊กจริงได้ต้องเสริม YAML check เอง เพราะ `validate-skills.ps1` ใช้ regex หลวมๆ ไม่ใช่ YAML parser จริง):

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\validate-skills.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\validate-skills.ps1 -Root Skill.md
python -c "import yaml,glob; [yaml.safe_load(open(f,encoding='utf-8').read().split('---')[1]) for f in glob.glob('skills/**/SKILL.md', recursive=True)]; print('OK')"
```

## 4. ข้อควรระวังจากการทดสอบจริง (กันบั๊กเดิมเกิดซ้ำตอนเพิ่ม skill ใหม่)

- เวลาเขียน `description:` ใน frontmatter ใหม่ **ถ้ามี `:` ตามด้วยช่องว่างอยู่กลางประโยค ต้องใส่ quote ครอบทั้งข้อความ** ไม่งั้น YAML parser เข้มงวด (Claude Code, gray-matter ฯลฯ) จะ parse พัง — นี่คือบั๊กที่เจอและแก้ไปแล้วใน `skill-management` กับ `obsidian-vault-workflow`
- ตั้งชื่อ `name:` ใน frontmatter ให้ตรงกับชื่อโฟลเดอร์เสมอ เพื่อให้ auto-discovery ของ client ต่างๆ หาเจอ
- ก่อนเพิ่ม skill ใหม่ ให้ใช้ `mcp-tool-management`/`skill-management` skill ช่วยตัดสินว่าควรเป็น skill, workflow, หรือ tool

## 5. สรุปเส้นทางเริ่มใช้งานที่เร็วที่สุด

1. ถ้าอยากใช้ตอนนี้เลยใน Cowork → paste เนื้อหา `SKILL.md` ที่ต้องการ หรือบอกผมตรงๆ ว่าจะใช้ skill ไหนกับงานอะไร
2. ถ้าใช้ Claude Code CLI ที่เครื่อง → `Copy-Item -Recurse .\skills\* "$env:USERPROFILE\.claude\skills\"` แล้วพิมพ์ `Use <skill-name>`
3. ถ้าอยากได้ tool จริง (แก้ไฟล์/รัน test/เรียก API อัตโนมัติ) → ติดตั้ง `ai-desk-tools` แยก แล้วเชื่อมผ่าน Claude Desktop config
