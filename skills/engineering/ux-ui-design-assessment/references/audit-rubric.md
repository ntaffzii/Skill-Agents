# UX/UI Audit Rubric

Used in **Audit mode**. Evaluate the interface across ten dimensions (the ten topics in [ux-ui-knowledge.md](ux-ui-knowledge.md)). Every rating must be backed by evidence — a `file:line` reference or an observed behavior in the browser. Never guess. See the evidence rules below.

## Severity Scale (matches `ui-design-engineering`)

- `P0` — unusable core flow, severe accessibility barrier, or destructive behavior.
- `P1` — broken interaction, keyboard/focus failure, major responsive overlap, or inaccessible form/dialog.
- `P2` — incomplete state, confusing hierarchy, performance issue, or significant inconsistency.
- `P3` — localized polish issue with low user impact.

## Dimension Rating

For each of the ten dimensions, assign one rating and cite evidence:

| Rating | Meaning |
|--------|---------|
| **Strong** | Clearly supports the user; no notable issues. |
| **Adequate** | Works, but with minor gaps. |
| **Weak** | Notable friction or defects (P1-P2). |
| **Missing** | Absent or broken (P0). |
| **N/A** | Does not apply to this surface (explain why). |

## The Ten Dimensions

### 1. UX/UI Foundations
- Evidence to seek: primary user + task identifiable from the interface; consistent interaction for the same action.
- Fail signals: task not inferable; same action done different ways across screens.

### 2. Design Thinking Evidence
- Evidence to seek: traces that the design came from real user evidence, not a first guess.
- Fail signals: obvious pain points shipped to production; flows that ignore user goals.

### 3. User Research Fit (Persona/Empathy Map)
- Evidence to seek: the product clearly serves a definable user; not over-serving too many segments.
- Fail signals: clutter from trying to please everyone; persona pain points still visible in the UI.

### 4. Information Architecture
- Evidence to seek: sitemap depth, navigation, labeling, taxonomy.
- Fail signals: primary task > ~3 clicks; inconsistent labels; overwhelming choices; nested cards.
- Quantitative: bottom navigation > 5 items; more than ~3 levels for common tasks.

### 5. Wireframe/Mockup/Prototype Integrity
- Evidence to seek: built product still reflects intended structure and priority.
- Fail signals: implementation drift; clutter that lost the original hierarchy.

### 6. Visual Hierarchy and UI Patterns
- Evidence to seek: dominant element per screen; reading pattern matches content density; proximity grouping.
- Quantitative (squint test): hierarchy still visible when blurred or viewed at a distance.
- Fail signals: flat screens; competing elements; primary CTA not the most prominent.

### 7. Color and Typography
- Quantitative thresholds:
  - Body text base ~16px, line-height ~1.5; body text below ~12px is a defect.
  - Contrast >= 4.5:1 for text, >= 3:1 for UI elements/large text (WCAG 2.1 AA).
  - At most 2 font families per screen.
  - Primary action button must outweigh secondary/cancel.
- Fail signals: gray-on-gray text; > 2 fonts; raw hex in components; color-only state signaling.

### 8. Responsive Design
- Quantitative thresholds:
  - Touch targets >= 44x44px.
  - Mobile-first; viewport meta tag present.
  - No horizontal scroll; zoom not disabled; CLS-friendly (reserve space for async media).
- Inspect at: one narrow mobile, one desktop, one wide viewport.
- Fail signals: overlap, overflow, fixed elements covering content, disabled zoom.

### 9. Mood (Moodboard Coherence)
- Evidence to seek: a coherent emotional direction across screens.
- Fail signals: mixed tone; inconsistent mood between sections.

### 10. Usability Testing Readiness
- Evidence to seek: complete states (default/hover/focus/active/disabled/loading/error/empty); unambiguous labels.
- Fail signals: missing states; labels that assume unknown knowledge; copy that leads the user.
- Recommend a usability test for any high-impact, high-uncertainty flow.

## Evidence Rules (adapted from `improve-ui`)

A finding is only valid if it passes a three-part proof gate:

1. **Contract** — cite the principle or threshold being violated (from this rubric or the project's own `DESIGN.md` / design tokens).
2. **Runtime** — prove the issue reaches the rendered surface (cite `file:line` or describe the observed browser behavior on the real route).
3. **Correction** — the evidence must point to one clear fix; if multiple fixes are equally valid, say so rather than guessing intent.

Before reporting, re-open each cited source and try to **falsify** the finding. Drop it if counterevidence shows the difference is valid. If nothing survives, report "No supported findings" for that dimension rather than inventing problems.

## Scoring Summary

Produce a small table in the report:

```text
| # | Dimension              | Rating    | Top severity | Evidence |
|---|------------------------|-----------|--------------|----------|
| 1 | UX/UI Foundations      | Adequate  | P2           | ...      |
| 2 | Design Thinking        | ...       | ...          | ...      |
```

Then list findings grouped by severity (P0 first), each with: title, evidence, impact, proposed fix, and the dimension it belongs to. Hand implementation of fixes to the `ui-design-engineering` skill.
