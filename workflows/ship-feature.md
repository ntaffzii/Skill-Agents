# Ship Feature

## Goal

Take a feature request from unclear intent to implemented, verified, reviewable code.

## When To Use

Use when the user asks to build, add, modify, or improve product behavior in a codebase.

## Skills

- `grill-with-docs`
- `architecture-review`
- `tdd`
- `code-review`
- `handoff`

## Steps

1. Scope the request with `grill-with-docs`.
   - Identify the user-visible behavior.
   - Define non-goals and the smallest useful version.
   - Record assumptions if the user is not available.

2. Inspect architecture with `architecture-review`.
   - Find entry points, module boundaries, and tests.
   - Choose the smallest change that fits local patterns.
   - If toolset tools are available, recommend a focused toolset before loading broad capabilities.
   - If Git tools are available, capture current status before editing.
   - If project tools are available, inspect stack and suggested commands before implementation.
   - If docs tools are available, build a context bundle from README, docs, architecture notes, and ADRs before changing shared behavior.
   - If repo-index tools are available, summarize the repo, search for feature terms, and find related files before selecting edit targets.
   - If package tools are available, inspect manifests and lockfiles before changing dependency-sensitive code.
   - If Docker tools are available, inspect Dockerfile, Compose services, exposed ports, and planned Docker validation before changing runtime or service behavior.
   - If API tools are available, inspect route files, endpoints, and OpenAPI specs before changing backend or integration behavior.
   - If database tools are available, inspect schema, migrations, and ORM models before changing persistence or data contracts.
   - If Postgres tools are available and the user has configured a DSN, plan read-only queries before inspecting live data.
   - If config tools are available, inspect env keys and secret hygiene before changing config-sensitive behavior.
   - If security scanner tools are available, scan secrets, env exposure, and dangerous commands before committing or releasing.
   - If test-inspection tools are available, map likely tests before choosing validation commands.
   - If CI tools are available, inspect workflows and validation commands so local checks match CI expectations.
   - If backup tools are available, create a snapshot before broad generated rewrites or large multi-file edits.
   - If structured-data tools are available, use them for JSON/TOML registry or config edits.
   - If browser tools are available, plan a local UI smoke check for frontend behavior.
   - If browser-page-map tools are available, map relevant HTML before choosing selectors or reviewing page structure.
   - If Figma tools are available and the request references a design, inspect tokens/components and draft the frontend plan before implementation.
   - If Playwright tools are available, check runtime before live UI inspection or screenshots.
   - If Playwright action tools are available, run click/fill/assert checks, console/network checks, accessibility snapshots, and persistent-session flows for user-facing UI paths.
   - If sandbox tools are available, compile or validate small experiments before patching production files.

3. Implement with `tdd`.
   - Add or update the narrowest useful test first.
   - Confirm red.
   - Implement.
   - Refactor only after green.
   - If validation tools are available, plan validation before running broad checks.

4. Review with `code-review`.
   - Look for regressions, missing tests, edge cases, and unsafe assumptions.
   - Patch issues found during review.
   - Inspect the final diff before handoff.
   - Run the narrowest relevant allowed validation command.

5. Hand off with `handoff`.
   - Summarize changed files, tests run, decisions, and remaining risks.
   - If memory tools are available, save durable decisions or follow-up context that should survive the session.
   - If memory-context tools are available, save typed project decisions or generate a memory handoff.
   - If vector-memory tools are available, search related prior decisions before saving duplicate context.
   - If Git control tools are available and the user asks for a commit, inspect diff/status, stage only intended files, then commit staged changes.
   - If a required step cannot run in sandbox, generate a user-run script and include the exact command in the handoff.

## Verification

- Relevant tests pass.
- The feature works through the intended user path.
- No unrelated refactor was introduced.
- Remaining risks are named.

## Output

End with:

- What changed
- How it was verified
- Files changed
- Risks or follow-up work
