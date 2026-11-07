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
- Choose a distinctive font pairing that fits this project's audience and visual direction; do not default to the same font choice for every project or use a generic browser font as the design identity.
- Use free-to-download, legally licensed font files bundled in the repository (prefer optimized WOFF2 or variable WOFF2); do not load fonts from Google Fonts API or another external font API.
- Record or retain the font license and attribution required by its terms. Subset to needed scripts and weights, including Cyrillic when needed, to limit asset size.
- Define font-family tokens in the global design system and use them consistently across components. Keep system fonts only as local fallback stacks.
- Load local fonts with `font-display: swap` and preload only critical fonts; avoid duplicate font files and unnecessary weights.
- Use a modular type scale (for example 1.2-1.25 ratio) with fluid `clamp()` sizes; define `--font-size-*`, `--line-height-*`, `--font-weight-*`.
- Body text 16px minimum, line length 45-75 characters, line height 1.4-1.6.

## Spacing, shape, and elevation
- Use a 4px or 8px spacing scale (`--space-1` ... `--space-12`); no arbitrary margins.
- Keep a small set of radii, borders, shadows, and z-index layers as tokens.
- Keep breakpoints and motion durations/easings as tokens too.

## Components
- Build a small shared set of reusable components (Button, Input, Select, Card, Modal, Tabs, Toast, Nav) and reuse them; do not recreate variants per page.
- Each component folder has its own `Component.jsx` and `styles.css`, using tokens only.
- Define variants (primary, secondary, ghost, danger), sizes (sm, md, lg), and states (hover, focus, active, disabled, loading, error) once, in the component.
- Prefer pre-made accessible components (Radix, React Aria, Ant Design, Material UI) wrapped and themed with the project tokens; see the frontend instructions.
- Use real icons from one consistent icon library; never use emoji or text glyphs as interface icons. Animated icons may be used for clear state changes or feedback when motion is appropriate.
- Components are responsive on their own (container queries) and accept props and `className` for composition.
- Change a design decision in the token or component, never by patching individual pages.
