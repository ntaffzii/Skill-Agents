# Interaction Craft

Use this reference in **Polish** mode or when reviewing motion, surfaces, type rendering, and icons. It is the detail layer under the Build Rules in `SKILL.md`.

Ground rules:

- Express every fix in the project's existing styling system (Tailwind in a Tailwind project, plain CSS in a CSS project, and so on). Never add a second styling system to apply a polish fix.
- Numbers below are starting points with a reason attached, not laws. If the project's design tokens already express the intent, use the tokens.
- To judge motion, replay it at about 10% speed in the browser's animation tools and walk every state: hover, focus, active, loading, empty, error. What looks off slowed down is subtly wrong at full speed.

## 1. Motion

### Should it animate at all?

Decide by how often the user sees it.

| Frequency | Decision |
| --- | --- |
| Keyboard-triggered or hundreds of times a day (command palette, shortcuts, list navigation) | No animation |
| Many times a day (hover, tab switches) | Remove or shrink drastically |
| Occasional (dialogs, drawers, toasts) | Standard animation |
| Rare or first-time (onboarding, success, celebration) | Delight is allowed |

Every animation needs a stated purpose: spatial continuity, state change, feedback for a press, an explanation, or softening an otherwise jarring change. "It looks nice" on something seen often is not a purpose. When unsure, deleting the motion is a valid fix.

### Timing and easing

- Entering and exiting elements use ease-out (fast start, immediate feedback). `ease-in` on UI delays the moment the user is watching, so treat it as a defect. Built-in keywords are weak; a custom cubic-bezier is usually worth defining once as a token.
- On-screen movement or morphing may use ease-in-out; simple hover and color changes use plain `ease`.
- Keep ordinary UI transitions short (roughly under 300 ms). Dialogs, drawers, sheets, and toasts may run longer; anything else slower than that needs a reason.
- Make deliberate actions (press-and-hold, destructive confirm) slower than system responses, and make exits shorter and softer than enters.

### Origin and starting state

- Popovers, dropdowns, and tooltips scale from their trigger (`transform-origin` at the anchor). Dialogs stay centered.
- Do not animate from `scale(0)`. Start from a slightly smaller scale combined with opacity; nothing in the physical world appears from nothing.
- Press feedback is a small scale-down on `:active`; a button that does not react to a press feels dead.

### Interruptibility

- Use CSS transitions for interactive state (hover, toggle, open/close): they retarget from the current value when the user changes their mind.
- Reserve keyframes for staged sequences that run once. Keyframes restart from zero when interrupted, which is wrong for toasts, toggles, drawers, and anything triggered rapidly.

### Enter and exit choreography

- Stagger only infrequent staged entrances (first page load, a success or empty state), in small semantic chunks with short delays. Never stagger routine, repeated interactions.
- Exits use a small fixed offset plus opacity, not the full container height. Remove immediately when motion adds no information.

### Accessibility and input

- Honor `prefers-reduced-motion` by removing movement while keeping opacity or color changes. Gentler, not necessarily zero.
- Gate hover-only motion behind `@media (hover: hover) and (pointer: fine)` so touch devices do not get stuck hover states.

### Cost

- Animate `transform` and `opacity` first. Layout properties (`width`, `height`, `margin`, `padding`, `top`, `left`) force layout every frame; a measured-height accordion is the usual exception.
- Never write `transition: all` (or Tailwind `transition-all`). List the exact properties that change.
- Add `will-change` only after you see a first-frame stutter, only on `transform`, `opacity`, or `filter`, and never `will-change: all`.
- Name the cause before changing code ("layout property animated", "main thread busy"). "Added will-change, seems smoother" is not a diagnosis, and a fast laptop proves nothing about a mid-range phone.

## 2. Surfaces

- **Concentric radius.** For nested rounded surfaces, outer radius = inner radius + the padding between them. Equal radii on nested elements is one of the most common reasons a UI feels off. When the padding is large (about 24px or more), treat the layers as separate surfaces and pick radii independently.
- **Optical alignment.** When geometric centering looks wrong, align by eye. A button with an icon on one side usually wants slightly less padding on the icon side; play triangles and asymmetric glyphs (arrows, stars, carets) need a small manual shift. Best fix is in the SVG itself, fallback is a 1px nudge.
- **Shadow or border.** For cards, buttons, and containers whose border exists only to suggest depth, prefer a layered, transparent `box-shadow` (a 1px ring plus a soft lift) because it adapts to any background. Keep real borders for dividers, table cells, form-input outlines, and anything that carries structure or state. In dark mode a single faint light ring is usually enough.
- **Images.** A very faint 1px outline in a neutral, low-opacity color keeps pale images from bleeding into a pale background. Do not tint it per image.
- **Hit areas.** The clickable area may be larger than the visible control. Keep targets at least 24×24 CSS px (WCAG 2.2 AA) and aim for about 44px on touch. Extend with padding or a pseudo-element rather than enlarging the visual. Neighbouring targets must not overlap.

## 3. Type rendering

These are rendering details; they never override the project's chosen font family. Do not introduce a new typeface to satisfy a polish pass.

- `text-wrap: balance` for headings and short titles (browsers cap it at a handful of lines). `text-wrap: pretty` for short and medium paragraphs, captions, and list text to avoid a lone last word. Leave very long text and code at the default.
- `font-variant-numeric: tabular-nums` for counters, timers, prices, and number columns that update. Not for static decorative numbers, phone numbers, or version strings. Check the glyph shapes in the chosen font.
- On macOS, apply antialiased font smoothing once at the root, not per element.

## 4. Icons

- Match the icon's stroke weight to the weight of adjacent text; use one stroke weight per icon set on a surface.
- Draw icons with `currentColor` and let CSS drive hover, selected, and disabled states. Strip hard-coded fill and stroke colors on import.
- Outline for the default state, fill for the selected or active state. Animate the swap with opacity and scale rather than toggling visibility.
- Check each icon at the smallest size it renders (often 16px); prefer the icon set's native grid sizes over fractional scaling; use SVG, not raster.
- In RTL layouts flip directional icons (back/forward arrows, chevrons, send) but not logos, checkmarks, clocks, or media controls. Give icon-only controls an accessible name and hide decorative icons from assistive technology.

## 5. Polish review output

Use the P0–P3 format from `SKILL.md`. For polish findings a compact table keeps them scannable:

| Before | After | Why |
| --- | --- | --- |
| `transition: all 300ms` | `transition-property: transform, opacity; duration: 200ms` | Name the properties; avoid unintended transitions |
| Same radius on card and inner image | Inner radius = outer radius − padding | Concentric corners |

Mark which findings were verified in a real browser and which come from reading source only.
