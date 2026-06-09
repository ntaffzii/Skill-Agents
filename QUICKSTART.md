# Quickstart

เริ่มใช้ `Skill-Agents` ภายในไม่กี่นาที

## 1. ติดตั้ง MCP Tools

```powershell
cd C:\Users\natth\Documents\Skill-Agents\mcp-tools
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

ถ้าจะใช้ browser/Playwright:

```powershell
playwright install chromium
```

## 2. รัน MCP Server

แบบ stdio ใช้กับ Claude Desktop/local MCP client:

```powershell
python .\server.py
```

แบบ HTTP ใช้กับ local agent หรือ MCP client ที่รองรับ HTTP:

```powershell
python .\server_http.py --host 127.0.0.1 --port 8765
```

## 3. ตั้งค่า Token ที่ต้องใช้

เริ่มจากตัวที่ใช้จริง:

```powershell
$env:NOTION_TOKEN="..."
$env:GITHUB_TOKEN="..."
$env:FIGMA_TOKEN="..."
```

ตัวอื่นดูใน `.env.example`

อย่า commit token จริงลง GitHub

## 4. เชื่อม Claude Desktop ตัวอย่าง

ใส่ config แนวนี้ โดยแก้ path ให้ตรงเครื่องของคุณ:

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

ดูตัวอย่างเต็มใน `examples/claude-desktop-config.json`

สำหรับ LM Studio ให้ใช้ตัวอย่างใน `examples/lm-studio-mcp-config.json` แล้วใส่ใน `Program > Install > Edit mcp.json`

## 5. ใช้ Prompt แรก

Daily plan:

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

## 6. Validate

จาก repo root:

```powershell
cd C:\Users\natth\Documents\Skill-Agents
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\validate-all.ps1
```

ถ้า Python ไม่อยู่ใน PATH:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\validate-all.ps1 -Python 'C:\path\to\python.exe'
```

## 7. อ่านต่อ

- `docs/PROJECT_GUIDE.md` - คู่มือโปรเจกต์ทั้งหมด
- `docs/USAGE_FOR_PERSONAL_AND_OTHERS.md` - วิธีใช้ส่วนตัวและให้คนอื่นใช้
- `docs/MCP_API_SERVER.md` - วิธีรัน HTTP MCP server
- `docs/SKILL_RUNTIME_FLOW.md` - วิธีให้ local LLM route skill/workflow โดยไม่อ่านทุกไฟล์
- `docs/LOCAL_LLM_SETTINGS.md` - ค่า context, temperature, max tokens, RAG chunk สำหรับ local LLM
- `docs/PROMPT_IMPROVER_LOCAL_MODEL.md` - วิธีใช้ prompt improver กับ LM Studio/Ollama/local model
- `docs/CONFIG_JSON_GUIDE.md` - วิธีใช้ `config.json` สำหรับ provider/model presets
- `docs/TOOLS_INVENTORY.md` - รายชื่อ tools/toolsets ทั้งหมด
