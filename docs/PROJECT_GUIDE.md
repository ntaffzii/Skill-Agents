# Project Guide ภาษาไทย

คู่มือนี้สรุปโปรเจกต์ `Skill-Agents` ทั้งหมดที่เราสร้างไว้: มันคืออะไร โครงสร้างทำงานอย่างไร เชื่อม MCP อย่างไร และใช้งานกับ Obsidian, Notion, GitHub, Figma, Browser, Finance, Memory/RAG, Email, Calendar และเครื่องมือส่วนตัวอื่น ๆ อย่างไร

## ภาพรวม

โปรเจกต์นี้คือ personal AI agent operating system สำหรับใช้งานส่วนตัวและงานวิศวกรรม โดยแบ่งเป็น 4 ส่วนหลัก:

```text
skills/      = วิธีคิดและกฎการทำงานของ agent
workflows/   = ลำดับงานแบบ playbook
mcp-tools/   = เครื่องมือที่ agent เรียกใช้ผ่าน MCP
data/        = registry ของ tools, toolsets, workflows
```

แนวคิดสำคัญ:

- `Skill` บอก agent ว่า “ควรทำงานแบบไหน”
- `Workflow` บอก agent ว่า “ควรทำอะไรก่อนหลัง”
- `Tool` ให้ agent “ลงมือทำจริง”
- `Toolset` รวม tool ที่เหมาะกับงานแต่ละประเภท เพื่อลดความรก

## สถานะปัจจุบัน

```text
52 tool groups
13 toolsets
9 workflows
24 local skills
4 portable Skill.md
150 tests
```

## โครงสร้างโปรเจกต์

```text
Skill-Agents/
  README.md
  CONTRIBUTING.md
  SECURITY.md
  LICENSE
  .env.example
  data/
    tools.json
    toolsets.json
    workflows.json
  docs/
    PROJECT_GUIDE.md
    DAILY_USAGE.md
    TOOLS_INVENTORY.md
    RECOMMENDED_NEXT_TOOLS.md
    WEB_CAPTURE_PROVIDERS.md
    FINANCE_MARKET_PROVIDERS.md
    USER_RUN_WORKFLOWS.md
  workflows/
    ship-feature.md
    debug-regression.md
    review-pr.md
    obsidian-vault-cleanup.md
    create-new-skill.md
    build-mcp-tool.md
    research-report.md
    daily-personal-agent.md
    personal-knowledge-sync.md
  skills/
    engineering/
    research/
    productivity/
    obsidian/
    misc/
    personal/
    in-progress/
    deprecated/
  Skill.md/
    universal-agent-operating-system/
    model-portability-adapter/
    tool-agnostic-mcp-routing/
    cross-model-handoff/
  mcp-tools/
    server.py
    security.py
    tools/
    tests/
    config/tool_policy.json
  scripts/
  user-run-scripts/
```

## การทำงานของระบบ

ลำดับที่ควรคิดเวลาสั่ง agent:

```text
ผู้ใช้สั่งงาน
  -> เลือก workflow
  -> เลือก skill ที่เกี่ยวข้อง
  -> เลือก toolset
  -> เรียก MCP tools
  -> ตรวจสอบผลลัพธ์
  -> สรุป/บันทึก memory/handoff
```

ตัวอย่าง:

```text
Use daily-personal-agent. Build today's plan from calendar, email, Slack/Discord, Notion, Obsidian, memory, and finance watchlist context. Draft replies but do not send anything.
```

Agent ควรเข้าใจว่า:

- workflow คือ `daily-personal-agent`
- toolset คือ `personal-daily-agent`
- skills ที่เกี่ยวข้องคือ `personal-agent-workflow`, `inbox-meeting-triage`, `markdown-report`, `handoff`
- tools ที่เกี่ยวข้องคือ `calendar`, `email-inbox`, `slack-discord`, `notion`, `obsidian-notion-bridge`, `memory-context`, `vector-memory`, `finance-market`

## วิธีติดตั้ง MCP Tools

เข้าโฟลเดอร์ `mcp-tools`:

```powershell
cd C:\Users\natth\Documents\Skill-Agents\mcp-tools
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

ติดตั้ง browser runtime ถ้าจะใช้ Playwright:

```powershell
playwright install chromium
```

ทดสอบ MCP server:

```powershell
python server.py
```

## เชื่อมกับ Claude Desktop หรือ MCP Client

ตัวอย่าง config:

```json
{
  "mcpServers": {
    "ai-desk-tools": {
      "command": "C:\\Users\\natth\\Documents\\Skill-Agents\\mcp-tools\\.venv\\Scripts\\python.exe",
      "args": [
        "C:\\Users\\natth\\Documents\\Skill-Agents\\mcp-tools\\server.py"
      ],
      "env": {
        "NOTION_TOKEN": "ใส่ token ของคุณ",
        "GITHUB_TOKEN": "ใส่ token ของคุณ",
        "FIGMA_TOKEN": "ใส่ token ของคุณ"
      }
    }
  }
}
```

สำหรับ client อื่น หลักการเหมือนกัน:

```text
command = python ใน virtualenv
args    = path ไปที่ mcp-tools/server.py
env     = token/provider config ที่ต้องใช้
```

## Environment Variables

ดูตัวอย่างทั้งหมดได้จาก `.env.example`

เริ่มต้นแนะนำตั้งแค่นี้ก่อน:

```powershell
$env:NOTION_TOKEN="..."
$env:GITHUB_TOKEN="..."
$env:FIGMA_TOKEN="..."
```

ถ้าจะใช้ Slack:

```powershell
$env:SLACK_BOT_TOKEN="..."
```

ถ้าจะใช้ Postgres:

```powershell
$env:POSTGRES_DSN="postgresql://user:pass@localhost:5432/dbname"
```

ถ้าจะใช้ web capture provider:

```powershell
$env:FIRECRAWL_API_KEY="..."
$env:FIRECRAWL_API_URL="..."
```

ถ้าจะใช้ RAG/embedding provider ในอนาคต:

```powershell
$env:EMBEDDINGS_API_URL="..."
$env:EMBEDDINGS_MODEL="..."
$env:EMBEDDINGS_API_KEY="..."
```

อย่า commit token จริงลง GitHub

## วิธีใช้ Skills

Skills อยู่ใน `skills/` และ `Skill.md/`

ตัวอย่าง skill สำคัญ:

- `diagnose` ใช้ debug ปัญหา
- `tdd` ใช้ทำ feature/bug fix แบบ red-green-refactor
- `code-review` ใช้ review code
- `obsidian-vault-workflow` ใช้จัดการ Obsidian vault
- `obsidian-notion-bridge` ใช้แปลง/วางแผน sync ระหว่าง Obsidian กับ Notion
- `personal-agent-workflow` ใช้ daily planning ส่วนตัว
- `inbox-meeting-triage` ใช้จัดการ email/chat/calendar
- `mcp-tool-management` ใช้เพิ่มหรือจัดระเบียบ tools

เรียกใช้ด้วย prompt:

```text
Use obsidian-notion-bridge. Treat Obsidian as source of truth and draft Notion payloads only.
```

```text
Use inbox-meeting-triage. Summarize these emails and messages into action items and draft replies, but do not send anything.
```

## วิธีใช้ Workflows

Workflows อยู่ใน `workflows/`

รายการหลัก:

- `ship-feature` ทำ feature ตั้งแต่ scope -> implement -> test -> handoff
- `debug-regression` หา root cause และแก้ regression
- `review-pr` review diff หรือ PR
- `obsidian-vault-cleanup` จัดระเบียบ Obsidian vault
- `create-new-skill` สร้าง skill ใหม่
- `build-mcp-tool` สร้าง MCP tool ใหม่
- `research-report` ทำรายงาน research แบบมีแหล่งอ้างอิง
- `daily-personal-agent` ทำ daily plan จากข้อมูลส่วนตัว
- `personal-knowledge-sync` sync/วางแผน knowledge ระหว่าง Obsidian, Notion, memory, RAG

ตัวอย่าง prompt:

```text
Use ship-feature. Inspect project, docs, tests, CI, and git before editing. Verify with the narrowest test.
```

```text
Use research-report. Research current AI agent MCP tool patterns and summarize what should be added to this repo.
```

```text
Use personal-knowledge-sync. Convert selected Obsidian notes into Notion payload plans and RAG chunks while preserving tags and wikilinks.
```

## วิธีใช้ Toolsets

Toolsets อยู่ใน `data/toolsets.json`

ใช้เมื่ออยากบอก agent ว่า “งานนี้ควรใช้เครื่องมือกลุ่มไหน”

รายการสำคัญ:

- `coding-basic` งาน code ทั่วไป
- `backend-review` backend/API/database
- `frontend-ui` frontend/browser/Playwright
- `skill-authoring` สร้าง skill/workflow/tool docs
- `safe-maintenance` cleanup/release/security
- `agent-control-plane` ตรวจ registry/policy/audit/runtime
- `finance-research` หุ้น crypto ข่าว finance
- `workspace-integrations` Notion/Obsidian/Slack/Discord/email/calendar
- `design-frontend` Figma -> frontend
- `data-query` Postgres read-only
- `personal-daily-agent` daily plan ส่วนตัว
- `personal-knowledge-rag` notes/memory/RAG
- `task-issue-planning` issue/task planning

ตัวอย่าง prompt:

```text
Use personal-daily-agent toolset. Build today's personal plan from notes, calendar, inbox, chat, memory, and finance watchlist.
```

## Tools สำคัญที่มีแล้ว

### Personal / Workspace

- `notion` อ่าน/search Notion และ draft payload
- `obsidian-notion-bridge` แปลง note/payload ระหว่าง Obsidian กับ Notion
- `calendar` สรุป event, daily plan, meeting prep
- `email-inbox` summarize email, extract action, draft reply
- `slack-discord` summarize message, draft reply, action items
- `issue-tracker` draft issue, parse issue ref, break down task

### Engineering

- `filesystem`
- `repo-index`
- `project`
- `package`
- `api`
- `database`
- `postgres`
- `git`
- `git-control`
- `github-api`
- `validation`
- `security-scanner`

### Browser / UI

- `browser`
- `browser-page-map`
- `playwright`
- `playwright-actions`
- `figma`
- `media`

### Research / Memory / RAG

- `web`
- `web-capture`
- `finance-market`
- `memory`
- `memory-context`
- `vector-memory`
- `rag-adapter`
- `external-mcp-catalog`

## Obsidian กับ Notion ควรใช้แบบไหน

แนะนำให้ใช้แบบนี้:

```text
Obsidian = source of truth ส่วนตัว
Notion   = publish/dashboard/workspace view
Memory   = decision/preference/bug lesson ที่ควรจำ
RAG      = index/search สำหรับข้อมูลเยอะ
```

กฎที่ควรใช้:

- เขียน note จริงใน Obsidian ก่อน
- ให้ AI draft Notion payload เท่านั้น
- review ก่อน apply เอง
- เก็บ Notion page id/url กลับมาใน frontmatter เมื่อจำเป็น
- อย่า auto-sync ทั้ง vault จนกว่าจะมี plan และ backup

ตัวอย่าง:

```text
Use personal-knowledge-sync. Obsidian is source of truth. Inspect this folder, draft Notion payloads, and create a sync checklist. Do not apply changes.
```

## Daily Personal Agent

ใช้สำหรับสรุปวันของคุณจากหลายแหล่ง:

- calendar
- email
- Slack/Discord
- Notion
- Obsidian
- memory
- issue tracker
- finance watchlist

ตัวอย่าง:

```text
Use daily-personal-agent. Build today's plan from my notes, Notion context, calendar, inbox, chat, memory, open issues, and finance watchlist. Draft replies and issue updates, but do not send or apply anything.
```

ผลลัพธ์ควรออกมาเป็น:

```text
Today
Meetings
Inbox/chat actions
Draft replies
Issues/tasks
Notes to save
Waiting on
```

## Finance Research

ใช้ `finance-research` และ `finance-market`

ตัวอย่าง:

```text
Use finance-research. Summarize today's market context for AAPL, NVDA, BTC, and ETH with quotes, public news, and risk notes. This is not financial advice.
```

ข้อควรจำ:

- ใช้เพื่อ research/education
- ไม่ใช่คำแนะนำการลงทุน
- ควรระบุ provider, timestamp, currency
- ข่าวหรือราคาปัจจุบันควรตรวจ web/current source ทุกครั้ง

## Browser และ Playwright

ใช้เมื่อต้องดู UI:

```text
Use frontend-ui. Inspect the page, map interactive elements, run Playwright screenshot, check console/network errors, and summarize UI issues.
```

ลำดับแนะนำ:

```text
browser-page-map -> playwright screenshot -> console/network -> accessibility -> action checks
```

## Git และ GitHub

มี 2 ระดับ:

- `git` read-only เช่น status, diff, log
- `git-control` branch/stage/commit แบบ controlled

ไม่มี push/force push/reset hard เป็นค่าเริ่มต้น เพื่อความปลอดภัย

ตัวอย่าง:

```text
Use review-pr. Inspect git diff, related files, tests, CI, and GitHub metadata. Report findings first.
```

## Safety Model

ระบบนี้ออกแบบให้ปลอดภัยก่อน:

- email/chat/issue/Notion เป็น draft หรือ plan ก่อน
- Postgres อนุญาตเฉพาะ read-only query
- web-capture ไม่ bypass login, captcha, private account, paywall
- Git ไม่มี reset hard, force push, merge, rebase
- command execution ผ่าน policy ใน `mcp-tools/config/tool_policy.json`
- blocked หรือ risky action ควรสร้าง user-run script ให้ผู้ใช้กดเอง

## User-Run Scripts

อยู่ใน `user-run-scripts/`

ใช้เมื่อ sandbox ทำไม่ได้ หรือควรให้ผู้ใช้กดเอง เช่น:

- install dependencies
- install Playwright browser
- split repo ก่อนขึ้น GitHub
- publish repo
- run validation

ตัวอย่าง:

```powershell
.\user-run-scripts\run-validate-all.ps1
```

## Validate โปรเจกต์

รันทั้งหมด:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\validate-all.ps1
```

ถ้า Python ไม่อยู่ใน PATH:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\validate-all.ps1 -Python 'C:\path\to\python.exe'
```

สิ่งที่ตรวจ:

- `data/tools.json`
- `data/toolsets.json`
- `data/workflows.json`
- `skills/**/SKILL.md`
- `Skill.md/**/SKILL.md`
- Python syntax
- MCP tool tests

## เอาขึ้น GitHub

มี 2 ทาง:

### ทางที่ 1: รวม repo เดียว

เหมาะกับใช้งานส่วนตัว:

```text
Skill-Agents/
  skills/
  Skill.md/
  workflows/
  docs/
  mcp-tools/
```

### ทางที่ 2: แยก repo

เหมาะกับ publish/share:

```text
skill-agents/
  skills/
  Skill.md/
  workflows/
  docs/

ai-desk-mcp-tools/
  server.py
  tools/
  tests/
  requirements.txt
```

ใช้ script:

```powershell
.\user-run-scripts\run-github-split.ps1
```

## คำสั่ง Prompt ที่ใช้บ่อย

Daily:

```text
Use daily-personal-agent. Build today's plan from my Obsidian notes, Notion context, calendar, inbox, chat, memory, and open issues. Draft replies but do not send anything.
```

Obsidian/Notion:

```text
Use personal-knowledge-sync. Treat Obsidian as source of truth. Draft Notion payloads only and preserve tags, wikilinks, and source paths.
```

Coding:

```text
Use ship-feature. Inspect docs, repo index, tests, CI, and git before editing. Verify with the narrowest test.
```

Review:

```text
Use review-pr. Inspect the diff and report findings first with file and line references.
```

Research:

```text
Use research-report. Gather current sources, summarize findings, label uncertainty, and produce a Markdown report.
```

Finance:

```text
Use finance-research. Check quotes, crypto prices, and public news for my watchlist. Include provider, timestamp, currency, and not-financial-advice note.
```

Browser/UI:

```text
Use design-frontend. Inspect Figma, map the current page, run Playwright checks, and list implementation gaps.
```

## สิ่งที่ควรทำต่อ

ตอนนี้ระบบพร้อมใช้แล้ว สิ่งที่ควรทำต่อเป็น optional:

1. ตั้งค่า token จริงใน MCP client
2. ใช้ Obsidian เป็น source of truth และทดสอบ `personal-knowledge-sync`
3. ใช้ `daily-personal-agent` ทุกวัน 3-5 วัน แล้วดูว่าต้องปรับ prompt/skill อะไร
4. เพิ่ม live Gmail/Google Calendar reader ถ้าต้องการดึงข้อมูลเองโดยตรง
5. เพิ่ม live Jira/Linear reader ถ้าใช้ issue tracker ทุกวัน
6. เพิ่ม Chroma/SQLite vector store ถ้าข้อมูล note/memory ใหญ่มาก

## สรุป

โปรเจกต์นี้ต่างจาก repo skills ทั่วไปตรงที่มีครบทั้ง:

- skill instructions
- workflow playbooks
- MCP executable tools
- tool registry
- curated toolsets
- safety policy
- personal workspace integrations
- Obsidian/Notion bridge
- browser automation
- finance research
- memory/RAG planning
- GitHub-ready docs and validation

เป้าหมายคือให้ AI agent ของคุณไม่ใช่แค่ตอบคำถาม แต่ทำงานเป็นระบบ รู้ว่าต้องอ่านอะไร ใช้เครื่องมือไหน ตรวจสอบอย่างไร และส่งมอบงานแบบที่คุณควบคุมได้

