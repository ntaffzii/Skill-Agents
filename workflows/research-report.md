# Research Report

## Goal

Research a current topic, repository pattern, market/news question, or project context and produce a sourced Markdown report.

## When To Use

Use when the user asks for research, a daily briefing, a sourced report, AI-skill research, current news, project discovery notes, or a Markdown deliverable based on multiple sources.

## Skills

- `daily-news-report`
- `github-skill-research`
- `project-discovery`
- `markdown-report`
- `handoff`

## Steps

1. Scope the research.
   - Identify topic, audience, time window, geography, source requirements, and output language.
   - Use `daily-news-report` for current news and time-sensitive topics.
   - Use `finance-market` tools when the user asks about stocks, crypto, markets, watchlists, price movement, or finance news.
   - Use `workspace-integrations` when the answer should include Notion notes, Obsidian-adjacent memory, Slack/Discord discussion, or prior personal context.
   - Use `github-skill-research` for AI-agent skill and workflow repository patterns.
   - Use `project-discovery` for local repo or codebase understanding.

2. Gather evidence.
   - Prefer primary sources, official docs, local files, and reputable reporting.
   - Browse or use current-source tools when facts may have changed.
   - If web-capture tools are available, plan capture first, then capture public pages through local-static, local-browser, or an optional provider adapter.
   - If finance-market tools are available, get quote/crypto data first, then gather public news context with web tools.
   - If Notion tools are available and the user wants workspace context, search and read only relevant pages before synthesizing.
   - If Slack/Discord tools are available and the user wants team context, summarize messages and extract action items without posting anything.
   - If vector-memory tools are available, search prior decisions and related memories before treating the question as new.
   - For Facebook, Instagram, LinkedIn, X, TikTok, or similar platforms, capture only public content; do not bypass login, CAPTCHA, private accounts, paywalls, or platform controls.
   - Save source links or file paths while reading.

3. Filter and synthesize.
   - Rank findings by relevance and practical impact.
   - Separate verified facts, inference, and uncertainty.
   - Drop duplicates and low-value background.

4. Write with `markdown-report`.
   - Use the lightest report structure that fits.
   - Put the answer and key findings near the top.
   - Include sources or file paths.

5. Hand off with `handoff`.
   - Summarize what was checked, what was not checked, and recommended next steps.

## Verification

- Major claims have sources or file references.
- Time-sensitive claims were checked against current sources.
- Finance claims include provider, timestamp or freshness caveat, currency, and a note that the output is not financial advice.
- Workspace claims identify whether they came from Notion, Obsidian/local memory, Slack/Discord, public web, or finance providers.
- Assumptions and uncertainties are labeled.
- Markdown is readable and useful for the next action.

## Output

End with:

- Report created
- Sources checked
- Key findings
- Remaining uncertainty
