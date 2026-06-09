# Skill Agents

Personal agent skills organized for daily engineering work, productivity workflows, and Obsidian vault operations.

This repo is original work that studies public agent-skill repositories for patterns. It is not an official fork, template, distribution, or endorsement of those projects.

Pattern references:

- `thananon/9arm-skills` - small, clean buckets with shippable, draft, personal, and deprecated areas.
- `mattpocock/skills` - practical engineering workflows with feedback loops, diagnosis, TDD, and architecture care.
- `kepano/obsidian-skills` - narrow domain skills with precise syntax and tool-specific rules.
- `sickn33/antigravity-awesome-skills` - workflow orchestration through ordered playbooks, catalogs, bundles, and machine-readable indexes.
- `google/skills` - domain-specific skills, install guidance, contribution guidance, and Apache-licensed distribution.
- `anthropics/skills` - public Agent Skills examples and the broader Agent Skills concept.

See `NOTICE.md` for attribution and license notes.

## Layout

Skills live under `skills/`, grouped into buckets:

- `engineering/` - daily code work
- `research/` - news, repo discovery, and AI-skill research
- `productivity/` - communication and workflow tools
- `obsidian/` - Obsidian Markdown, Canvas, and vault work
- `misc/` - useful but infrequent skills
- `personal/` - tied to one setup, not promoted
- `in-progress/` - drafts not ready to ship
- `deprecated/` - retired skills

Portable model-neutral skills live under `Skill.md/`. These are designed to be copied into Claude, ChatGPT, Gemini, Codex, local agents, or other MCP-enabled assistants without depending on this repo's `mcp-tools/`.

Workflow playbooks live under `workflows/`. They describe how to combine multiple skills into an end-to-end job. The machine-readable index lives at `data/workflows.json`.

MCP tools live under `mcp-tools/`. They are the executable action layer: file operations, code editing, prompt improvement, web lookup, media processing, and system checks. The machine-readable tool registry lives at `data/tools.json`.

Curated toolsets live at `data/toolsets.json`. Toolsets group tool capabilities by job type so an agent can load `coding-basic`, `backend-review`, `frontend-ui`, `skill-authoring`, `safe-maintenance`, `agent-control-plane`, `finance-research`, `workspace-integrations`, `design-frontend`, `data-query`, `personal-daily-agent`, `personal-knowledge-rag`, or `task-issue-planning` instead of considering every tool at once.

Detailed inventory and roadmap docs:

- `QUICKSTART.md`
- `config.json`
- `examples/`
- `NOTICE.md`
- `docs/PROJECT_GUIDE.md`
- `docs/USAGE_FOR_PERSONAL_AND_OTHERS.md`
- `docs/MCP_API_SERVER.md`
- `docs/SKILL_RUNTIME_FLOW.md`
- `docs/LOCAL_LLM_SETTINGS.md`
- `docs/PROMPT_IMPROVER_LOCAL_MODEL.md`
- `docs/CONFIG_JSON_GUIDE.md`
- `docs/TOOLS_INVENTORY.md`
- `docs/RECOMMENDED_NEXT_TOOLS.md`
- `docs/DAILY_USAGE.md`
- `docs/WEB_CAPTURE_PROVIDERS.md`
- `docs/FINANCE_MARKET_PROVIDERS.md`
- `docs/USER_RUN_WORKFLOWS.md`

Each skill is its own directory containing a required `SKILL.md` file with YAML frontmatter:

```yaml
---
name: skill-name
description: Clear trigger guidance for when an agent should use this skill.
---
```

Optional folders inside a skill:

- `references/` - detailed docs loaded only when needed
- `scripts/` - deterministic helper scripts
- `assets/` - templates or reusable output assets

## What You Can Do With This Repo

Use this repo as a personal operating system for AI agents:

- Install the skills into Codex, Claude Code, or another skills-aware agent.
- Copy portable skills from `Skill.md/` into any agent that accepts instruction files, project instructions, custom GPT/Gem guidance, or skill-like prompts.
- Ask the agent to use a specific skill, such as `diagnose`, `tdd`, or `obsidian-vault-workflow`.
- Ask the agent to follow a workflow, such as `ship-feature`, `debug-regression`, or `obsidian-vault-cleanup`.
- Ask for a personal daily workflow with `daily-personal-agent`.
- Ask to connect Obsidian, Notion, memory, and RAG with `personal-knowledge-sync`.
- Ask for recurring or one-off reports with `daily-news-report`, `markdown-report`, or `automation-design`.
- Keep company-specific or personal instructions in `personal/` without mixing them into public skills.
- Draft experimental skills in `in-progress/`, then promote them when the workflow is proven.
- Publish the repo as a GitHub skill pack for your team.
- Expose repeated executable actions as MCP tools and connect them to skills/workflows.

Example prompts:

```text
Use the ship-feature workflow to implement this request end to end.
```

```text
Use diagnose first. Do not patch until you have a failing signal.
```

```text
Use obsidian-vault-workflow to organize this folder and preserve existing links.
```

```text
Use skill-management to create a new skill for our support-ticket workflow.
```

```text
Use build-mcp-tool to turn this Python helper into a safe MCP tool.
```

```text
Use model-portability-adapter to make this skill work across Claude, ChatGPT, Gemini, and local MCP agents.
```

```text
Use daily-personal-agent. Summarize my calendar, inbox, chat, Notion, Obsidian, and memory context into today's plan.
```

```text
Use personal-knowledge-sync. Treat Obsidian as source of truth and draft Notion payloads without applying them.
```

## Install

With `npx skills`, replace `your-github-user/your-skill-repo` with your own published repo:

```bash
npx skills add your-github-user/your-skill-repo
```

Manual install:

```bash
cp -R skills/* ~/.codex/skills/
```

For Claude Code, copy shippable skill folders into `~/.claude/skills/`.

## Reference

### Workflows

- `ship-feature` - plan, implement, test, review, and hand off a product or code feature.
- `debug-regression` - reproduce, diagnose, fix, test, and document a regression.
- `review-pr` - inspect a change with review-first output and targeted follow-up.
- `obsidian-vault-cleanup` - organize a vault or folder while preserving links and conventions.
- `create-new-skill` - turn a repeated task into a clean installable skill.
- `build-mcp-tool` - turn a repeated executable action into a clean MCP tool.
- `daily-personal-agent` - combine calendar, inbox, chat, notes, memory, and drafts into a daily plan.
- `personal-knowledge-sync` - move knowledge between Obsidian, Notion, memory, and RAG safely.

### Portable Skill.md

- `universal-agent-operating-system` - portable operating rules for any capable agent.
- `model-portability-adapter` - adapt skills and workflows across model providers.
- `tool-agnostic-mcp-routing` - map tasks to available tools by capability.
- `cross-model-handoff` - create handoffs another model or agent can continue.

### MCP Tools

- `filesystem` - read, inspect, and search local project files.
- `registry` - inspect available tools, workflow metadata, runtime capabilities, allowed roots, and tool policy.
- `skill-runtime` - route requests to workflows, skills, and toolsets, then load compact context for local LLMs.
- `toolsets` - list, recommend, inspect, and validate curated toolsets by job type.
- `audit` - inspect audit logs, policy denials, and recent tool activity.
- `mcp-security-audit` - classify tool risk, find mutating tools, and summarize attack surface.
- `security-scanner` - scan repo secrets, dangerous commands, env exposure, and dependency risks.
- `project` - inspect project stack, package scripts, important files, and lightweight health.
- `docs` - find README/docs files, summarize documentation coverage, and build context bundles.
- `repo-index` - build lightweight repo maps, search symbols/files, and find related files.
- `external-mcp-catalog` - compare open-source MCP patterns and draft local tool adaptations.
- `package` - inspect package managers, manifests, lockfiles, dependencies, and dependency health.
- `docker` - inspect Dockerfile/Compose files and plan Docker validation commands without running containers.
- `api` - inspect likely route files, endpoints, OpenAPI specs, and API config hints.
- `database` - inspect schema files, migrations, ORM models, and database config hints.
- `postgres` - plan and run read-only Postgres queries when explicitly configured.
- `config` - inspect config files, env keys, examples, and secret hygiene signals.
- `test-inspection` - find test files, frameworks, and source-to-test hints without running tests.
- `ci` - inspect CI files, GitHub Actions jobs, and validation commands without running them.
- `task` - scan TODO/FIXME/HACK/BUG markers and roadmap files.
- `dependency-risk` - inspect offline dependency risk signals from manifests.
- `release` - inspect changelog/version/release readiness signals.
- `backup` - plan, create, and list zip snapshots inside allowed roots.
- `structured-data` - read, validate, inspect, and patch JSON/YAML/TOML safely.
- `memory` - store, search, and summarize local project memories.
- `memory-context` - save typed decisions/preferences/bug lessons and build context packs.
- `vector-memory` - search and relate long-running memories with lightweight semantic scoring.
- `rag-adapter` - chunk text, plan RAG indexes, and draft embedding-provider request payloads.
- `finance-market` - look up educational market quotes, crypto prices, finance-news plans, watchlists, and simple position risk.
- `notion` - search/read Notion pages and draft safe note/block updates when a token is configured.
- `obsidian-notion-bridge` - inspect Obsidian notes and draft Notion/Markdown conversion plans.
- `calendar` - summarize supplied events, draft meeting prep, and build daily plans.
- `email-inbox` - plan email searches, summarize supplied emails, extract actions, and draft replies.
- `figma` - inspect Figma files, extract design-token hints, and draft frontend implementation plans.
- `slack-discord` - search/summarize Slack messages, draft chat replies, and extract action items when configured.
- `issue-tracker` - parse issue references, draft issues, break down work, and plan updates for GitHub/Linear/Jira-style workflows.
- `github` - inspect local GitHub workflows and draft PR descriptions.
- `github-api` - read GitHub repo, issue, PR, file, and check metadata when a token is configured.
- `browser` - inspect browser readiness, static HTML, localhost URLs, and smoke-check plans.
- `browser-page-map` - turn HTML into a page map of headings, links, forms, buttons, and labels.
- `playwright` - inspect live pages and capture screenshots with Playwright when runtime is available.
- `playwright-actions` - click, fill, assert visible text, inspect console/network failures, capture accessibility snapshots, run UI checks, and keep persistent browser sessions with Playwright.
- `sandbox` - create safe temp workspaces and compile snippets without arbitrary execution.
- `git` - inspect repository status, diffs, branches, and commits without mutation.
- `git-control` - create/switch branches, stage/unstage files, and commit staged changes safely.
- `code-editing` - patch, format, diff, and test code.
- `user-runner` - create scripts and command handoffs for actions the user should run outside the agent sandbox.
- `validation` - plan and run allowlisted tests, lint, typecheck, and build commands.
- `prompt-improver` - analyze, rewrite, score, and template prompts.
- `web` - search, fetch, extract, and summarize sources.
- `web-capture` - capture public webpages through local static, local browser, or optional Firecrawl-style providers with social-site safety limits.
- `media` - inspect and process images, audio, and video.
- `system` - inspect environment and run validation commands.

### Engineering

- `diagnose` - disciplined debugging and performance regression loop.
- `tdd` - red-green-refactor implementation for features and bug fixes.
- `code-review` - review code for bugs, regressions, and missing tests.
- `architecture-review` - find design pressure, coupling, and simplification opportunities.

### Research

- `daily-news-report` - create sourced current-news briefings and scheduled digests.
- Finance research uses `finance-market` with `web` and `web-capture` for market quotes, crypto prices, public news, and educational summaries. It is not financial advice.
- `github-skill-research` - research AI-agent skill and workflow patterns from real repos and docs.
- `project-discovery` - inspect and summarize a project before planning or editing.

### Productivity

- `grill-with-docs` - ask sharp planning questions and produce durable project docs.
- `handoff` - compact a session into a continuation-ready handoff.
- `markdown-report` - produce clean Markdown reports, briefs, RCA notes, and decision records.
- `automation-design` - design Codex automations, recurring reports, monitors, and reminders.
- `prompt-improvement` - rewrite vague prompts into clear executable prompts.
- `inbox-meeting-triage` - turn email/chat/calendar context into actions, meeting notes, drafts, and issue tasks.

### Obsidian

- `obsidian-markdown` - create and edit Obsidian flavored Markdown.
- `obsidian-canvas` - create and edit JSON Canvas files.
- `obsidian-vault-workflow` - operate across an Obsidian vault with links, tags, properties, and structure.
- `obsidian-notion-bridge` - convert and sync-plan between Obsidian Markdown and Notion pages safely.

### Repository Management

- `skill-management` - create, classify, improve, deprecate, and reorganize skills.
- `mcp-tool-management` - organize MCP tools and connect them to skills and workflows.
- `in-progress-skill-incubator` - prototype draft skills before promotion.
- `personal-skill-rules` - keep personal-only instructions scoped and private.
- `personal-agent-workflow` - coordinate private daily planning across notes, calendar, inbox, chat, memory, and issue trackers.
- `deprecated-skill-maintenance` - retire stale skills with replacement guidance.
- `boomz-preferences` - apply Boomz's personal language, reporting, and workflow preferences.

## Skill Quality Rules

- Keep each `SKILL.md` focused and under 500 lines.
- Put only essential operating instructions in `SKILL.md`.
- Move long syntax tables or examples into `references/`.
- Make descriptions explicit enough that the agent can decide when to load the skill.
- Prefer workflows with verification steps over advice-only prompts.

## How To Grow It

1. Add a skill when a task repeats at least three times.
2. Add a workflow when a job needs multiple skills in a reliable order.
3. Add a tool when a repeated action should be performed by code instead of agent judgment.
4. Add a portable skill in `Skill.md/` when it should work across model providers.
5. Add references when the skill needs detailed syntax, product docs, schemas, or examples.
6. Keep public skills general and move personal preferences into `personal/`.
7. Retire stale skills into `deprecated/` instead of silently deleting them.

## Validate Everything

Run the full local health check from the repo root:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\validate-all.ps1
```

If `python` is not on PATH, pass an explicit executable:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\validate-all.ps1 -Python 'C:\path\to\python.exe'
```

## Repo Split Guidance

Keep everything together while developing personally. Split into separate repos when you publish or share with a team:

```text
skill-agents/        = Skill.md, skills, workflows, docs
ai-desk-mcp-tools/   = MCP server, Python tools, requirements
```

Skills are portable behavior. Tools are software with dependencies and permissions.
