# Daily Personal Agent

## Goal

Turn calendar, inbox, chat, notes, finance watch context, and prior memory into a clear personal daily plan.

## When To Use

Use when the user asks for a daily plan, personal briefing, inbox triage, meeting prep, action extraction, or a combined Notion/Obsidian/workspace summary.

## Skills

- `personal-agent-workflow`
- `markdown-report`
- `automation-design`
- `handoff`

## Steps

1. Scope the day.
   - Identify date, timezone, work/personal split, and must-do priorities.
   - Select `personal-daily-agent` when toolsets are available.

2. Gather personal context.
   - Use calendar tools for events and meeting prep.
   - Use email-inbox tools for supplied or configured inbox summaries.
   - Use Slack/Discord tools for message summaries and action items.
   - Use Notion and Obsidian bridge tools for relevant notes only.
   - Use memory/vector-memory before treating a preference or decision as new.
   - Use finance-market tools only when the user asks for market/watchlist context.

3. Decide the plan.
   - Separate hard calendar commitments, deep work, admin tasks, and personal errands.
   - Turn loose messages into action items.
   - Draft issue tracker updates when tasks should become issues.

4. Write the output.
   - Produce a short daily plan, meeting prep notes, inbox actions, and open loops.
   - Include source labels such as calendar, email, Notion, Obsidian, Slack, memory, or finance.

5. Save or hand off.
   - Save durable decisions to memory when useful.
   - Create Obsidian-ready Markdown or Notion payload plans when requested.
   - Do not send email, post chat messages, or mutate calendars automatically.

## Verification

- Every action item has a source or reason.
- Private-source claims are labeled by source.
- Draft replies and issue updates are marked as drafts.
- Time-sensitive finance/news context includes date and provider.

## Output

End with:

- Today plan
- Meetings
- Inbox/chat actions
- Notes or issue updates drafted
- Anything waiting on the user

