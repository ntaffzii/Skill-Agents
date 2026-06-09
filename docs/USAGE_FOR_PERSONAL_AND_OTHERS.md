# Usage Guide For Personal And Shared Use

คู่มือนี้อธิบายวิธีใช้ `Skill-Agents` ทั้งสำหรับเจ้าของ repo และคนอื่นที่ clone/fork ไปใช้เอง

## แนวคิดสั้น ๆ

```text
Skills     = วิธีคิด กฎ และความเชี่ยวชาญของ agent
Workflows  = ลำดับงาน เช่น daily plan, review PR, sync notes
MCP Tools  = เครื่องมือที่ agent ใช้ลงมือทำจริง
Toolsets   = ชุดเครื่องมือที่เหมาะกับงานแต่ละประเภท
```

เวลาคุยกับ AI ให้เรียก `workflow` หรือ `skill` เป็นหลัก แล้วให้ agent เลือก tools เอง

ตัวอย่าง:

```text
Use daily-personal-agent. Build today's plan from Obsidian, Notion, memory, calendar, inbox, and open issues. Draft only. Do not send or apply anything.
```

## สำหรับเจ้าของ Repo

### 1. ติดตั้ง MCP tools

```powershell
cd C:\Users\natth\Documents\Skill-Agents\mcp-tools
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
playwright install chromium
```

### 2. ตั้งค่า token เฉพาะที่ใช้จริง

ดูตัวอย่างจาก `.env.example`

เริ่มต้นแนะนำแค่นี้:

```powershell
$env:NOTION_TOKEN="..."
$env:GITHUB_TOKEN="..."
$env:FIGMA_TOKEN="..."
```

เพิ่มเมื่อใช้จริง:

```powershell
$env:SLACK_BOT_TOKEN="..."
$env:POSTGRES_DSN="..."
$env:FIRECRAWL_API_KEY="..."
```

อย่าใส่ token จริงใน GitHub

### 3. เชื่อม MCP client

ตัวอย่าง Claude Desktop:

```json
{
  "mcpServers": {
    "ai-desk-tools": {
      "command": "C:\\Users\\natth\\Documents\\Skill-Agents\\mcp-tools\\.venv\\Scripts\\python.exe",
      "args": [
        "C:\\Users\\natth\\Documents\\Skill-Agents\\mcp-tools\\server.py"
      ]
    }
  }
}
```

สำหรับ client อื่น หลักการเหมือนกัน:

```text
command = python ใน .venv
args    = path ไปที่ mcp-tools/server.py
env     = token ที่ต้องใช้
```

### 4. ติดตั้งหรือชี้ Skills

ถ้า agent รองรับ skills โดยตรง ให้ copy skill folder:

```powershell
Copy-Item -Recurse .\skills\* "$env:USERPROFILE\.codex\skills\"
```

หรือ Claude Code:

```powershell
Copy-Item -Recurse .\skills\* "$env:USERPROFILE\.claude\skills\"
```

ถ้า provider ไม่รองรับ skill โดยตรง ให้เปิดไฟล์ `SKILL.md` แล้ววางเป็น project instruction/system prompt

## สำหรับคนอื่นที่ Clone/Fork Repo นี้

### 1. Fork หรือ clone

```bash
git clone https://github.com/<owner>/<repo>.git
cd <repo>
```

### 2. อ่านคู่มือหลัก

เริ่มจาก:

```text
docs/PROJECT_GUIDE.md
docs/DAILY_USAGE.md
docs/TOOLS_INVENTORY.md
```

### 3. เปลี่ยนข้อมูลส่วนตัว

ควรแก้:

- path ใน MCP config
- token/env ของตัวเอง
- skill ใน `skills/personal/`
- preference ใน `skills/personal/boomz-preferences/` ถ้าไม่ใช่เจ้าของเดิม
- ชื่อ repo ใน README หาก publish เป็นของตัวเอง

### 4. ใช้เฉพาะส่วนที่ต้องการ

ถ้าต้องการแค่ skills:

```text
ใช้เฉพาะ skills/, Skill.md/, workflows/, docs/
```

ถ้าต้องการ tools:

```text
ติดตั้ง mcp-tools/ และเชื่อม MCP client
```

ถ้าต้องการ local agent:

```text
อ่าน Skill.md/ เป็น instruction กลาง
อ่าน skills/**/SKILL.md ตามงาน
เชื่อม mcp-tools/server.py ผ่าน MCP
```

## วิธีใช้กับ Provider ต่าง ๆ

### Codex / Claude Code ที่รองรับ Skills

โครงสร้างต้องเป็น:

```text
skill-name/
  SKILL.md
```

สั่ง:

```text
Use personal-agent-workflow.
```

หรือ:

```text
Use ship-feature workflow.
```

### Claude Desktop / MCP Client

ใช้ MCP tools ผ่าน config แล้วเรียก skill/workflow ใน prompt:

```text
Use personal-knowledge-sync. Treat Obsidian as source of truth. Use MCP tools if available. Draft Notion payloads only.
```

### ChatGPT / Gemini / Provider ที่ไม่มี Skill Loader

ใช้วิธี manual instruction:

```text
You are using this skill:

<paste SKILL.md>

Task:
<user task>
```

หรือใช้ portable skills ใน `Skill.md/`:

```text
Use universal-agent-operating-system and tool-agnostic-mcp-routing. Select the right capability by task, not by exact tool name.
```

### Local LLM / Local Agent

ให้ agent loader ทำแบบนี้:

```text
1. ใช้ skill-runtime.route_request ถ้ามี MCP tools
2. ถ้า prompt ไม่ชัด ใช้ prompt_improver ก่อน
3. โหลดเฉพาะ workflow และ SKILL.md ที่ route เลือก
4. ใช้ toolset ที่ runtime แนะนำ
5. เรียก MCP tools ตาม workflow
6. ตอบพร้อม verification และ safety boundary
```

ไม่ต้องผูก skill กับชื่อ model เช่น GPT, Claude, Gemini, Llama หรือ Qwen

## Prompt สูตรใช้งาน

ใช้สูตรนี้:

```text
Use <workflow or skill>.
Use <toolset> if available.
Goal: <สิ่งที่ต้องการ>
Context: <ข้อมูล/ไฟล์/แหล่งข้อมูล>
Constraints: <ข้อห้าม>
Output: <รูปแบบผลลัพธ์>
```

ตัวอย่าง:

```text
Use daily-personal-agent.
Use personal-daily-agent toolset if available.
Goal: Build today's plan from Obsidian, Notion, memory, calendar, inbox, chat, and open issues.
Constraints: Draft only. Do not send messages, update Notion, or create issues.
Output: Today plan, meetings, actions, draft replies, notes to save.
```

## งานส่วนตัวที่แนะนำให้ใช้ทุกวัน

### Daily Plan

```text
Use daily-personal-agent. Build today's plan from my Obsidian notes, Notion context, memory, calendar, inbox, chat, finance watchlist, and open issues. Draft replies but do not send anything.
```

### Obsidian To Notion

```text
Use personal-knowledge-sync. Treat Obsidian as source of truth. Draft Notion payloads only and preserve tags, wikilinks, aliases, and source paths.
```

### Inbox And Meeting Triage

```text
Use inbox-meeting-triage. Summarize these emails, calendar events, and chat messages into actions, meeting notes, and draft replies. Do not send anything.
```

### Finance Research

```text
Use finance-research. Summarize my watchlist with quotes, crypto prices, public news, risk notes, provider, timestamp, and currency. This is not financial advice.
```

### Code Work

```text
Use ship-feature. Inspect docs, repo index, tests, CI, and git before editing. Verify with the narrowest test and summarize changed files.
```

### Review

```text
Use review-pr. Inspect the diff and related files. Report findings first with severity, file, and line reference.
```

### Browser/UI

```text
Use design-frontend. Inspect Figma, map the current page, run Playwright checks, and list implementation gaps.
```

## Safety Rules สำหรับคนใช้

- ใส่คำว่า `Draft only` เมื่อเกี่ยวกับ email, chat, Notion, issue tracker
- ใส่คำว่า `Read-only` เมื่อเกี่ยวกับ database หรือ private workspace
- ให้ Obsidian เป็น source of truth ถ้ายังไม่มั่นใจเรื่อง sync
- อย่าให้ agent ส่งอีเมล โพสต์ข้อความ หรือสร้าง issue อัตโนมัติในช่วงแรก
- ตรวจ payload/script ก่อนรันเองเสมอ
- อย่า commit token, `.env`, screenshot ที่มี secret หรือ private content

## วิธี Validate หลังแก้ไข

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\validate-all.ps1
```

ถ้าต้องระบุ Python:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\validate-all.ps1 -Python 'C:\path\to\python.exe'
```

ควรผ่าน:

```text
tools registry
toolsets
workflows
skills
portable skills
python syntax
unit tests
```

## ถ้าจะ Publish เป็นของตัวเอง

แก้ก่อน publish:

- README install command ให้เป็น repo ของตัวเอง
- `NOTICE.md` คงเครดิตไว้
- `skills/personal/` ลบหรือปรับข้อมูลส่วนตัว
- `.env.example` เก็บเฉพาะชื่อ env ไม่ใส่ค่า
- ตรวจ `SECURITY.md`
- รัน validation

ตัวอย่าง install command หลัง publish:

```bash
npx skills add your-github-user/your-skill-repo
```

อย่าใส่ repo คนอื่น เว้นแต่ต้องการติดตั้งของเขาจริง ๆ
