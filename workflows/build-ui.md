# Frontend Interface

Use this workflow to design, implement, harden, or substantially improve a frontend interface.

## 1. Discover

- Identify the user, primary task, product domain, route, framework, component system, and existing design conventions.
- Inspect related screens and reusable primitives before proposing a direction.
- Use the `frontend-ui` toolset; add `design-frontend` when Figma or design mapping is involved.

## 2. Shape

- Define information hierarchy, density, responsive behavior, interaction states, and one product-specific signature.
- Name generic defaults to avoid.
- Preserve existing product behavior and technical boundaries.

## 3. Implement

- Build the complete working experience using existing project patterns.
- Include loading, empty, error, disabled, focus, selected, success, and edge-case states where relevant.
- Keep accessibility and responsive behavior part of implementation, not a later patch.

## 4. Validate

- Run focused lint, typecheck, tests, and build checks.
- Use Browser or Playwright on the actual route at mobile and desktop viewports.
- Verify keyboard interaction, focus, overflow, long content, console errors, and rendered assets.

## 5. Review And Hand Off

- Apply `ui-design-engineering` review mode before completion.
- Report changed files, behavior, verification, and residual risks.
