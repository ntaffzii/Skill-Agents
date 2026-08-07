# Operational Guide for AI Agents — {{PROJECT_NAME}}

## Build, Test & Lint Commands

```bash
# Build
{{package_manager}} run build

# Test
{{package_manager}} run test
{{package_manager}} run test:e2e

# Lint & Format
{{package_manager}} run lint
{{package_manager}} run format
```

## Directory Structure & Conventions

- Source code lives in `src/`
- Component naming: PascalCase for components (`Button.tsx`), camelCase for utility files/hooks (`useAuth.ts`)
- Component modularity: Keep UI primitives in `src/components/ui/` and domain features in `src/components/features/`

## Hard Constraints

1. **No direct DOM mutations**: Always use component state / frameworks logic.
2. **Strict TypeScript**: Do not use `any` type casting without explicit comment explanation.
3. **No Emoji in UI**: Use Lucide Icons (`lucide-react` / inline SVGs) for visual indicators.
4. **Token Efficiency**: Omit facts inferable from code; keep instructions concise.
