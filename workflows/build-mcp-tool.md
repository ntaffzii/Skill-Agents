# Build MCP Tool

## Goal

Turn a repeated executable action into a clean MCP tool and connect it to the right skills and workflows.

## When To Use

Use when the user asks to create, refactor, expose, document, or organize MCP tools.

## Skills

- `mcp-tool-management`
- `skill-management`
- `code-review`
- `handoff`

## Steps

1. Classify with `mcp-tool-management`.
   - Decide whether the request belongs in a skill, workflow, or tool.
   - Identify the right tool group.
   - If docs tools are available, inspect MCP README, policy notes, and existing tool registry before designing the contract.
   - If external MCP catalog tools are available, compare community patterns before deciding the local contract.
   - If package tools are available, inspect current dependencies before adding a new runtime requirement.
   - For web scraping/capture tools, design provider adapters and public-only safety limits before adding platform-specific behavior.
   - If sandbox restrictions block install, copy, browser setup, or publish steps, use user-runner tools to generate scripts instead of hiding the blocked action in tool code.

2. Define the contract.
   - Tool name
   - Inputs
   - Output shape
   - Error behavior
   - Safety constraints
   - Provider fallback behavior, if the tool can run against multiple backends.

3. Implement the tool.
   - Keep the action narrow.
   - Return structured data.
   - Avoid broad hidden workflows.

4. Connect the tool.
   - Update `data/tools.json`.
   - Update `data/toolsets.json` when the tool belongs in a curated job profile.
   - Confirm registry/introspection tools can see the new group.
   - Update related workflows when the tool changes a workflow phase.
   - Update related skills only when the agent needs new behavior guidance.
   - If structured-data tools are available, validate and patch registry/toolset JSON through structured paths.

5. Review with `code-review`.
   - Check failures, unsafe inputs, validation, and missing tests.
   - If MCP security audit tools are available, classify risk and confirm policy coverage for the new or changed tool group.
   - If the tool reads SaaS, database, browser, finance, or social data, verify auth behavior, public/private boundaries, and read-only defaults.
   - If user-runner scripts are generated, validate the scripts and report their risk level.

6. Hand off with `handoff`.
   - Summarize the contract, files changed, and verification.
   - If memory tools are available, save durable tool design decisions for future maintenance.

## Verification

- The MCP server can load.
- The tool can be called with a simple valid input.
- Invalid input fails clearly.
- `data/tools.json` points to real modules.
- Runtime registry lists the new tool group.

## Output

End with:

- Tool added or changed
- Contract
- Connected skills/workflows
- Verification commands
