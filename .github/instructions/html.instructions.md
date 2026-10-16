---
description: "Use when creating or modifying HTML documents or templates. Covers semantic structure, accessibility, forms, and safe markup."
applyTo: "**/*.html"
---

# HTML Guidelines

- Follow the project's existing document structure, formatting, and template conventions.
- Use semantic elements that reflect the content and purpose of each region; maintain a logical heading hierarchy.
- Associate form controls with visible labels, use appropriate input types, and expose validation feedback accessibly.
- Provide meaningful alternative text for informative images; use empty alternative text for decorative images.
- Prefer native HTML elements and behavior. Add ARIA only when native semantics are insufficient, and ensure interactive elements are keyboard accessible.
- Escape or safely render untrusted content using the project's established templating practices.
- Keep markup concise and avoid deprecated elements, unnecessary wrappers, and inline styles when project stylesheets are used.
- Preserve valid document structure and include required metadata and accessibility attributes for the surrounding project.
