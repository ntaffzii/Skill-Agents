# UI Audit Checklist

Use this reference for frontend review or final implementation QA.

## 1. Product Fit

- The primary user and task are identifiable from the interface hierarchy.
- Navigation reflects the product's information model.
- Density matches workflow frequency and urgency.
- At least one visual or interaction choice is specific to the domain.
- Marketing composition is not used for an operational application.

## 2. Structure And Layout

- No accidental nested cards or floating-card page sections.
- Fixed-format controls have stable dimensions.
- Long labels and values wrap, truncate, or clamp intentionally.
- Content does not overlap at mobile, tablet, desktop, or wide desktop sizes.
- Fixed elements account for safe areas and do not hide content.
- Empty space supports hierarchy rather than filling a template.

## 3. Components And Interaction

- Native elements or accessible primitives provide keyboard behavior.
- Icon-only controls have accessible names and useful tooltips when unfamiliar.
- Destructive actions require clear confirmation.
- Loading uses a stable skeleton or local progress state.
- Errors appear near the failed action and provide a recovery path.
- Empty states offer one useful next action.
- Binary settings use switches or checkboxes; option sets use the appropriate menu, tabs, or segmented control.

## 4. Accessibility

- Controls, fields, landmarks, headings, lists, and tables use correct semantics.
- Focus is visible, ordered logically, trapped in modal surfaces, and restored on close.
- Labels, help text, errors, `aria-invalid`, and required state are connected.
- Expandable controls expose expanded state and controlled content.
- Dynamic status and critical errors are announced appropriately.
- Text, icons, focus rings, and non-text states have sufficient contrast.
- Images have meaningful or empty alt text as appropriate.
- Reduced-motion preferences are honored.

## 5. Typography And Data

- Type choices support the product tone and remain readable.
- Heading scale matches the size of its container.
- Letter spacing is not used as a generic polish shortcut.
- Data columns and changing numbers use tabular numerals when useful.
- Tables support scanning, alignment, comparison, and responsive overflow.

## 6. Color And Surfaces

- Colors come from project tokens or a deliberate small extension.
- Accent colors indicate priority rather than decorating every surface.
- Semantic colors remain distinct and accessible.
- Elevation changes are subtle and consistent.
- Inputs read as interactive or inset without excessive borders.
- Gradients, glow, blur, and decorative shapes are justified by the product.

## 7. Motion And Performance

- Motion communicates state or spatial change.
- Interaction feedback is brief and does not block action.
- Animation uses compositor-friendly properties where possible.
- No large animated blur/backdrop-filter surfaces.
- Scroll-linked work avoids layout thrashing.
- `will-change` is temporary and local.
- Off-screen loops pause.

## 8. Responsive And Browser QA

- Verify at least one narrow mobile, one desktop, and one wide desktop viewport.
- Check menus, dialogs, forms, tables, sidebars, sticky elements, and long content.
- Test keyboard-only operation and Escape behavior.
- Check browser console and failed network requests.
- Confirm fonts, icons, images, charts, canvas, and media load correctly.
- Capture screenshots when visual comparison or review is part of the task.

## 9. Review Boundaries

- Quote or reference the exact failing code or visible behavior.
- Fix critical usability and accessibility issues before visual polish.
- Prefer targeted changes over unrelated redesigns.
- Do not migrate component libraries unless requested or necessary to fix the behavior.
- Distinguish verified defects from subjective alternatives.

## 10. System Verification

- `skill-runtime` selected `ui-design-engineering` for the task.
- The chosen toolset is `frontend-ui` or `design-frontend` as appropriate.
- Browser/Playwright checks use the real route and application state.
- MCP tools stayed within configured allowed roots and tool policy.
- The final response states viewports, interactions, tests, and visual checks actually performed.
