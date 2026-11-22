# Credits And Inspiration

`ui-design-engineering` is an original Skill-Agents synthesis created for this repository's local LLM, MCP, browser-validation, and frontend-development workflow. It is not an official skill from UI Skills and is not a verbatim copy of any upstream skill.

## Directory

- [UI Skills](https://www.ui-skills.com/skills/) by Interface Office provided the discovery directory and taxonomy across accessibility, motion, systems, visual design, interaction, performance, craft, taste, frameworks, testing, and tooling.

## Primary Inspirations

- [Baseline UI](https://www.ui-skills.com/skills/ibelick/baseline-ui/) by Ibelick inspired baseline constraints for primitives, layout stability, typography, motion, and accessibility.
- [Fixing Accessibility](https://www.ui-skills.com/skills/ibelick/fixing-accessibility/) by Ibelick inspired accessibility priority, semantic HTML, keyboard, focus, form-error, and targeted-remediation guidance.
- [Frontend Design](https://www.ui-skills.com/skills/anthropics/frontend-design/) by Anthropic inspired product-specific aesthetic intent and resistance to generic generated interfaces.
- [Interface Design](https://www.ui-skills.com/skills/dammyjay93/interface-design/) by Dammyjay93 inspired domain-first thinking for dashboards, admin panels, SaaS products, hierarchy, density, and signature product details.
- [Impeccable](https://www.ui-skills.com/skills/pbakaus/impeccable/) and its focused modes by Paul Bakaus inspired the enhancement-mode organization: shape, adapt, audit, harden, polish, optimize, and distill.

## Additional Directory Patterns

The directory review also informed these areas:

- `frontend-ui-engineering` and `web-quality-audit` by Addy Osmani: maintainable frontend architecture and broad quality validation.
- `fixing-motion-performance` by Ibelick: compositor-friendly motion and avoidance of layout thrashing.
- `make-interfaces-feel-better` by Jakub Krehel and `emil-design-eng` by Emil Kowalski: interaction polish and production craft.
- `react-doctor` by MillionCo and React best-practice entries by Vercel Labs: framework-aware correctness and performance checks.
- `playwright-cli` by Microsoft and `agent-browser` by Vercel Labs: browser-driven validation rather than source-only confidence.
- `wcag-audit-patterns` by wshobson: structured accessibility auditing.
- Framework-specific skills from Antfu, Svelte, Vue, Remix, Vercel, Three.js, Shadcn, and others: detect the project's framework and preserve its conventions instead of imposing one universal stack.

## Added 2026-11-22: Interaction Craft And Anti-Slop

`interaction-craft.md` and `anti-slop.md` were written fresh in this repository after reading the public skills below. No text or code was copied; the examples, tables, and wording are original. Upstream files change often, so these notes record what was read on that date.

- [make-interfaces-feel-better](https://github.com/jakubkrehel/make-interfaces-feel-better) by Jakub Krehel (MIT) informed the surface, type-rendering, icon, and interruptible-transition guidance, and the "replay at 10% speed" review technique.
- [Emil Kowalski's skills](https://github.com/emilkowalski/skills) (MIT; `emil-design-eng`, `review-animations`, `animation-performance`) informed the animate-or-not frequency decision, easing and duration budgets, transform-origin and starting-scale rules, hover gating, and the "name the cause before fixing" rule for motion performance.
- [Hallmark](https://github.com/Nutlope/hallmark) by Nutlope / Together AI (MIT) informed the Floor / Reflex / Finish gate tiers, the idea of linting rendered output in a real browser, and the fresh-context reviewer. Its themes, scripts, and lint tooling were not adopted. Several of its absolute rules are treated here as surface-dependent Reflex items.
- [Uizze anti-ui-slop](https://github.com/uizze/uizze) was reviewed but contributed no content: it is a derivative of Impeccable plus an optional paid reference service.

Not adopted: Vercel web-design-guidelines (no license declared in the repository), Stageshow (out of scope), UI UX Pro Max (already covered by `ux-ui-design-assessment`).

## Adaptation For Skill-Agents

The following are specific to this repository and are not claims about upstream skills:

- Integration with `skill-runtime.route_request` and `build_agent_context`.
- Use of `frontend-ui` and `design-frontend` toolsets.
- MCP sequencing for project inspection, Figma, code editing, Browser, Playwright, CI, and validation.
- Local LLM Orchestrator guidance for `main-llm-tools`.
- Existing Skill-Agents frontend constraints and browser verification requirements.

Upstream authors retain credit for their own work. Consult their pages and repositories for authoritative versions and licenses before redistributing upstream content.
