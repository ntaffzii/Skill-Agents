# Contributing

This repo is a personal-first AI agent skill and MCP tool system. Contributions should keep the same shape: focused skills, narrow tools, clear workflows, and safety-first defaults.

## Principles

- Put behavior guidance in `skills/` or `Skill.md/`.
- Put ordered multi-step jobs in `workflows/`.
- Put executable actions in `mcp-tools/tools/`.
- Register every tool group in `data/tools.json`.
- Register broad job profiles in `data/toolsets.json`.
- Prefer read-only, plan-only, or draft-only behavior for private services.
- Do not add tools that send email, post chat messages, mutate Notion, or modify issue trackers without explicit confirmation and policy coverage.

## Add A Skill

1. Create `skills/<bucket>/<skill-name>/SKILL.md`.
2. Include only `name` and `description` in frontmatter.
3. Keep the body concise and procedural.
4. Add references only when the skill needs detailed docs.

## Add A Tool

1. Add a narrow module in `mcp-tools/tools/`.
2. Expose functions through `register(mcp)`.
3. Return structured dictionaries.
4. Add the module to `mcp-tools/tools/__init__.py`.
5. Add registry metadata in `data/tools.json`.
6. Add tests in `mcp-tools/tests/`.
7. Run validation.

## Validate

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\validate-all.ps1
```

With explicit Python:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\validate-all.ps1 -Python 'C:\path\to\python.exe'
```

