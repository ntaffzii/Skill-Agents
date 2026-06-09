# Tools Inventory

This document tracks what has already been built, what each area is for, and what remains optional for later.

## Current Status

- Tool groups: 53
- Toolsets: 13
- Workflows: 9
- Main local skills: 24
- Portable skills: 4

## Toolsets

| Toolset | Purpose | Tool groups |
|---|---|---|
| `coding-basic` | Everyday code work | filesystem, project, docs, repo-index, git, git-control, code-editing, validation, structured-data |
| `backend-review` | Backend/API/database review | project, docs, repo-index, package, docker, api, database, config, test-inspection, ci, dependency-risk, security-scanner, git, validation |
| `frontend-ui` | Frontend/UI work | project, docs, repo-index, package, docker, browser, browser-page-map, playwright, playwright-actions, figma, test-inspection, ci, git, code-editing, validation, media |
| `skill-authoring` | Skills/workflows/tool docs | filesystem, docs, repo-index, registry, skill-runtime, external-mcp-catalog, structured-data, task, memory, memory-context, notion, web, web-capture, prompt-improver, validation |
| `safe-maintenance` | Safer broad maintenance | registry, audit, mcp-security-audit, security-scanner, backup, git, git-control, github-api, external-mcp-catalog, task, release, dependency-risk, config, ci, docker, validation, user-runner |
| `agent-control-plane` | Agent runtime control | registry, skill-runtime, toolsets, audit, mcp-security-audit, memory, memory-context, vector-memory, external-mcp-catalog, web-capture, sandbox, system, user-runner |
| `finance-research` | Finance and market research | finance-market, web, web-capture, memory, memory-context, vector-memory, docs, prompt-improver |
| `workspace-integrations` | Notion, Obsidian-adjacent notes, Slack, Discord, and cross-app handoffs | notion, obsidian-notion-bridge, slack-discord, email-inbox, calendar, web-capture, memory, memory-context, vector-memory, rag-adapter, docs, prompt-improver |
| `design-frontend` | Figma-to-frontend and UI mapping | figma, browser-page-map, project, docs, repo-index, package, browser, playwright, playwright-actions, test-inspection, ci, git, code-editing, validation, media |
| `data-query` | Read-only database research | database, postgres, security-scanner, config, validation |
| `personal-daily-agent` | Personal planning across calendar, inbox, chat, notes, issues, memory, finance, and handoffs | skill-runtime, calendar, email-inbox, notion, obsidian-notion-bridge, slack-discord, issue-tracker, memory, memory-context, vector-memory, rag-adapter, docs, web, web-capture, finance-market, prompt-improver, user-runner |
| `personal-knowledge-rag` | Index and search local notes, memory, Notion context, and research | skill-runtime, filesystem, docs, repo-index, memory, memory-context, vector-memory, rag-adapter, notion, obsidian-notion-bridge, structured-data, web-capture |
| `task-issue-planning` | Turn messages, notes, and requirements into issues and task plans | skill-runtime, issue-tracker, github-api, notion, slack-discord, email-inbox, calendar, docs, memory-context, git, prompt-improver |

## Tool Groups Already Built

### Control Plane

- `registry` - discover tools, workflows, runtime capabilities, roots, and policy.
- `skill-runtime` - index skills, route requests to workflows/skills/toolsets, load selected files, and build compact context packs.
- `toolsets` - recommend focused toolsets by job type.
- `audit` - inspect audit logs and policy denials.
- `mcp-security-audit` - classify tool risk, find mutating tools, check policy coverage, and summarize attack surface.
- `security-scanner` - scan repository files for likely secrets, dangerous commands, env exposure, dependency risks, and security reports.
- `system` - inspect environment, command availability, current time, and health.

### Project Context

- `project` - inspect stack, manifests, scripts, and project health.
- `docs` - find README/docs/ADR files and build context bundles.
- `repo-index` - build lightweight repo maps, search by names/symbols/previews, find related files, and summarize repo shape.
- `external-mcp-catalog` - search curated MCP/agent-tool catalogs, compare repo patterns, and draft local tool adaptations.
- `package` - inspect package managers, manifests, lockfiles, and dependencies.
- `docker` - inspect Dockerfile/Compose files, Docker CLI availability, and Docker validation plans without running containers.
- `config` - inspect config files, env keys, examples, and secret hygiene signals.
- `task` - scan TODO/FIXME/HACK/BUG markers and roadmap files.
- `release` - inspect changelog/version/release readiness signals.

### Code Work

- `filesystem` - list, read, search, and inspect files.
- `structured-data` - read, validate, inspect, and patch JSON/YAML/TOML.
- `code-editing` - write files, replace exact blocks, preview diffs, run formatter/test commands.
- `user-runner` - write auditable scripts and command handoffs for user-run actions outside sandbox.
- `validation` - plan, check, and run allowlisted validation commands.
- `sandbox` - create temp workspaces and compile snippets without arbitrary execution.
- `backup` - plan/create/list zip snapshots inside allowed roots.

### Git And GitHub

- `git` - read-only status, diff, log, show, and branch inspection.
- `git-control` - create/switch branches, stage/unstage, and commit staged changes.
- `github` - inspect local GitHub metadata/workflows and draft PR descriptions.
- `github-api` - inspect repo, issue, PR, changed files, and check metadata through GitHub API when a token is configured.
- `issue-tracker` - check GitHub/Linear/Jira config, parse issue references, draft issues, break down tasks, and plan issue updates.

### Backend And Data

- `api` - inspect route files, endpoints, OpenAPI specs, and API config hints.
- `database` - inspect schema files, migrations, ORM models, and database config hints.
- `postgres` - check Postgres configuration, explain SQL risk, plan read-only queries, run read-only SQL when configured, and summarize result shape.
- `dependency-risk` - inspect dependency risk signals offline from manifests.
- `test-inspection` - find tests, frameworks, and source-to-test hints without running tests.
- `ci` - find CI files, inspect GitHub Actions jobs, extract validation commands, and summarize CI surface.

### UI And Media

- `browser` - inspect browser readiness, static HTML, localhost URLs, and smoke-check plans.
- `browser-page-map` - parse HTML into a compact page map with headings, links, forms, buttons, inputs, and matching by label.
- `playwright` - inspect live pages, collect title/text/console errors, and capture screenshots.
- `playwright-actions` - click, fill, assert text, inspect console/network failures, capture accessibility snapshots, run small UI check sequences, and keep persistent sessions.
- `figma` - check auth, inspect Figma file summaries, extract design token hints, inspect components, and draft frontend implementation plans.
- `media` - inspect/process image, audio, and video artifacts.

### Agent Support

- `memory` - store, list, search, and summarize local project memories.
- `memory-context` - save typed decisions, preferences, bug lessons, context packs, and memory handoffs.
- `vector-memory` - build lightweight semantic indexes, search related memories, find neighbors, and summarize memory clusters.
- `rag-adapter` - list RAG provider patterns, check embedding config, chunk text, plan indexes, and draft embedding payloads.
- `finance-market` - get educational quotes, crypto prices, finance-news query plans, watchlists, and position risk calculations.
- `notion` - check Notion auth, search/read pages, and draft safe page/block update payloads.
- `obsidian-notion-bridge` - inspect Obsidian notes, plan Notion payloads, plan Notion-to-Obsidian Markdown, and create sync checklists.
- `calendar` - check calendar config, summarize events, build daily plans, draft meeting prep, and extract follow-ups.
- `email-inbox` - check email config, plan searches, summarize supplied emails, extract actions, and draft replies.
- `slack-discord` - check Slack/Discord configuration, search/summarize messages, draft replies, and extract action items.
- `prompt-improver` - analyze, improve, score, and template prompts.
- `web` - search, fetch, extract, and summarize web sources.
- `web-capture` - capture public webpages through local/provider adapters, extract content/links, and apply social-site public-only safeguards.

## Things Not Built Yet

These are optional. They should be added only when you need the workflow.

| Candidate | Why it might help | Priority |
|---|---|---|
| `ci.py` | Deeper CI inspection for GitHub Actions and other CI systems | Done |
| `github_api.py` | Read issues, PRs, files, and checks through GitHub API | Done |
| `playwright_actions.py` | Click, fill, visible text assertions, accessibility snapshots, network/console failures, persistent sessions | Done |
| `docker.py` | Inspect Dockerfile/Compose and plan container checks | Done |
| `repo_index.py` | Build searchable project index for larger repositories | Done |
| `vector_memory.py` | Embedding/vector memory for long-running projects | Done |
| `external_mcp_catalog.py` | Search external MCP catalogs for new tool ideas | Done |
| `web_capture.py` | Provider-neutral public webpage capture and social-site public reading | Done |
| `slack.py` / `notion.py` / `jira.py` | SaaS integrations | Notion, Slack/Discord, email/calendar planning, and issue planning done; live Jira/Linear API reads optional |
| `obsidian_notion_bridge.py` | Personal knowledge sync planning | Done |
| `rag_adapter.py` | Provider-neutral RAG planning and chunking | Done |
| `calendar.py` / `email_inbox.py` | Personal planning and inbox triage | Done |
| `issue_tracker.py` | Draft and break down issue work | Done |

## Recommended Next Build Order

1. Live Jira/Linear API readers if issue tracking becomes daily.
2. Live Google Calendar/Gmail provider readers if you want direct inbox/calendar pull instead of supplied exports.
3. Cloud/kubernetes inspection only when your projects need it.
4. Controlled Docker runtime commands only with explicit approval policy.
5. Real vector store adapter when lightweight `vector-memory` and `rag-adapter` plans are no longer enough.

## Safety Notes

- Keep `git` read-only and `git-control` mutating.
- Keep `playwright` inspection separate from future `playwright-actions`.
- Do not expose push, force push, reset hard, merge, rebase, or destructive database operations until there is an explicit confirmation model.
- Continue using `tool_policy.json` for command allowlists and blocked executables.
- Run `mcp-security-audit` after adding any new tool group.
