# Template Usage Guide — project-docs-prep

This reference document explains how an AI coding agent should utilize the skeleton templates in `templates/` when generating documentation for a new or existing software project.

## Structure Overview

The output documentation set is split into two operational layers:

### 1. Spec Layer (`docs/`)
- `docs/01-project-overview.md`: High-level goals, problems, target users, and success metrics.
- `docs/02-system-requirements.md`: Functional and non-functional requirements (NFRs).
- `docs/03-tech-stack-architecture.md`: Selected technologies, directory structure, architecture diagrams.
- `docs/04-system-modeling.md`: ERD diagrams, data schemas, API contracts, sequence diagrams.
- `docs/05-ux-ui-design.md`: Design principles, screen inventory, user flows, accessibility guidelines.

### 2. Operational Layer (Root)
- `AGENTS.md`: Agent operational rules, build/test/lint commands, directory conventions.
- `DESIGN.md`: Design tokens (YAML front matter) and component styling rules.
- `CLAUDE.md`: Lightweight pointer file for Claude Code runtime.
- `README.md`: Concise human-facing project overview.

## Generation Rules

1. **Placeholders**: Replace all `{{...}}` markers with project-specific facts derived from the user's prompt or requirements.
2. **Unconfirmed NFRs**: If performance numbers or SLA metrics are unknown, use `> ⚠️ TODO: confirm target NFR` rather than making up stats.
3. **No Emoji Rule**: Ensure `docs/05-ux-ui-design.md` and `DESIGN.md` use Lucide Icons or named SVGs. **Never use emoji as UI elements**.
4. **Token Efficiency**: Keep operational files (`AGENTS.md`, `DESIGN.md`, `CLAUDE.md`) in English and dense. Omit standard boilerplate that can be directly inferred from code.
