# Workflows

Workflows are ordered playbooks. A skill teaches the agent how to do one kind of task; a workflow tells the agent which skills to combine, in what order, to finish a larger job.

Use workflows when the request needs multiple phases, such as planning, implementation, review, verification, and handoff.

## Workflow Format

Each workflow file should include:

- Goal
- When to use
- Required skills
- Steps
- Verification
- Output

The same workflows are indexed in `../data/workflows.json` so tools or agents can browse them programmatically.

## Current Workflows

- `ship-feature.md`
- `debug-regression.md`
- `review-pr.md`
- `obsidian-vault-cleanup.md`
- `create-new-skill.md`
- `build-mcp-tool.md`
- `research-report.md`
- `daily-personal-agent.md`
- `personal-knowledge-sync.md`
