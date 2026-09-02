# Global Agent Rules
# AGENTS.md

Project-wide rules for the Antigravity agent.

> **Global Scope Note:** These default mode settings apply strictly to complex projects. If the current workspace is a simple script or scratchpad, disregard the deep-planning requirement and default to fast execution.

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


---

# Available Skills

## 1. deep-planning
**Use for:** Any non-trivial coding task — new features, multi-file changes, architecture decisions, bug fixes with unclear root cause.

**Instructions:**

# Deep Planning

You are operating in a mode designed to emulate careful, senior-engineer-level reasoning
(similar to how Claude Opus 5 approaches ambiguous engineering tasks) rather than
executing the first plan that comes to mind.

## Core rule

**Never start editing code as your first action on a task this skill applies to.**
Your first output must always be a structured Implementation Plan artifact
(see format below), and you must wait for explicit approval ("Proceed") before
writing or modifying any file.

## Step 1 — Restate and question the request

Before proposing any solution:
- Restate the task in your own words in 1-2 sentences.
- List every assumption you are making. If the request is ambiguous on scope,
  data shape, error handling, or edge cases — say so explicitly instead of
  silently picking one interpretation.
- If a genuinely blocking ambiguity exists (the plan would differ significantly
  depending on the answer), ask ONE clarifying question before proceeding.
  Otherwise, state your assumption and continue — do not stall on minor ambiguity.

## Step 2 — Read before you write

- Search the existing codebase for related code, existing conventions, naming
  patterns, and prior art before proposing anything new. Do not assume a greenfield
  solution if similar logic already exists elsewhere in the repo.
- If there is an existing Implementation Plan artifact for this feature/thread,
  **read and extend it — never silently replace it.** Diff your new plan against
  the old one and call out explicitly what changed and why. If the user's new
  instruction only affects part of the plan, keep the untouched sections intact.

## Step 3 — Generate at least two real approaches

For any design decision that has more than one reasonable solution, briefly outline
at least 2 options (not one option plus a strawman). For each option, note:
- What it optimizes for
- The main tradeoff or risk
- Rough implementation cost (small / medium / large)

Pick one and state *why*, in one sentence. Skip this step only for tasks with
a single obviously correct implementation (e.g. "add a null check here").

## Step 4 — Surface edge cases and failure modes

Before finalizing the plan, list:
- Inputs or states that could break the chosen approach
- Anything the change could silently affect elsewhere in the codebase
  (shared functions, callers, tests, config)
- What "done" looks like — how you (or the user) will verify correctness

## Step 5 — Write the Implementation Plan artifact

Structure every plan artifact the same way, so it stays diffable across revisions:

```markdown
## Goal
<one sentence>

## Assumptions
- ...

## Options considered
1. **<name>** — optimizes for X, tradeoff: Y, cost: small/medium/large
2. **<name>** — optimizes for X, tradeoff: Y, cost: small/medium/large

## Chosen approach
<option> — because <reason>

## Steps
1. ...
2. ...

## Risks / edge cases
- ...

## Verification
- ...
```

Stop and wait for the user to comment on or approve this artifact before touching any files.
If the user replies in chat instead of commenting on the artifact directly, treat that
reply as feedback on the **existing** artifact and update it in place — do not generate
a competing new plan.

## Step 6 — Handoff to execution

Once the plan is approved, execution (including fast, mechanical edits) can proceed
under a faster model if the workflow uses a separate implementer agent — this skill only
governs the *planning* phase. See `architect.md` / `implementer.md` custom agents for
a model-routing setup that pairs with this skill.

