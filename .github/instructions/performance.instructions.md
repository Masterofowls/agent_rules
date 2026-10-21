---
description: "Use when creating or modifying frontend code where loading speed, rendering, bundle size, images, fonts, or Core Web Vitals matter. Covers web performance best practices."
applyTo: ["**/*.{js,jsx,ts,tsx,css,html}"]
---

# Web Performance Guidelines

- Target good Core Web Vitals: LCP under 2.5s, INP under 200ms, CLS under 0.1. Verify with Lighthouse, DevTools, or the React Profiler rather than guessing.
- Split code by route and heavy feature with `React.lazy`, `Suspense`, or dynamic `import()`; keep the initial bundle small.
- Import only what is used (named imports, no whole-library imports) so tree shaking works, and check bundle size before adding a dependency.
- Serve images in modern formats (WebP/AVIF), with explicit `width` and `height`, `loading="lazy"` below the fold, `fetchpriority="high"` on the LCP image, and responsive `srcset`/`sizes`.
- Self-host fonts, use `font-display: swap`, preload only critical fonts, and limit weights and families.
- Prevent layout shift: reserve space for images, embeds, ads, and async content.
- Avoid long main-thread tasks: defer non-critical work with `requestIdleCallback`, `setTimeout`, or Web Workers; use `defer`/`async` on scripts.
- Debounce or throttle frequent events (scroll, resize, input), and use passive listeners for scroll and touch.
- Virtualize long lists and paginate or stream large data instead of rendering everything.
- In React, avoid creating new objects, arrays, or functions in props of memoized children, keep state close to where it is used, and clean up effects, timers, and listeners.
- Animate with `transform` and `opacity`, avoid layout-triggering properties, and respect `prefers-reduced-motion`.
- Use HTTP caching with hashed asset filenames, compression (gzip/Brotli), and `preconnect` to critical origins.
- Remove unused CSS, JS, and dependencies; do not add libraries for tasks the platform already handles.
