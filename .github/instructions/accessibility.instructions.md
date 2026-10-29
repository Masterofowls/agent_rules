---
description: "Use when building or reviewing UI for accessibility (a11y): semantic HTML, ARIA, keyboard navigation, focus management, labels, alt text, contrast, and axe-style audits."
applyTo: ["**/*.{jsx,tsx,html,css}", "src/**/*.{js,ts}"]
---

# Accessibility (a11y)

## Semantic HTML first
- Use native elements: `button`, `a`, `nav`, `main`, `header`, `footer`, `section`, `ul`, `table`, `form`, `dialog`; never a clickable `div`/`span`.
- One `h1` per page; headings follow order without skipping levels.
- Use landmarks (`main`, `nav`, `aside`) and a "skip to content" link.
- Links navigate, buttons act; links have meaningful text (no "click here").

## ARIA only when needed
- Native semantics beat ARIA; add ARIA only when no native element fits.
- Never change native roles needlessly; no `role="button"` on a `button`.
- Use `aria-label` or `aria-labelledby` for unlabeled controls, `aria-expanded`/`aria-controls` for toggles, `aria-live="polite"` for async status, `aria-current="page"` for active nav.
- Hide decorative content with `aria-hidden="true"`; never hide focusable elements.

## Keyboard and focus
- Everything interactive works with the keyboard: Tab, Shift+Tab, Enter, Space, Escape, arrow keys for composite widgets.
- Keep a logical tab order from DOM order; avoid positive `tabindex`.
- Always show `:focus-visible` styles with enough contrast; never `outline: none` without a replacement.
- Modals and dialogs trap focus, close on Escape, and return focus to the trigger; prefer `<dialog>` or Radix/React Aria.
- Move focus to the new content or heading after route changes and form errors.

## Labels, alt text, forms
- Every input has a visible `label` tied by `htmlFor`/`id`; placeholders are not labels.
- Group related fields with `fieldset` and `legend`; mark required fields in text and with `required`.
- Show errors next to fields, link them with `aria-describedby`, and announce them; do not rely on color alone.
- Informative images get descriptive `alt`; decorative images use `alt=""`; icon-only buttons get an accessible name.
- Videos have captions; audio has transcripts; no autoplay with sound.

## Visual
- Contrast at least 4.5:1 for text and 3:1 for large text and UI parts; support 200% zoom and text resize without loss.
- Do not convey meaning by color only; respect `prefers-reduced-motion` and `prefers-color-scheme`.
- Touch targets at least 44x44px; set `lang` on `html`.

## Testing
- Run axe (`@axe-core/playwright`, `eslint-plugin-jsx-a11y` equivalents in Oxlint) and Lighthouse accessibility audits; fix all serious and critical issues.
- Test by keyboard only and with a screen reader (NVDA, VoiceOver) on key flows.
