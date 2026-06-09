# Debug Regression

## Goal

Find and fix a regression with a clear root cause and a durable verification signal.

## When To Use

Use when the user reports a bug, failing test, broken behavior, crash, flaky issue, or performance regression.

## Skills

- `diagnose`
- `tdd`
- `code-review`
- `handoff`

## Steps

1. Reproduce with `diagnose`.
   - Capture the failing command, input, route, UI path, or dataset.
   - Minimize the reproduction.
   - Avoid patching before root cause is plausible.
   - If toolset tools are available, choose a focused debugging toolset before inspecting broad context.
   - If Git tools are available, inspect status and relevant diffs before changing files.
   - If project tools are available, inspect stack and likely test commands.
   - If repo-index tools are available, search error names, feature names, and related files before adding probes or patches.
   - If package tools are available, inspect manifests and lockfiles when the failure may involve versions, scripts, build tools, or runtime packages.
   - If Docker tools are available, inspect Dockerfile, Compose services, ports, and validation plan when the failure may involve containers, local services, CI, or deployment.
   - If API tools are available, inspect endpoints and API config when the failure involves routes, integrations, webhooks, auth, or request/response shape.
   - If database tools are available, inspect schema, migrations, and ORM models when the failure involves persistence, queries, data shape, or migrations.
   - If config tools are available, inspect env/config keys when the failure may be environment-specific.
   - If security scanner tools are available, scan for secret/env/command risks when debugging deployment or automation failures.
   - If test-inspection tools are available, locate nearby tests before adding a regression signal.
   - If CI tools are available, inspect CI jobs and validation commands when the failure appears in automation or differs from local behavior.
   - If backup tools are available, create a snapshot before a risky multi-file rollback or generated patch.
   - If browser tools are available, plan a UI smoke check when the regression is visible in a page.
   - If Playwright tools are available, inspect the live page or capture a screenshot when visual evidence matters.
   - If Playwright action tools are available, reproduce UI regressions with click/fill/assert checks, console/network failure checks, accessibility snapshots, and persistent sessions for stateful flows.
   - If sandbox tools are available, compile or validate a minimized experiment before editing production files.

2. Prove the behavior with `tdd`.
   - Add a regression test when a suitable seam exists.
   - Confirm it fails for the reported reason.
   - If validation tools are available, check the intended test command against policy before running it.

3. Fix the root cause.
   - Keep the change as small as possible.
   - Remove temporary debugging instrumentation.

4. Review with `code-review`.
   - Check edge cases, callers, data shape changes, and test coverage.

5. Hand off with `handoff`.
   - State root cause, fix mechanism, and verification commands.
   - If memory tools are available, save the root cause and durable lesson for future debugging.
   - If memory-context tools are available, save the bug lesson with file links and tags.
   - If Git control tools are available and the user asks for a commit, stage only the fix and regression test before committing.
   - If a required reproduction or environment setup step cannot run in sandbox, generate a user-run script and wait for the user's output.

## Verification

- Original failure no longer occurs.
- Minimized repro no longer fails.
- Regression test passes.
- Broader relevant suite passes when practical.

## Output

End with:

- Root cause
- Fix
- Test or repro used
- Commands run
- Remaining risk
