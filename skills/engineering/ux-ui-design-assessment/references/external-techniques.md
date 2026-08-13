# External Techniques Adapted Into This Skill

This skill is an original Skill-Agents synthesis. It drew specific techniques from public skills in the [UI Skills](https://www.ui-skills.com/skills/) directory and adapted them to this repository's analyze-and-document workflow. We do not claim these are official or verbatim versions of the upstream skills. See [credits.md](credits.md) for attribution and links.

## From `design-lab` (0xdesign) — the Design-mode loop

**What it does:** an interactive loop — interview the user, compile a structured design brief, generate several meaningfully distinct variants in a temporary lab, collect feedback via an in-browser overlay, synthesize a hybrid if needed, then finalize and clean up.

**What we adapted:**
- The **interview -> brief -> variants -> feedback -> finalize** shape became the 7-step Design mode in [design-workflow.md](design-workflow.md).
- Its **open-ended question discipline** ("never ask leading questions") reinforced our Usability Testing topic.
- Its **variant axes** (information hierarchy, layout model, density, interaction model, expressive direction) became the Ideate guidance.
- Its **quantitative accessibility thresholds** feed the rubric: contrast 4.5:1 text / 3:1 UI, touch targets 44x44px, visible `:focus-visible` (2px ring + offset), motion 150-200ms micro / 200-300ms transitions, respect `prefers-reduced-motion`.
- Its **full component-state list** (default, hover, focus, active, disabled, loading, error, empty) became the Prototype step's state checklist.

**What we deliberately did NOT copy:** the temporary code lab, the `FeedbackOverlay` component, the `.claude-design/` artifacts, and route generation. Those are implementation scaffolding for a code-gen agent; this skill produces a *document*, not a running lab.

## From `ui-ux-pro-max` (nextlevelbuilder) — prioritized guidelines

**What it does:** a searchable database of ~98 UX guidelines in 10 priority categories (CRITICAL -> LOW), plus palettes, font pairings, styles, and 20+ technology stacks.

**What we adapted:**
- The **priority-tiered guideline structure** (Accessibility CRITICAL -> Touch -> Performance -> ... -> Charts LOW) shaped how the rubric orders checks by impact.
- **Concrete numeric rules** became rubric thresholds: contrast 4.5:1, touch 44x44px / 8px spacing, base font 16px, line-height 1.5, animation 150-300ms, CLS < 0.1, bottom navigation <= 5 items.
- Its **anti-pattern list** became Audit fail signals: removing focus rings, icon-only buttons without labels, hover-only states, 0ms instant changes, emoji as icons, fixed px container widths, disabled zoom, text < 12px, gray-on-gray, raw hex in components, animating width/height, placeholder-only labels, errors only at the top.
- Its **forms/navigation guidance** (visible labels, errors near field, helper text, progressive disclosure, predictable back, deep linking) maps to our IA and Usability dimensions.

**What we deliberately did NOT copy:** the large style/palette/font databases and stack-specific implementation snippets. We reference the concept and the numbers, not the bulk data.

## From `improve-ui` (ibelick) — evidence-based auditing

**What it does:** a strict auditor that never mutates code. It traces a rendered surface, reconstructs the local design system, and only reports a finding if it passes a three-part proof gate, then falsifies its own candidates.

**What we adapted:**
- The **three-part evidence gate (Contract / Runtime / Correction)** became the Evidence Rules in [audit-rubric.md](audit-rubric.md). Every Audit finding must cite a principle/contract, prove it reaches the rendered surface, and point to one clear fix.
- The **falsification step** — re-open each source and try to invalidate — is required before reporting.
- Its **"No supported findings" honesty** — if nothing survives falsification, say so rather than inventing problems.
- Its **findings table format** (Problem / Evidence / Proposed change / Scope / Confidence) shaped the report template.

**What we deliberately did NOT copy:** its read-only codebase tracing internals and its `design-plans/` self-contained implementation-plan writer (that role belongs to the `ui-design-engineering` companion skill, which actually implements fixes).

## From `rams` — real-time quality checks

**What it does:** real-time design feedback on accessibility, spacing, typography, contrast, and component quality.

**What we adapted:** the idea of **quantitative, checkable quality bars** for spacing, typography, and contrast, folded into the Color/Typography and Responsive dimensions of the rubric (the shared thresholds above).

## From `web-design-guidelines` (antfu) — compliance review

**What it does:** reviews UI code for web interface guideline compliance, including accessibility and UX best practices.

**What we adapted:** an **accessibility-and-UX compliance checklist mindset** — treat the audit as a pass/fail check against explicit standards (WCAG 2.1 AA, keyboard, semantics, reduced motion) rather than subjective opinion.

## How this skill differs from each upstream skill

| Upstream skill | Its focus | This skill's focus |
|----------------|-----------|--------------------|
| `design-lab` | Generate a running variant lab in code | Produce a design document; no code lab |
| `ui-ux-pro-max` | Lookup database of styles/palettes/rules | Apply the rules as an audit rubric and design method |
| `improve-ui` | Write implementation plans for another agent | Produce a UX/UI assessment report; hand fixes to `ui-design-engineering` |
| `rams` | Real-time editor feedback | One-time documented evaluation |
| `web-design-guidelines` | Code compliance review | UX/UI evaluation across the full 10-topic body of knowledge |

Consult the upstream pages and repositories for authoritative versions and licenses before redistributing their content.
