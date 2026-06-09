# Review PR

## Goal

Review a diff for correctness, regressions, test gaps, and maintainability risks.

## When To Use

Use when the user asks for a review, audit, PR feedback, code scrutiny, or risk assessment.

## Skills

- `code-review`
- `architecture-review`

## Steps

1. Understand intent.
   - Read PR description, issue, user request, or commit message.
   - Identify the expected behavior change.
   - If toolset tools are available, choose a focused review toolset before inspecting broad context.
   - If Git tools are available, inspect status and diff before reviewing.
   - If project tools are available, inspect stack and validation commands.
   - If docs tools are available, read README or relevant docs when the diff touches documented behavior, public APIs, or workflow contracts.
   - If repo-index tools are available, summarize the repo or find related files for changed paths before reviewing cross-file behavior.
   - If package tools are available, inspect manifests and lockfiles when the diff changes dependencies, scripts, build config, or runtime imports.
   - If Docker tools are available, inspect Dockerfile and Compose changes when the diff touches runtime, deployment, services, ports, or CI container setup.
   - If API tools are available, inspect endpoint and OpenAPI changes when the diff touches routes, controllers, API clients, auth, or integration config.
   - If database tools are available, inspect schema objects and migrations when the diff touches data models, persistence logic, queries, or migrations.
   - If Postgres tools are available and a configured DSN is relevant, explain SQL risk and use only read-only inspection.
   - If config tools are available, inspect config and secret hygiene signals when the diff touches env, deployment, or feature flags.
   - If test-inspection tools are available, compare changed source paths with nearby tests.
   - If CI tools are available, inspect workflows, jobs, and validation commands before judging coverage or release risk.
   - If dependency-risk tools are available, inspect dependency risk signals when dependencies changed.
   - If security scanner tools are available, scan for likely secrets, dangerous commands, and env exposure before approval.
   - If GitHub tools are available, inspect workflow metadata or draft PR description text when useful.
   - If GitHub API tools are available and a token is configured, inspect PR metadata, changed files, and check status before final findings.
   - If structured-data tools are available, validate changed JSON/TOML registries or configuration.
   - If browser tools are available, plan UI smoke checks for frontend-facing changes.
   - If browser-page-map tools are available, inspect page structure and interactive elements for frontend-facing changes.
   - If Figma tools are available and the PR claims to implement a design, compare implementation risk against design tokens/components.
   - If Playwright tools are available, capture screenshots or inspect console errors for frontend-facing changes.
   - If Playwright action tools are available, run focused UI interaction checks, console/network failure checks, accessibility snapshots, and persistent-session flows when login or multi-page state matters.

2. Review implementation with `code-review`.
   - Trace changed paths.
   - Check data boundaries, error handling, async behavior, and tests.
   - Report findings first.

3. Use `architecture-review` only if the diff changes boundaries or shared abstractions.
   - Look for coupling, ownership confusion, or awkward seams.

4. Summarize residual risk.
   - Name tests not run or areas not inspected.
   - If validation tools are available, report planned or executed validation commands.
   - If Git control tools are available, do not stage or commit during review unless the user explicitly requests it.
   - If review requires a blocked command, generate a user-run command plan instead of running it.

## Verification

- Findings include file and line references.
- Severity is clear.
- No issue is reported without an actionable failure mode.

## Output

Use review format:

```text
Findings
- [P1] Title - path:line
  Explanation.

Open Questions
- ...

Summary
Brief context only.
```
