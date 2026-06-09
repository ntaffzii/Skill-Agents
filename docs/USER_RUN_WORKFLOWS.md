# User-Run Workflows

Use `user-runner` when the agent cannot or should not run an action inside the sandbox.

## Pattern

```text
Agent tries safe local action
If blocked or too risky:
  1. Plan the command
  2. Write a user-run script
  3. Explain exactly what it changes
  4. Ask the user to run it manually
  5. Continue after the user reports output
```

## Built-In Scripts

- `github_split` - create `github-ready/Skill-Agents` and `github-ready/ai-desk-mcp-tools`.
- `install_mcp_dependencies` - create `.venv` and install MCP tool dependencies.
- `install_playwright` - install Chromium for Playwright.
- `validate_all` - run all validators and MCP tests.
- `git_publish_skill_agents` - initialize and push the Skill-Agents publish folder.
- `git_publish_mcp_tools` - initialize and push the ai-desk-mcp-tools publish folder.
- `mcp_server_config_hint` - print an MCP server config snippet.

## Run

Generated scripts live in:

```text
user-run-scripts/
```

Run one generated script:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\user-run-scripts\run-validate-all.ps1
```

## Safety

- Review scripts before running them.
- High-risk scripts include git publish or environment-changing actions.
- Scripts should say what they change.
- Scripts should avoid deleting the combined repo unless explicitly requested.
