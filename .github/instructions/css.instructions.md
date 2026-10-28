---
description: "Use when creating or modifying CSS stylesheets. Covers maintainable styles, responsive design, accessibility, and consistent themes."
applyTo: "**/*.css"
---

# CSS Guidelines

- Follow the project's existing styling approach, naming conventions, and formatting.
- Keep styles in the relevant stylesheet and use the project's established component, page, or global stylesheet organization.
- Prefer individual component styles over global styles: put a component's styles in its own `styles.css` inside the component folder, scoped by a component-specific class prefix (or CSS Modules when the project uses them).
- Reserve global stylesheets for design tokens (CSS variables), resets, base element and typography styles, and layout shared by the whole app. Do not add component-specific rules to global files.
- Reuse existing design tokens, variables, and shared styles for colors, spacing, typography, and layout to maintain a consistent theme.
- Follow one color scheme and one set of design patterns across every component in the project. Define the palette once as CSS custom properties in the global stylesheet (for example `--color-primary`, `--color-surface`, `--color-text`, `--color-border`, plus semantic `--color-success`, `--color-warning`, `--color-danger`) and use only those variables in component styles.
- Never hard-code colors, font sizes, spacing, radii, shadows, or z-indexes in component CSS; use shared tokens (`--space-*`, `--radius-*`, `--shadow-*`, `--font-size-*`, `--z-*`) so a single change updates the whole project.
- Keep patterns consistent: the same button, input, card, modal, and form styles, states (hover, focus, active, disabled), spacing scale, and border radius everywhere. Reuse an existing component or pattern before creating a new variant.
- Support light and dark themes through token overrides (`[data-theme='dark']` or `prefers-color-scheme`), not duplicated component rules, and keep text contrast at WCAG AA (4.5:1 for body text).
- Always implement adaptive design: build mobile-first with `min-width` media queries, and verify at phone, tablet, laptop, and wide-desktop widths.
- Define breakpoints once (for example 480, 768, 1024, 1280px) and reuse them; prefer container queries (`@container`) for components that live in different layout contexts.
- Use flexible layout tools: Flexbox, CSS Grid (`repeat(auto-fit, minmax(...))`), `gap`, `clamp()` for fluid type and spacing, relative units (`rem`, `em`, `%`, `vw`, `dvh`), `max-width`, and `aspect-ratio`; avoid fixed pixel widths and heights.
- Make media, tables, and long text adapt: `max-width: 100%` for images and video, allow text wrapping, and make wide tables scroll within their own container instead of the page.
- Size touch targets at least 44x44px on small screens, avoid hover-only interactions, and respect safe areas (`env(safe-area-inset-*)`) and `prefers-reduced-motion`.
- Prevent horizontal scrolling at every viewport width, and test with browser device emulation before finishing.
- Prefer class-based selectors with clear, scoped names. Avoid broad selectors and excessive specificity that can cause unintended effects.
- Build responsive layouts using existing breakpoints and layout patterns; avoid fixed dimensions when flexible sizing works.
- Preserve keyboard focus visibility and support reduced-motion preferences when adding interactive or animated styles.
- Avoid unnecessary `!important`, duplicated declarations, and one-off overrides; integrate with the existing cascade.
- Do not add a CSS framework or styling dependency unless requested or required by the project's established approach.
