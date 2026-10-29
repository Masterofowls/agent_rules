---
description: "Use when designing or building UI: mobile-first, adaptive, fluent, modern, and unique visual design. Covers layout, responsiveness, motion, depth, and avoiding generic templated looks."
applyTo: ["**/*.{jsx,tsx,css,html}", "src/**/*.{js,ts}"]
---

# Design

## Mobile-first and adaptive
- Design the smallest screen first, then enhance with `min-width` breakpoints; never hide core features on mobile.
- Adapt layout per device class (phone, tablet, desktop), not only scale it: change navigation, columns, and density.
- Use fluid sizing (`clamp()`, `%`, `fr`, `rem`), `auto-fit`/`minmax()` grids, and container queries.
- Touch targets at least 44x44px; keep primary actions in thumb reach on mobile.
- Support portrait and landscape, safe areas (`env(safe-area-inset-*)`), and `100dvh` instead of `100vh`.
- Support keyboard, mouse, touch, and screen readers; use `hover` and `pointer` media queries for input differences.
- Test at 320, 375, 768, 1024, 1440px and with zoom at 200%.

## Fluent design
- Use light, depth, motion, material, and scale deliberately: subtle layered surfaces, soft shadows, and optional translucency (`backdrop-filter`) with a solid fallback.
- Give every interaction immediate feedback: hover, focus, pressed, loading, success, and error states.
- Keep motion short (150-300ms), purposeful, and eased; honor `prefers-reduced-motion`.
- Keep a clear visual hierarchy: one primary action per view, consistent spacing rhythm, generous whitespace.

## Modern design
- Prefer clean layouts, strong typography, consistent radii, and restrained color over decoration.
- Use modern CSS: Grid, `gap`, `clamp()`, `aspect-ratio`, `:has()`, `color-mix()`, logical properties, and view transitions when supported.
- Use SVG or icon libraries for icons; use optimized images (`webp`/`avif`) with `loading="lazy"`.
- Support light and dark themes through `prefers-color-scheme` and tokens.

## Unique design
- Pick one clear visual direction per project (tone, shape language, type pairing, signature accent) and apply it everywhere.
- Avoid generic AI/template looks: default purple gradients, identical card grids, stock hero layouts, emoji as icons, and filler copy.
- Add a few distinctive details (custom illustration style, a signature layout, thoughtful micro-interactions) without hurting usability or performance.
- Use real content and realistic data in designs, not lorem ipsum.
- Use the installed design skills (`frontend-design`, `design-taste-frontend`, `no-ai-design-slop`) to check originality before finishing.

## Accessibility
- Contrast at least 4.5:1 for text and 3:1 for large text and UI parts.
- Visible `:focus-visible` styles; never remove outlines without a replacement.
- Never convey meaning by color alone.
