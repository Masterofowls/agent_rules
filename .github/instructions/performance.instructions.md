---
description: "Use when creating or modifying frontend code where loading speed, rendering, bundle size, images, fonts, or Core Web Vitals matter. Covers web performance best practices."
applyTo: ["**/*.{js,jsx,ts,tsx,css,html}"]
---

# Web Performance Guidelines

- Target good Core Web Vitals at the 75th percentile of real visits: LCP at most 2.5s, INP at most 200ms, and CLS at most 0.1. Use field measurements when available; Lighthouse and profiler results are diagnostic lab evidence, not proof of field INP.
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
- Reduce unused CSS and JS and avoid libraries for tasks the platform already handles. Delete files or dependencies only when necessary and authorized under the agent permissions.

## Performance verification
- Measure production builds with representative devices, network conditions, and data sizes; development mode and warm local caches are not production benchmarks.
- Define project-specific budgets for initial JavaScript, images, requests, memory, and interaction latency. Preserve existing budgets and report regressions rather than silently raising limits.
- Profile the actual bottleneck before memoizing, virtualizing, or moving work to a worker. Preserve accessibility and interaction behavior.
- Load-test backends only in an authorized environment with bounded traffic; examine latency percentiles, error rates, database queries, and resource saturation.
- Verify cleanup after repeated navigation and operations to catch accumulating listeners, requests, and memory.
- Compare before/after measurements alongside functional tests; do not deploy to verify an optimization without permission.
