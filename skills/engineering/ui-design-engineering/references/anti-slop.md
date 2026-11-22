# Anti-Slop Gate

Use this reference in **Review** mode, in **Polish** mode, and as the last step of **Build** mode. It is a checklist for catching the tells of machine-made interfaces. It is not a redesign procedure: when the user wants the look reworked, use the Shape and Build modes in `SKILL.md`.

If a separate user-level skill (for example `unslop`) is also active, run this checklist as the verification step and let that skill own the redesign.

## Pick the surface first

The tells differ by surface. Decide which one you are looking at before applying anything below.

- **Marketing surface:** landing page, product page, announcement, portfolio. The page has to persuade and be remembered.
- **Product surface:** dashboard, admin, settings, internal tool. The page has to be scanned, compared, and operated repeatedly. Marketing conventions (big hero, decorative section labels, storytelling copy) are themselves defects here; see "Marketing composition is not used for an operational application" in `ui-audit.md`.

## Three gate tiers

| Tier | Meaning | Handling |
| --- | --- | --- |
| **Floor** | Never ships | Fix before handoff. No waiver. |
| **Reflex** | A default a model falls into | Fix, or keep it with a one-line written reason in the handoff |
| **Finish** | Craft detail | Report; never blocks |

### Floor (all surfaces)

1. Text and non-text contrast pass; focus is visible on every interactive element and appears immediately.
2. Every animation has a `prefers-reduced-motion` fallback, and content is visible with scripting disabled where the page is content-first.
3. No horizontal scroll or clipped content at about 390px wide, and no overlapping elements at tablet and desktop widths.
4. No invented facts: metrics, testimonials, logo walls, customer counts, case studies, or "trusted by" claims that the user or product did not supply. Use a clearly marked placeholder or leave it out.
5. A form never confirms success without actually submitting; a control never looks interactive while doing nothing.
6. Colors and fonts come from the project's tokens (or a small declared extension), not scattered literals.
7. No `transition: all`, and no animated layout properties except a measured-height accordion.

### Reflex: marketing surface

Fix, or justify in the handoff:

- A small "eyebrow" label above every heading.
- Labels, tags, and nav links in tracked (letter-spaced) capitals or small caps.
- One word in a headline set apart by color, italics, or a gradient.
- A purple-to-blue gradient, glow, or glassy blob as the main decoration.
- Cards inside cards, or every section turned into a row of identical rounded cards with an icon tile on top.
- Emoji used as icons, or a hand-drawn fake browser or OS window instead of a real screenshot.
- Meta text glued with middle dots, arrows attached to link text, or decorative pulsing status dots.
- The hero's headline, one supporting sentence, and primary action are not all visible without scrolling at about 1280×800.
- A wall of copy: more than roughly 80 words competing on one screen.
- An email sign-up band at the bottom regardless of what the page is for. The closing section should be the action the visitor came to do.
- Content stretched edge to edge on wide screens instead of a capped, centered measure.

### Reflex: product surface

- A hero, tagline, or illustration where the user expects the working screen.
- Decorative gradients or glow behind data; accent color on every surface instead of on priority.
- Identical stat cards in a row with no hierarchy, or charts with no labels, units, or empty/error states.
- Placeholder or lorem data left in views the user will see; icon tiles with no meaning.
- Motion on keyboard-triggered or high-frequency actions (see `interaction-craft.md`).

### Finish

Run `interaction-craft.md` sections 2–4: concentric radii, optical alignment, shadow versus border, tabular numerals, text wrapping, icon weight.

## Procedure

1. Read the product context and tokens first (see `SKILL.md` workflow step 1). Do not judge against an imagined blank slate.
2. Render the real page with the project's browser tools (`browser`, `playwright`). Capture at least 1280×800 and about 390px wide. For product surfaces also capture the empty, loading, and error states.
3. Walk Floor, then the Reflex list for the surface type, then Finish. Quote the exact element or code for each finding.
4. Fix Floor items, then Reflex items, in one batch. Re-render and re-check once. If a bounded pass cannot resolve something, report it instead of claiming a pass.
5. When subagents are available, have a fresh-context reviewer (one that did not build the page) give the final verdict from the screenshots and the checklist. If not, say that the verdict is from the same context.

## Waiver format

When keeping a Reflex item on purpose, add one line to the handoff: `Kept <item>: <reason tied to this product or audience>`. "It looks nice" is not a reason.

## Handoff

List the surface type, viewports and states captured, Floor result, each Reflex item fixed or waived, and anything unverified (for example "could not render; source-only review").
