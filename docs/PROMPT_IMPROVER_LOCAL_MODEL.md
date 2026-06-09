# Prompt Improver Local Model Guide

คู่มือนี้อธิบายวิธีใช้ `prompt_improver.py` กับ local LLM หรือ OpenAI-compatible endpoint เช่น LM Studio, Ollama, llama.cpp server, vLLM, OpenAI, OpenRouter, Groq, Together, Fireworks หรือ Mistral

## สรุปสั้น

`prompt_improver` ไม่จำเป็นต้องใช้โมเดลเสมอไป

```text
ถ้าไม่มี PROMPT_IMPROVER_API_URL
  -> ใช้ rule-based fallback

ถ้ามี PROMPT_IMPROVER_API_URL
  -> เรียก local/OpenAI-compatible model
```

ชื่อ `LFM2.5-8B-A1B` ไม่ใช่ required model แต่เป็นโมเดลที่แนะนำเป็นตัวแรกสำหรับงาน prompt improvement ถ้าคุณมีให้ใช้งาน เพราะขนาด 8B เหมาะกับการ rewrite, clarify, score prompt และยังไม่หนักเท่าโมเดลใหญ่

คุณเปลี่ยนเป็นโมเดลอะไรก็ได้ เช่น:

```text
LFM2.5-8B-A1B
qwen2.5-coder:7b
qwen3:8b
llama-3.1-8b-instruct
mistral-small
ชื่อโมเดลใน LM Studio
```

## Tools ที่เกี่ยวข้อง

Tool group:

```text
prompt-improver
```

Tools:

- `analyze_prompt`
- `improve_prompt`
- `generate_system_prompt`
- `score_prompt`
- `get_prompt_history`
- `export_prompt_history`

## ใช้เมื่อไหร่

ใช้ `prompt_improver` เมื่อ:

- prompt สั้นหรือคลุมเครือ
- user ขอให้ช่วยเขียน prompt
- local LLM route แล้วเจอ `needs_prompt_improver = true`
- ต้องการแปลงคำขอกว้าง ๆ เป็น prompt ที่ทำงานได้จริง
- ต้องการสร้าง system prompt สำหรับ agent/local LLM

ไม่จำเป็นต้องใช้เมื่อ:

- user request ชัดแล้ว
- workflow/skill ถูกระบุชัด เช่น `Use ship-feature`
- งานเป็น tool execution ที่ตรงไปตรงมา

## Flow ที่แนะนำ

```text
User request
  -> skill-runtime.route_request
  -> ถ้า needs_prompt_improver = true
       -> prompt_improver.analyze_prompt
       -> prompt_improver.improve_prompt
  -> skill-runtime.build_agent_context
  -> ใช้ tools ทำงาน
```

## ตั้งค่ากับ LM Studio

1. เปิด LM Studio
2. Load model ที่ต้องการ
3. เปิด local server
4. ดู URL ปกติจะเป็น:

```text
http://localhost:1234/v1/chat/completions
```

ตั้งค่าใน PowerShell:

```powershell
$env:PROMPT_IMPROVER_API_URL="http://localhost:1234/v1/chat/completions"
$env:PROMPT_IMPROVER_MODEL="ชื่อโมเดลใน LM Studio"
```

ตัวอย่าง:

```powershell
$env:PROMPT_IMPROVER_API_URL="http://localhost:1234/v1/chat/completions"
$env:PROMPT_IMPROVER_MODEL="LFM2.5-8B-A1B"
```

ถ้าไม่มี `LFM2.5-8B-A1B` ใน LM Studio ให้เปลี่ยนเป็นชื่อโมเดลที่คุณโหลดอยู่

จากนั้นรัน MCP server:

```powershell
cd C:\Users\natth\Documents\Skill-Agents\mcp-tools
.\.venv\Scripts\Activate.ps1
python .\server.py
```

## ตั้งค่ากับ Ollama

Ollama OpenAI-compatible endpoint มักเป็น:

```text
http://localhost:11434/v1/chat/completions
```

ตัวอย่าง:

```powershell
ollama pull qwen2.5-coder:7b

$env:PROMPT_IMPROVER_API_URL="http://localhost:11434/v1/chat/completions"
$env:PROMPT_IMPROVER_MODEL="qwen2.5-coder:7b"
```

## ตั้งค่ากับ llama.cpp server

ถ้าใช้ llama.cpp server ที่เปิด OpenAI-compatible endpoint:

```powershell
$env:PROMPT_IMPROVER_API_URL="http://localhost:8080/v1/chat/completions"
$env:PROMPT_IMPROVER_MODEL="local-model"
```

ตัวอย่างรัน llama.cpp:

```powershell
llama-server -m .\models\your-model.gguf --ctx-size 32768 --port 8080
```

## ตั้งค่ากับ vLLM

ถ้า vLLM เปิด OpenAI-compatible server:

```powershell
$env:PROMPT_IMPROVER_API_URL="http://localhost:8000/v1/chat/completions"
$env:PROMPT_IMPROVER_MODEL="your-vllm-model"
```

## ตั้งค่ากับ Remote OpenAI-Compatible Providers

ใช้รูปแบบเดียวกัน:

```powershell
$env:PROMPT_IMPROVER_API_URL="<provider>/v1/chat/completions"
$env:PROMPT_IMPROVER_MODEL="<model-name>"
```

ตัวอย่าง OpenRouter:

```powershell
$env:PROMPT_IMPROVER_API_URL="https://openrouter.ai/api/v1/chat/completions"
$env:PROMPT_IMPROVER_MODEL="openrouter/auto"
$env:OPENROUTER_API_KEY="..."
```

ตัวอย่าง Groq:

```powershell
$env:PROMPT_IMPROVER_API_URL="https://api.groq.com/openai/v1/chat/completions"
$env:PROMPT_IMPROVER_MODEL="llama-3.1-8b-instant"
$env:GROQ_API_KEY="..."
```

หมายเหตุ: `prompt_improver.py` รองรับ OpenAI-compatible endpoint เป็นหลัก ถ้าจะใช้ Anthropic หรือ Gemini direct API ควรใช้ adapter/proxy ที่แปลงเป็น OpenAI-compatible หรือเพิ่ม provider adapter ภายหลัง

## ตัวอย่างใน MCP config

ถ้าจะใส่ใน LM Studio/Claude Desktop MCP config:

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
        "PROMPT_IMPROVER_MODEL": "ชื่อโมเดลใน LM Studio"
      }
    }
  }
}
```

## ใช้กับ Skill Runtime

ตัวอย่าง prompt:

```text
Use skill-runtime first.
Route this request. If needs_prompt_improver is true, improve the prompt before loading skills:

จัด notes ให้หน่อย
```

ระบบควรทำ:

```text
1. route_request("จัด notes ให้หน่อย")
2. ถ้า needs_prompt_improver = true
3. analyze_prompt
4. improve_prompt
5. route_request อีกครั้งด้วย prompt ที่ชัดขึ้น
6. build_agent_context
```

## ตัวอย่างการใช้ Prompt Improver โดยตรง

```text
Use prompt-improver. Rewrite this into a clear agent prompt:

ช่วยจัดงานวันนี้ให้หน่อยจาก Notion กับ Obsidian
```

ผลลัพธ์ที่ควรได้ประมาณ:

```text
Use daily-personal-agent.
Goal: Build today's plan from Notion, Obsidian, memory, calendar, inbox, and open issues.
Constraints: Draft only. Do not send messages, update Notion, or create issues.
Output: Today plan, meetings, actions, draft replies, notes to save.
```

## Recommended Generation Settings

สำหรับ prompt improvement:

```text
context: 4096-8192
max_output: 1024-2048
temperature: 0.2-0.4
top_p: 0.9
repeat_penalty: 1.05-1.10
```

อย่าตั้ง temperature สูงมาก เพราะ model อาจเปลี่ยนเจตนาของ user

## Recommended Model

ถ้าจะเลือกหนึ่งโมเดลสำหรับ `prompt_improver` แนะนำ:

```text
LFM2.5-8B-A1B
```

เหตุผล:

- ขนาด 8B เหมาะกับเครื่องส่วนตัวมากกว่าโมเดลใหญ่
- ดีพอสำหรับ rewrite, clarify, score, และสร้าง system prompt
- ไม่จำเป็นต้องใช้ reasoning model ใหญ่สำหรับงาน prompt improvement
- ใช้ร่วมกับ LM Studio/OpenAI-compatible endpoint ได้ง่าย

ค่าที่แนะนำ:

```powershell
$env:PROMPT_IMPROVER_API_URL="http://localhost:1234/v1/chat/completions"
$env:PROMPT_IMPROVER_MODEL="LFM2.5-8B-A1B"
```

ถ้าเครื่องช้าหรือไม่มีโมเดลนี้ ให้ใช้โมเดล 7B-9B instruction รุ่นอื่นแทนได้

## Troubleshooting

### ไม่มี local model

ไม่เป็นไร ระบบจะใช้ rule-based fallback ถ้าไม่ได้ตั้ง `PROMPT_IMPROVER_API_URL`

### เรียก model ไม่ได้

ตรวจ:

```powershell
echo $env:PROMPT_IMPROVER_API_URL
echo $env:PROMPT_IMPROVER_MODEL
```

แล้วเปิด URL server ให้ตรงกับ LM Studio/Ollama/llama.cpp/vLLM

### Model เปลี่ยนเจตนา prompt

ลด:

```text
temperature: 0.1-0.2
```

เพิ่ม instruction:

```text
Preserve the user's original intent. Do not add new goals.
```

### Model ตอบยาวเกิน

ลด:

```text
max_output: 1024
```

## สรุป

ค่าเริ่มต้นสำหรับคุณ:

```powershell
$env:PROMPT_IMPROVER_API_URL="http://localhost:1234/v1/chat/completions"
$env:PROMPT_IMPROVER_MODEL="LFM2.5-8B-A1B"
```

ถ้ายังไม่เปิด local model:

```text
ไม่ต้องตั้งค่าอะไร ระบบใช้ rule-based fallback ได้
```

จำไว้:

```text
skill-runtime = เลือก skill/workflow/toolset
prompt-improver = ทำ prompt ให้ชัดเมื่อจำเป็น
MCP tools = ลงมือทำจริง
```
