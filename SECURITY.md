# Security Policy

This project is designed for personal AI-agent tooling. Treat all workspace integrations, private notes, email, calendar, chat, finance, and browser data as sensitive.

## Supported Pattern

- Read-only inspection by default.
- Draft-only replies, issue updates, Notion payloads, and sync plans.
- Explicit user-run scripts for actions that should happen outside the agent sandbox.
- Command allowlists and blocked executables in `mcp-tools/config/tool_policy.json`.
- Public-only web capture for social platforms.

## Do Not Add Without Extra Review

- Automatic email sending.
- Automatic chat posting.
- Broad Notion or Obsidian sync.
- Destructive Git operations.
- Mutating database SQL.
- Login bypass, CAPTCHA bypass, paywall bypass, or private social scraping.
- Token printing or unredacted secret reporting.

## Report Or Fix Issues

For personal use, open an issue or patch the repo directly. Before sharing publicly, rotate any tokens that may have touched local config, logs, screenshots, or examples.

## Local Validation

Run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\validate-all.ps1
```

