# Portable Skill.md Pack

This folder contains model-neutral `SKILL.md` files.

Use it when you want skills that can travel across Claude, ChatGPT, Gemini, Codex, local agents, and other MCP-aware agents without depending on this repo's `mcp-tools/` implementation.

## Why This Exists

`mcp-tools/` is executable code. It depends on Python, FastMCP, local packages, machine permissions, and client configuration.

`Skill.md/` is instruction. It should work as a portable behavior layer even when the agent has different tools, different model providers, or no MCP server from this repo.

```text
Skill.md/    = portable model-neutral skills
skills/      = local curated skill library for this repo
workflows/   = ordered playbooks
mcp-tools/   = executable MCP server and tools
data/        = machine-readable registries
```

## Use Cases

- Copy a skill into Claude Code, ChatGPT custom instructions, Gemini Gems, or another agent profile.
- Give a model-neutral operating procedure to an agent that already has its own MCP tools.
- Keep tool names abstract so the same skill works with different clients.
- Build company/team skills without depending on one model vendor.
- Convert a workflow into a reusable behavior pack.

## Design Rule

Portable skills should describe capabilities, not local implementation names.

Good:

```text
Use available file-reading tools to inspect nearby source files.
```

Avoid:

```text
Call mcp-tools/tools/filesystem.py::read_file.
```

## Current Portable Skills

- `universal-agent-operating-system` - general operating rules for any capable agent.
- `model-portability-adapter` - adapt behavior across Claude, ChatGPT, Gemini, Codex, and local agents.
- `tool-agnostic-mcp-routing` - choose tools by capability instead of vendor-specific names.
- `cross-model-handoff` - create handoffs that another model or agent can continue.

## How To Use

Prompt example:

```text
Use the universal-agent-operating-system skill. You may use whatever tools are available in this environment.
```

Prompt example for cross-model use:

```text
Use model-portability-adapter. Rewrite this workflow so it can work in Claude, ChatGPT, Gemini, or a local MCP agent.
```

Prompt example for tool routing:

```text
Use tool-agnostic-mcp-routing. Do not assume exact tool names; map the task to the tools currently available.
```

## Repository Split Recommendation

For a personal repo, keeping `Skill.md/`, `skills/`, `workflows/`, and `mcp-tools/` together is convenient.

For a team or public release, split into two repos:

```text
skill-agents/        = Skill.md, skills, workflows, docs
ai-desk-mcp-tools/   = MCP server, Python tools, requirements
```

Reason:

- Skills change like documentation and behavior policy.
- Tools change like software packages.
- Skills are portable across agents.
- Tools need installation, permissions, dependency updates, and security review.
