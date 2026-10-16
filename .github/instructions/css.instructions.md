---
description: "Use when creating or modifying CSS stylesheets. Covers maintainable styles, responsive design, accessibility, and consistent themes."
applyTo: "**/*.css"
---

# CSS Guidelines

- Follow the project's existing styling approach, naming conventions, and formatting.
- Keep styles in the relevant stylesheet and use the project's established component, page, or global stylesheet organization.
- Reuse existing design tokens, variables, and shared styles for colors, spacing, typography, and layout to maintain a consistent theme.
- Prefer class-based selectors with clear, scoped names. Avoid broad selectors and excessive specificity that can cause unintended effects.
- Build responsive layouts using existing breakpoints and layout patterns; avoid fixed dimensions when flexible sizing works.
- Preserve keyboard focus visibility and support reduced-motion preferences when adding interactive or animated styles.
- Avoid unnecessary `!important`, duplicated declarations, and one-off overrides; integrate with the existing cascade.
- Do not add a CSS framework or styling dependency unless requested or required by the project's established approach.
