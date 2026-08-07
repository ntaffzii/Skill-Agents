---
tokens:
  colors:
    primary: "#2563eb"
    primary-hover: "#1d4ed8"
    secondary: "#64748b"
    background: "#f8fafc"
    surface: "#ffffff"
    text-primary: "#0f172a"
    text-secondary: "#475569"
    border: "#e2e8f0"
    success: "#16a34a"
    warning: "#d97706"
    error: "#dc2626"
  typography:
    font-sans: "'Inter', sans-serif"
    font-mono: "'JetBrains Mono', monospace"
    base-size: "16px"
  spacing:
    xs: "4px"
    sm: "8px"
    md: "16px"
    lg: "24px"
    xl: "32px"
  breakpoints:
    mobile: "0px"
    tablet: "768px"
    desktop: "1024px"
    wide: "1280px"
  z-index:
    dropdown: 1000
    sticky: 1020
    modal: 1050
    tooltip: 1080
---

# Design Specification — {{PROJECT_NAME}}

> **Hard Rule — NO Emoji in UI-facing files or components.**
> Use Lucide Icons or named inline SVGs instead.

## Design Rationale

- **Aesthetics**: Clean, modern, high contrast, readable typography.
- **Theme**: Light mode primary with support for dark mode variables.

## Component Standards

- **Buttons**: Focus ring must be visible on keyboard tab (`:focus-visible`).
- **Icons**: Always reference Lucide icons by name (e.g. `CheckCircle`, `AlertTriangle`).
- **Form Inputs**: Distinct border colors for default, focus, hover, and error states.

## Accessibility (a11y)

- Color contrast ratio must satisfy WCAG AA standards (>= 4.5:1 for normal text).
- All interactive controls must be focusable via `Tab` key.
