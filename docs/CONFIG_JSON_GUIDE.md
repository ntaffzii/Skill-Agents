# Config JSON Guide

คู่มือนี้อธิบายไฟล์ `config.json` กลางสำหรับ local LLM/provider/model settings

## อ่านตรงนี้ก่อน

`config.json` ใน repo นี้เป็นไฟล์ **แนะนำค่าและเก็บ preset กลาง** ไม่ใช่ไฟล์ที่ LM Studio อ่านเองโดยอัตโนมัติ

สิ่งที่ใช้งานจริงมี 3 ชั้น:

```text
config.json
  = ค่าแนะนำ / preset / reference ของโปรเจกต์

LM Studio mcp.json
  = ไฟล์ที่ LM Studio อ่านจริงเพื่อเปิด MCP tools

env ใน mcp.json หรือ PowerShell
  = ค่าที่ mcp-tools ใช้จริง เช่น PROMPT_IMPROVER_API_URL
```

ดังนั้นถ้าคุณตั้งค่าใน `config.json` อย่างเดียว LM Studio จะยังไม่เปลี่ยน ต้องเอาค่าที่ต้องใช้ไปใส่ใน `mcp.json` หรือ environment variable ด้วย

## ไฟล์คืออะไร

`config.json` เป็น template กลางสำหรับบอกว่าโปรเจกต์ควรใช้ provider/model/preset อะไร

รองรับ:

- LM Studio
- Ollama
- llama.cpp server
- vLLM
- OpenAI-compatible remote endpoint
- OpenAI
- Anthropic
- Gemini
- OpenRouter
- Groq
- Together
- Fireworks
- Mistral
- custom OpenAI-compatible endpoint
- prompt improver
- skill runtime
- RAG/chunk settings
- MCP stdio/HTTP settings

ไฟล์นี้ไม่ควรใส่ token จริง ให้ใช้ environment variables แทน

## config.json เกี่ยวกับ mcp.json ยังไง

ให้คิดแบบนี้:

```text
config.json = สมุดจดค่าแนะนำ
mcp.json    = config ที่ client ใช้รัน MCP จริง
```

ตัวอย่างใน `config.json`:

```json
{
  "active_provider": "lm-studio",
  "active_model": "LFM2.5-8B-A1B"
}
```

แปลว่าเราควรตั้งค่าใน `mcp.json` เป็น:

```json
{
  "env": {
    "PROMPT_IMPROVER_API_URL": "http://localhost:1234/v1/chat/completions",
    "PROMPT_IMPROVER_MODEL": "LFM2.5-8B-A1B"
  }
}
```

LM Studio จะไม่ไปอ่าน `config.json` เอง ต้อง copy ค่าไปใส่ใน `mcp.json`

## ขั้นตอนใช้งานสำหรับมือใหม่

### Step 1: เปิด config.json

เปิดไฟล์:

```text
config.json
```

ดู 2 ค่านี้:

```json
{
  "active_provider": "lm-studio",
  "active_model": "LFM2.5-8B-A1B"
}
```

ความหมาย:

```text
ใช้ LM Studio เป็น provider
ใช้ LFM2.5-8B-A1B เป็นโมเดลแนะนำสำหรับ prompt improver
```

### Step 2: เปิด LM Studio

ใน LM Studio:

```text
Program
-> Install
-> Edit mcp.json
```

ถ้าเห็น:

```json
{
  "mcpServers": {}
}
```

ให้ใส่ `ai-desk-tools` เข้าไป

### Step 3: ใส่ MCP config

สำหรับเริ่มต้นแบบไม่มี token:

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

ถ้าจะใช้ prompt improver กับ LM Studio local model:

```json
{
  "mcpServers": {
    "ai-desk-tools": {
      "command": "C:\\Users\\natth\\Documents\\Skill-Agents\\mcp-tools\\.venv\\Scripts\\python.exe",
      "args": [
        "C:\\Users\\natth\\Documents\\Skill-Agents\\mcp-tools\\server.py"
      ],
      "env": {
        "PROMPT_IMPROVER_API_URL": "http://localhost:1234/v1/chat/completions",
        "PROMPT_IMPROVER_MODEL": "LFM2.5-8B-A1B"
      }
    }
  }
}
```

### Step 4: ถ้ามี token ค่อยเพิ่ม

เช่น Notion/GitHub/Figma:

```json
{
  "env": {
    "PROMPT_IMPROVER_API_URL": "http://localhost:1234/v1/chat/completions",
    "PROMPT_IMPROVER_MODEL": "LFM2.5-8B-A1B",
    "NOTION_TOKEN": "ใส่ token ของคุณ",
    "GITHUB_TOKEN": "ใส่ token ของคุณ",
    "FIGMA_TOKEN": "ใส่ token ของคุณ"
  }
}
```

ถ้ายังไม่ใช้ Notion/GitHub/Figma ไม่ต้องใส่

### Step 5: Save และ restart/refresh

หลังแก้ `mcp.json`:

```text
Save
Restart LM Studio หรือ refresh MCP tools ถ้ามีปุ่ม
```

### Step 6: ทดสอบ

ใน LM Studio ลองถาม:

```text
Use skill-runtime first. Route this request and tell me what workflow, skills, and toolsets you recommend:

I want to organize my Obsidian notes and draft Notion payloads without applying anything.
```

ถ้าเชื่อม MCP สำเร็จ ควรเห็นว่ามันเรียกหรือแนะนำ `skill-runtime`

## ถ้าใช้ provider อื่น

### LM Studio

ใน `config.json`:

```json
"active_provider": "lm-studio"
```

ค่า env:

```json
"PROMPT_IMPROVER_API_URL": "http://localhost:1234/v1/chat/completions"
```

### Ollama

ถ้าจะเปลี่ยนเป็น Ollama:

```json
{
  "active_provider": "ollama",
  "active_model": "qwen2.5-coder:7b"
}
```

แล้วใน `mcp.json`:

```json
"env": {
  "PROMPT_IMPROVER_API_URL": "http://localhost:11434/v1/chat/completions",
  "PROMPT_IMPROVER_MODEL": "qwen2.5-coder:7b"
}
```

### llama.cpp

ถ้าใช้ llama.cpp server:

```json
{
  "active_provider": "llama-cpp",
  "active_model": "local-model"
}
```

ใน `mcp.json`:

```json
"env": {
  "PROMPT_IMPROVER_API_URL": "http://localhost:8080/v1/chat/completions",
  "PROMPT_IMPROVER_MODEL": "local-model"
}
```

### vLLM

```json
"env": {
  "PROMPT_IMPROVER_API_URL": "http://localhost:8000/v1/chat/completions",
  "PROMPT_IMPROVER_MODEL": "your-vllm-model"
}
```

### OpenAI-compatible remote

ใช้กับ provider ที่มี endpoint แบบ `/v1/chat/completions`

```json
"env": {
  "PROMPT_IMPROVER_API_URL": "https://api.example.com/v1/chat/completions",
  "PROMPT_IMPROVER_MODEL": "your-model",
  "OPENAI_COMPATIBLE_API_KEY": "ใส่ key ใน env หรือ client secret manager"
}
```

### OpenRouter

```json
"env": {
  "PROMPT_IMPROVER_API_URL": "https://openrouter.ai/api/v1/chat/completions",
  "PROMPT_IMPROVER_MODEL": "openrouter/auto",
  "OPENROUTER_API_KEY": "ใส่ key ของคุณ"
}
```

### Groq

```json
"env": {
  "PROMPT_IMPROVER_API_URL": "https://api.groq.com/openai/v1/chat/completions",
  "PROMPT_IMPROVER_MODEL": "llama-3.1-8b-instant",
  "GROQ_API_KEY": "ใส่ key ของคุณ"
}
```

### Together

```json
"env": {
  "PROMPT_IMPROVER_API_URL": "https://api.together.xyz/v1/chat/completions",
  "PROMPT_IMPROVER_MODEL": "ใส่ model id",
  "TOGETHER_API_KEY": "ใส่ key ของคุณ"
}
```

### Fireworks

```json
"env": {
  "PROMPT_IMPROVER_API_URL": "https://api.fireworks.ai/inference/v1/chat/completions",
  "PROMPT_IMPROVER_MODEL": "ใส่ model id",
  "FIREWORKS_API_KEY": "ใส่ key ของคุณ"
}
```

### Mistral

```json
"env": {
  "PROMPT_IMPROVER_API_URL": "https://api.mistral.ai/v1/chat/completions",
  "PROMPT_IMPROVER_MODEL": "mistral-small-latest",
  "MISTRAL_API_KEY": "ใส่ key ของคุณ"
}
```

### OpenAI / Anthropic / Gemini

ใน `config.json` มี provider metadata สำหรับ OpenAI, Anthropic และ Gemini เพื่อให้ agent รู้ว่า provider เหล่านี้มีอยู่

ข้อควรจำ:

```text
OpenAI = ใช้ OpenAI-compatible chat completions ได้
Anthropic = ใช้ Messages API ไม่ใช่ OpenAI-compatible โดยตรง
Gemini = ใช้ Gemini API ไม่ใช่ OpenAI-compatible โดยตรง
```

ดังนั้น `prompt_improver.py` ตอนนี้เหมาะกับ OpenAI-compatible endpoint เป็นหลัก ถ้าจะเรียก Anthropic/Gemini โดยตรง ควรเพิ่ม adapter tool หรือใช้ provider gateway ที่แปลงเป็น OpenAI-compatible เช่น OpenRouter หรือ custom proxy

## Provider ประเภทไหนใช้กับ prompt_improver ได้ทันที

ใช้ได้ทันทีเมื่อ provider เป็น:

```text
openai-compatible
```

ตัวอย่าง:

- LM Studio
- Ollama OpenAI endpoint
- llama.cpp server
- vLLM
- OpenAI
- OpenRouter
- Groq
- Together
- Fireworks
- Mistral
- custom OpenAI-compatible server

ต้องมี adapter เพิ่มถ้าจะเรียก direct API:

- Anthropic Messages API
- Gemini API

แต่ยังใส่ไว้ใน `config.json` ได้ เพื่อให้ agent/provider router รู้จัก

## วิธีเลือก preset

ใน `config.json` มี `task_presets`

เช่น:

```json
"prompt-improver": {
  "model": "LFM2.5-8B-A1B",
  "context_window": 8192,
  "max_output_tokens": 2048,
  "temperature": 0.3
}
```

ใช้เป็นค่าแนะนำเวลาตั้ง model ใน LM Studio:

```text
Context length: 8192 หรือมากกว่า
Max tokens: 2048
Temperature: 0.3
Top P: 0.9
Repeat penalty: 1.08
```

สำหรับใช้งานทั่วไป แนะนำ:

```text
Context length: 32768
Max tokens: 4096
Temperature: 0.2
Top P: 0.9
Repeat penalty: 1.08
```

## ตัวอย่างการตั้งค่าเต็มสำหรับคุณ

ใช้ LM Studio + LFM2.5:

```json
{
  "mcpServers": {
    "ai-desk-tools": {
      "command": "C:\\Users\\natth\\Documents\\Skill-Agents\\mcp-tools\\.venv\\Scripts\\python.exe",
      "args": [
        "C:\\Users\\natth\\Documents\\Skill-Agents\\mcp-tools\\server.py"
      ],
      "env": {
        "PROMPT_IMPROVER_API_URL": "http://localhost:1234/v1/chat/completions",
        "PROMPT_IMPROVER_MODEL": "LFM2.5-8B-A1B"
      }
    }
  }
}
```

ถ้าจะเพิ่ม Notion/GitHub/Figma:

```json
{
  "mcpServers": {
    "ai-desk-tools": {
      "command": "C:\\Users\\natth\\Documents\\Skill-Agents\\mcp-tools\\.venv\\Scripts\\python.exe",
      "args": [
        "C:\\Users\\natth\\Documents\\Skill-Agents\\mcp-tools\\server.py"
      ],
      "env": {
        "PROMPT_IMPROVER_API_URL": "http://localhost:1234/v1/chat/completions",
        "PROMPT_IMPROVER_MODEL": "LFM2.5-8B-A1B",
        "NOTION_TOKEN": "ใส่ token ของคุณ",
        "GITHUB_TOKEN": "ใส่ token ของคุณ",
        "FIGMA_TOKEN": "ใส่ token ของคุณ"
      }
    }
  }
}
```

## สิ่งที่ต้องจำ

```text
config.json = ไม่ได้ทำงานเอง เป็น reference/preset
mcp.json = LM Studio ใช้จริง
env = mcp-tools ใช้จริง
```

ถ้าคุณแก้ `config.json` แต่ไม่แก้ `mcp.json`:

```text
LM Studio จะยังใช้ค่าเดิม
```

ถ้าคุณแก้ `mcp.json`:

```text
LM Studio จะใช้ค่าใหม่หลัง save/restart/refresh
```

## ค่าแนะนำเริ่มต้น

```json
{
  "active_provider": "lm-studio",
  "active_model": "LFM2.5-8B-A1B"
}
```

เหตุผล:

- LM Studio ใช้ง่ายสำหรับเครื่องส่วนตัว
- `LFM2.5-8B-A1B` เป็น recommended starter model สำหรับ prompt improvement
- เปลี่ยนเป็นโมเดลอื่นได้ถ้าไม่มี

## ใช้กับ Prompt Improver

ถ้าใช้ LM Studio:

```powershell
$env:PROMPT_IMPROVER_API_URL="http://localhost:1234/v1/chat/completions"
$env:PROMPT_IMPROVER_MODEL="LFM2.5-8B-A1B"
```

ถ้าใช้ Ollama:

```powershell
$env:PROMPT_IMPROVER_API_URL="http://localhost:11434/v1/chat/completions"
$env:PROMPT_IMPROVER_MODEL="qwen2.5-coder:7b"
```

ถ้าใช้ llama.cpp:

```powershell
$env:PROMPT_IMPROVER_API_URL="http://localhost:8080/v1/chat/completions"
$env:PROMPT_IMPROVER_MODEL="local-model"
```

## Provider Fields

แต่ละ provider มี:

```json
{
  "type": "openai-compatible",
  "base_url": "http://localhost:1234/v1",
  "chat_completions_url": "http://localhost:1234/v1/chat/completions",
  "api_key_env": "LM_STUDIO_API_KEY",
  "api_key_required": false
}
```

ถ้า provider ต้องใช้ key ให้ใส่ชื่อ env ใน `api_key_env` แต่ไม่ใส่ค่า key จริง

## Model Fields

แต่ละ model มี:

```json
{
  "provider": "lm-studio",
  "role": "recommended-prompt-improver",
  "context_window": 32768,
  "max_output_tokens": 4096,
  "temperature": 0.2,
  "top_p": 0.9,
  "top_k": 40,
  "repeat_penalty": 1.08
}
```

## Task Presets

ใช้เลือกค่าตามงาน:

- `skill-routing`
- `prompt-improver`
- `daily-personal-agent`
- `coding-review`
- `research-rag`

ตัวอย่าง:

```json
{
  "task_presets": {
    "prompt-improver": {
      "model": "LFM2.5-8B-A1B",
      "context_window": 8192,
      "max_output_tokens": 2048,
      "temperature": 0.3
    }
  }
}
```

## Skill Runtime

ส่วนนี้บอก local agent ว่าไม่ควรอ่าน skill ทุกไฟล์:

```json
{
  "skill_runtime": {
    "route_before_loading_skills": true,
    "use_prompt_improver_when_unclear": true,
    "build_agent_context_max_chars": 24000
  }
}
```

Flow:

```text
route_request
-> prompt_improver ถ้าจำเป็น
-> build_agent_context
-> tools
```

## RAG Settings

ค่าเริ่มต้น:

```json
{
  "rag": {
    "chunk_size": 1200,
    "overlap": 120
  }
}
```

ปรับได้:

```text
notes สั้น: chunk_size 600, overlap 60
docs ยาว: chunk_size 1800, overlap 180
default: chunk_size 1200, overlap 120
```

## MCP Settings

```json
{
  "mcp": {
    "stdio_server": "mcp-tools/server.py",
    "http_server": "mcp-tools/server_http.py",
    "http_url": "http://127.0.0.1:8765",
    "default_transport": "stdio"
  }
}
```

ใช้ `stdio` ก่อนถ้าเป็น LM Studio/Claude Desktop local MCP

ใช้ `http` ถ้า client รองรับ HTTP MCP

## Safety

ค่า default:

```json
{
  "private_actions_default": "draft-only",
  "database_default": "read-only",
  "notion_default": "plan-only",
  "email_default": "draft-only"
}
```

แนะนำให้คงไว้ โดยเฉพาะตอนใช้กับ local LLM

## วิธีใช้จริง

1. เปิด `config.json`
2. เลือก `active_provider`
3. เลือก `active_model`
4. ตั้ง env ให้ตรง provider
5. รัน MCP server
6. ใช้ `skill-runtime.route_request` ก่อนทำงาน

ตัวอย่างสำหรับ LM Studio:

```powershell
$env:PROMPT_IMPROVER_API_URL="http://localhost:1234/v1/chat/completions"
$env:PROMPT_IMPROVER_MODEL="LFM2.5-8B-A1B"
cd C:\Users\natth\Documents\Skill-Agents\mcp-tools
.\.venv\Scripts\Activate.ps1
python .\server.py
```

## หมายเหตุ

ตอนนี้ `config.json` เป็น shared configuration template สำหรับคน/agent อ่านและใช้ตั้งค่า

ถ้าต้องการให้ MCP tools อ่านไฟล์นี้โดยตรงในอนาคต ควรเพิ่ม tool เช่น:

```text
model-config
  - read_model_config
  - get_active_provider
  - get_task_preset
  - export_prompt_improver_env
```
