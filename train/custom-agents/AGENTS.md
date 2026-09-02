# AGENTS.md

Project-wide rules for the Antigravity agent.

## Default Mode Settings

- **New feature / multi-file change / architecture decision**: Always use Planning Mode.
  Apply the `deep-planning` skill before writing any code.
- **Bug fix with unknown root cause**: Planning Mode. Apply `deep-planning`.
- **Bug fix that is an obvious one-line typo or off-by-one**: Fast Mode is fine.
- **Refactor touching more than one file**: Planning Mode.
- **Refactor within a single file, no behavior change**: Fast Mode is fine.
- **Test generation / documentation / formatting**: Fast Mode.

When in doubt, default to Planning Mode. A wasted plan review costs seconds;
an unreviewed multi-file change that goes wrong costs much more.

## Plan continuity (important)

This project has had recurring issues with the agent losing earlier plan context when
the conversation gets long or the user changes direction mid-thread.

Rules:
1. If an Implementation Plan artifact already exists for the current thread/feature,
   **treat new chat instructions as edits to that plan, not as a new task.**
   Update the existing artifact in place. Never silently discard prior plan content.
2. When a plan changes materially, add a one-line "Revision note" at the top of the
   artifact explaining what changed and why, so the human can track drift over time.
3. For any task expected to span multiple sessions, write the approved plan to
   `PLAN.md` at the project root as the source of truth, not just the in-conversation
   artifact. Read `PLAN.md` at the start of every session before proposing new work.

## Model routing

This project uses two custom agents (see `.agents/agents/`):
- `architect` — planning, spec-writing, and plan revisions. Runs on a stronger
  reasoning model. Never edits files directly.
- `implementer` — executes approved plans. Runs on a faster/cheaper model.
  Never invents scope beyond what `architect` approved.

Default to `architect` first for anything matching the Planning Mode rules above.
Only hand off to `implementer` once a plan has been explicitly approved.

## Skills

- Apply `deep-planning` automatically whenever a task matches the Planning Mode
  criteria above, even if the user does not explicitly ask for a plan.
