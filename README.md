# Skill Agents

Personal AI-agent skills, workflows, prompts, and setup guides for using AI assistants with local tools.

This repo is the **skill and workflow layer**. It tells an AI agent how to work: how to plan, debug, review code, organize Obsidian notes, draft Notion payloads, improve prompts, route skills, and run personal daily workflows.

For executable MCP tools, use the companion repo:

[ntaffzii/ai-desk-tools](https://github.com/ntaffzii/ai-desk-tools)

```text
Skill-Agents       = skills, workflows, docs, examples, provider config
ai-desk-tools      = MCP server, Python tools, tests, runtime safety policy
local-llm          = llama.cpp Router, FastAPI Orchestrator, Docker deployment
```

Recommended Local LLM repository name: `ntaffzii/local-llm-orchestrator`.

## Who This Is For

Use this repo if you want an AI agent to:

- follow reusable `SKILL.md` instructions
- use workflow playbooks such as `ship-feature` or `daily-personal-agent`
- work across Codex, Claude, ChatGPT, Gemini, LM Studio, local LLMs, and MCP clients
- route tasks to the right skill/workflow before loading context
- connect personal notes, Notion, Obsidian, memory, RAG, and MCP tools
- keep personal automation safe with draft-only and read-only defaults

## Companion Repo

This repo does not need to contain the MCP server when published separately.

Install or clone the MCP tools from:

[ntaffzii/ai-desk-tools](https://github.com/ntaffzii/ai-desk-tools)

Typical setup:

```text
1. Clone Skill-Agents for skills/workflows/docs.
2. Clone ai-desk-tools for MCP tools.
3. Configure your AI client to run ai-desk-tools/server.py.
4. Tell your local LLM or agent to use Skill-Agents prompts and workflows.
```

## Quick Start

Clone this repo:

```bash
git clone https://github.com/ntaffzii/Skill-Agents.git
cd Skill-Agents
```

Read first:

- [QUICKSTART.md](QUICKSTART.md)
- [docs/COMPLETE_LOCAL_AI_SYSTEM.md](docs/COMPLETE_LOCAL_AI_SYSTEM.md)
- [docs/PROJECT_GUIDE.md](docs/PROJECT_GUIDE.md)
- [docs/USAGE_FOR_PERSONAL_AND_OTHERS.md](docs/USAGE_FOR_PERSONAL_AND_OTHERS.md)

Then clone MCP tools:

```bash
git clone https://github.com/ntaffzii/ai-desk-tools.git
cd ai-desk-tools
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Configure LM Studio, Claude Desktop, or another MCP client to run:

```text
ai-desk-tools/server.py
```

## Install Skills

### Automatic Sync Tool (Recommended)

This repo includes a built-in sync script that copies skills to your AI providers automatically.

Run in PowerShell from the repo root:

```powershell
.\sync
```

The tool shows a 2-step interactive menu:

1. Choose which skill(s) to sync (or press Enter for all)
2. Choose the target AI Provider:

| Key | Provider | Install Path |
|---|---|---|
| A | All providers | — |
| 1 | Antigravity IDE | `~/.gemini/config/skills/` |
| 2 | Claude Code | `~/.claude/skills/` |
| 3 | OpenCode Interpreter | `~/.opencode/skills/` |

One-liner to sync a specific skill to a specific provider:

```powershell
# Sync all skills to Antigravity IDE
.\sync thai antigravity

# Sync trading skill to Claude Code only
.\sync trading claude

# Sync all skills to all providers
.\sync
```

Full usage guide: [docs/SYNC_SKILLS_GUIDE.md](docs/SYNC_SKILLS_GUIDE.md)

---

### Manual Install

If you prefer to copy files manually:

```bash
# Claude Code
cp -R skills/* ~/.claude/skills/

# Antigravity IDE
cp -R skills/* ~/.gemini/config/skills/
```

On Windows PowerShell:

```powershell
# Antigravity IDE
Copy-Item -Recurse .\skills\* "$env:USERPROFILE\.gemini\config\skills\"

# Claude Code
Copy-Item -Recurse .\skills\* "$env:USERPROFILE\.claude\skills\"
```

## Local LLM Usage

For LM Studio, Ollama, llama.cpp, vLLM, or any local LLM that does not have native skill loading, use:

[examples/local-llm-agent-prompt.md](examples/local-llm-agent-prompt.md)

Recommended flow:

```text
User request
  -> skill-runtime.route_request
  -> prompt-improver if unclear
  -> skill-runtime.build_agent_context
  -> use recommended toolset/tools
  -> answer with verification
```

The `skill-runtime` and `prompt-improver` tools live in:

[ntaffzii/ai-desk-tools](https://github.com/ntaffzii/ai-desk-tools)

## LM Studio MCP Setup

1. Clone and install [ntaffzii/ai-desk-tools](https://github.com/ntaffzii/ai-desk-tools)
2. Open LM Studio
3. Go to `Program > Install > Edit mcp.json`
4. Add a server pointing to `ai-desk-tools/server.py`

Example config is in:

[examples/lm-studio-mcp-config.json](examples/lm-studio-mcp-config.json)

For model/provider settings, see:

- [config.json](config.json)
- [docs/CONFIG_JSON_GUIDE.md](docs/CONFIG_JSON_GUIDE.md)
- [docs/LOCAL_LLM_SETTINGS.md](docs/LOCAL_LLM_SETTINGS.md)
- [docs/PROMPT_IMPROVER_LOCAL_MODEL.md](docs/PROMPT_IMPROVER_LOCAL_MODEL.md)

Recommended prompt-improver model when available:

```text
LFM2.5-8B-A1B
```

It is recommended, not required.

## Repo Layout

```text
Skill-Agents/
  Skill.md/        portable model-neutral skills
  skills/          local skill folders with SKILL.md
  workflows/       ordered workflow playbooks
  data/            tools/toolsets/workflows/skills-index registry metadata
  docs/            guides and usage docs
  examples/        prompts and MCP client examples
  scripts/         validators and repo utilities
  config.json      provider/model/preset reference
```

## Main Workflows

- `ship-feature` - implement and verify a feature end to end
- `debug-regression` - reproduce, diagnose, fix, and verify a regression
- `review-pr` - review a diff or PR with findings first
- `obsidian-vault-cleanup` - organize Obsidian notes safely
- `create-new-skill` - create a new reusable skill
- `build-mcp-tool` - design a new MCP tool
- `research-report` - create sourced research reports
- `daily-personal-agent` - build a personal daily plan
- `personal-knowledge-sync` - connect Obsidian, Notion, memory, and RAG

## Skill Categories

- `engineering/` - diagnose, TDD, code review, architecture review
- `research/` - news, GitHub skill research, project discovery, claim/citation integrity check, repo-tour (guided tour/onboarding/diff-impact over an existing graphify graph)
- `productivity/` - handoff, prompt improvement, reports, automation, inbox triage
- `obsidian/` - Markdown, Canvas, vault workflow, Notion bridge
- `misc/` - skill and MCP tool management
- `thai/` - Thai-locale domain knowledge (tax invoices, government letters, PDPA, ID/PromptPay validation, dates, translation, resumes) - see `skills/thai/SKILL.md`
- `trading/` - market regime, position sizing, risk gates, portfolio review, trade journaling (not financial advice) - see `skills/trading/SKILL.md`
- `personal/` - private/personal preferences and daily-agent workflow
- `in-progress/` - draft skills
- `deprecated/` - retired skills with replacement guidance

## Portable Skill.md

`Skill.md/` contains portable skills that can be copied into other agents:

- `universal-agent-operating-system`
- `model-portability-adapter`
- `tool-agnostic-mcp-routing`
- `cross-model-handoff`

Use these when a provider does not support native skill folders.

## Common Prompts

Daily planning:

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

Review:

```text
Use review-pr. Inspect the diff and related files. Report findings first with severity, file, and line reference.
```

Local LLM routing:

```text
Use skill-runtime first. Route this request, improve it only if unclear, then load selected workflow and skills.
```

## Documentation

### Getting Started

- [QUICKSTART.md](QUICKSTART.md)
- [docs/ONBOARDING.md](docs/ONBOARDING.md)
- [docs/PROJECT_GUIDE.md](docs/PROJECT_GUIDE.md)
- [docs/USAGE_FOR_PERSONAL_AND_OTHERS.md](docs/USAGE_FOR_PERSONAL_AND_OTHERS.md)

### Skills

- [docs/SYNC_SKILLS_GUIDE.md](docs/SYNC_SKILLS_GUIDE.md) — sync skills to AI providers (Antigravity, Claude, OpenCode)
- [docs/NEW_SKILLS_GUIDE.md](docs/NEW_SKILLS_GUIDE.md) — guide to recently added skills
- [docs/SKILL_RUNTIME_FLOW.md](docs/SKILL_RUNTIME_FLOW.md)
- [docs/TOUR.md](docs/TOUR.md)

### Configuration & Setup

- [docs/CONFIG_JSON_GUIDE.md](docs/CONFIG_JSON_GUIDE.md)
- [docs/LOCAL_LLM_SETTINGS.md](docs/LOCAL_LLM_SETTINGS.md)
- [docs/PROMPT_IMPROVER_LOCAL_MODEL.md](docs/PROMPT_IMPROVER_LOCAL_MODEL.md)
- [docs/COMPLETE_LOCAL_AI_SYSTEM.md](docs/COMPLETE_LOCAL_AI_SYSTEM.md)

### Tools & Integrations

- [docs/TOOLS_INVENTORY.md](docs/TOOLS_INVENTORY.md)
- [docs/MCP_API_SERVER.md](docs/MCP_API_SERVER.md)
- [docs/WEB_CAPTURE_PROVIDERS.md](docs/WEB_CAPTURE_PROVIDERS.md)
- [docs/FINANCE_MARKET_PROVIDERS.md](docs/FINANCE_MARKET_PROVIDERS.md)
- [docs/RECOMMENDED_NEXT_TOOLS.md](docs/RECOMMENDED_NEXT_TOOLS.md)
- [NOTICE.md](NOTICE.md)

## Validate

From the combined workspace:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\validate-all.ps1
```

This validates:

- tool registry metadata
- toolsets
- workflows
- `skills/**/SKILL.md`
- `Skill.md/**/SKILL.md`
- `data/skills-index.json` is current (regenerate with `scripts/generate-skills-index.ps1` after adding/renaming/removing a skill)
- MCP tool Python syntax and tests when tools are present

## Attribution

This repo is original work inspired by public agent-skill and MCP repositories. It is not an official fork, template, distribution, or endorsement of those projects.

See [NOTICE.md](NOTICE.md) for attribution and license notes.

## License

See [LICENSE](LICENSE).
