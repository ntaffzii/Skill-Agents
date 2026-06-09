# Daily Usage

Use this repo as a small operating system for personal AI-agent work: pick a workflow, select a focused toolset, inspect before editing, validate before handing off, and save durable context when the job teaches you something.

## Fast Start

1. Choose the job:
   - Feature work: `ship-feature`
   - Debugging: `debug-regression`
   - Review: `review-pr`
   - Skill/tool work: `create-new-skill` or `build-mcp-tool`

2. Choose the smallest useful toolset:
   - General coding: `coding-basic`
   - Backend/API/database: `backend-review`
   - Frontend/UI: `frontend-ui`
   - Skill writing: `skill-authoring`
   - Broad cleanup: `safe-maintenance`
   - Tool/runtime inspection: `agent-control-plane`
   - Notion/Obsidian/Slack/Discord work: `workspace-integrations`
   - Figma-to-frontend work: `design-frontend`
   - Read-only database research: `data-query`
   - Personal daily planning: `personal-daily-agent`
   - Personal notes/RAG: `personal-knowledge-rag`
   - Issue/task planning: `task-issue-planning`

3. Inspect before acting:
   - Project/docs/package/config first.
   - Repo index before broad exploration or when you need likely related files.
   - Dockerfile/Compose when runtime, deployment, ports, CI, or local services matter.
   - Git status/diff before edits.
   - Test and CI surface before validation.
   - Security scanner before release or broad commits.

4. Verify:
   - Run the narrowest relevant test.
   - For UI, use Playwright page inspection, screenshot, interaction checks, console/network failures, accessibility snapshot, and persistent sessions for multi-step flows.
   - For design/UI implementation, use Figma inspection and browser page maps before screenshots and Playwright actions.
   - For Notion/Obsidian work, read local notes first, then Notion pages only when configured and relevant.
   - For Slack/Discord context, summarize messages and extract action items; do not post automatically.
   - For database questions, plan and explain SQL risk first, then run only read-only Postgres queries.
   - For personal daily work, combine calendar, inbox, chat, Notion/Obsidian, memory, and issue drafts, but keep sends/mutations as drafts.
   - For RAG, chunk and index only selected sources first; preserve source paths, URLs, and page IDs.
   - For PR/release work, inspect CI commands and GitHub API metadata when available.
   - For public web or social pages, plan capture first, use provider-neutral `web-capture`, and avoid login/captcha/private-content bypass.
   - For finance questions, use `finance-research`: check quote/crypto data, read current public news, include timestamps/currency/provider, and label that it is not financial advice.

5. Save context:
   - Use memory/context tools for project decisions, user preferences, bug lessons, and continuation handoffs.
   - If sandbox blocks install, copy, publish, GUI, browser setup, or network setup, use `user-runner` to write a reviewed script for the user to run manually.

## Full Local Health Check

From the repo root:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\validate-all.ps1
```

With explicit Python:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\validate-all.ps1 -Python 'C:\path\to\python.exe'
```

## Practical Prompts

```text
Use ship-feature. Inspect project, docs, tests, CI, and git before editing. Verify with the narrowest test and summarize the diff.
```

```text
Use review-pr. If GitHub API tools are available, inspect PR files and checks. Report findings first with file and line references.
```

```text
Use frontend-ui tools. Run Playwright screenshot, console/network checks, and accessibility snapshot for this flow.
```

```text
Use workspace-integrations. Search my local memory and Notion notes about this project, summarize the latest decisions, and create an Obsidian-ready Markdown note.
```

```text
Use design-frontend. Inspect the Figma file, map the current page, then list the frontend changes needed.
```

```text
Use data-query. Explain the SQL risk first, then run only read-only Postgres queries to answer this question.
```

```text
Use daily-personal-agent. Build today's plan from calendar, email, Slack/Discord, Notion, Obsidian, memory, and finance watchlist context. Draft replies but do not send anything.
```

```text
Use personal-knowledge-sync. Convert these Obsidian notes into Notion payload plans and RAG chunks while preserving tags, links, source paths, and page IDs.
```

```text
Use task-issue-planning. Turn these notes and messages into issue drafts with acceptance criteria and implementation steps.
```

```text
Use safe-maintenance. Scan secrets, dependency risk, CI surface, audit policy, then propose only low-risk cleanup.
```
