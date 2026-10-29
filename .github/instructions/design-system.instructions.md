---
description: "Use when defining or using a global design system: design tokens, colors, typography and fonts, spacing, and shared components. Keeps all UI consistent."
applyTo: ["**/*.{jsx,tsx,css}", "src/**/*.{js,ts}"]
---

# Global design system

## Single source of truth
- Keep one design system per project; define all tokens once in a global file (for example `src/styles/tokens.css`) as CSS custom properties.
- Components use only tokens, never raw hex values, pixel sizes, or font names.
- Add a new token only when no existing one fits; do not duplicate near-identical values.
- Document tokens and components briefly in the project (README or a showcase page).

## Colors
- Define a palette of: primary, secondary/accent, neutral scale (50-950), and semantic colors (success, warning, danger, info).
- Name tokens by role (`--color-surface`, `--color-text`, `--color-primary`), not by value (`--blue`).
- Use roughly 60% neutral, 30% secondary, 10% accent; keep accent for actions and emphasis.
- Provide matching light and dark values for every role; check contrast (WCAG AA) on all pairs.
- Use `color-mix()` or token variants for hover, active, and disabled states instead of new hex values.

## Fonts and typography
- Use at most two font families: one for headings, one for body (or one variable font); define them as tokens.
- Prefer variable fonts and self-hosted or system font stacks; load with `font-display: swap` and preload critical fonts.
- Use a modular type scale (for example 1.2-1.25 ratio) with fluid `clamp()` sizes; define `--font-size-*`, `--line-height-*`, `--font-weight-*`.
- Body text 16px minimum, line length 45-75 characters, line height 1.4-1.6.
- Do not use default browser or overused generic fonts as the only identity of a design.

## Spacing, shape, and elevation
- Use a 4px or 8px spacing scale (`--space-1` ... `--space-12`); no arbitrary margins.
- Keep a small set of radii, borders, shadows, and z-index layers as tokens.
- Keep breakpoints and motion durations/easings as tokens too.

## Components
- Build a small shared set of reusable components (Button, Input, Select, Card, Modal, Tabs, Toast, Nav) and reuse them; do not recreate variants per page.
- Each component folder has its own `Component.jsx` and `styles.css`, using tokens only.
- Define variants (primary, secondary, ghost, danger), sizes (sm, md, lg), and states (hover, focus, active, disabled, loading, error) once, in the component.
- Prefer pre-made accessible components (Radix, React Aria, Ant Design, Material UI) wrapped and themed with the project tokens; see the frontend instructions.
- Components are responsive on their own (container queries) and accept props and `className` for composition.
- Change a design decision in the token or component, never by patching individual pages.
