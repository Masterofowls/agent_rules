---
description: "Use when optimizing code, algorithms, queries, caching, build output, or resource usage in JavaScript, TypeScript, Python, or SQL. Covers measure-first optimization, data handling, caching, and backend efficiency."
applyTo: ["**/*.{js,jsx,ts,tsx,py,sql}"]
---

# Optimization Guidelines

- Measure first: profile or time the real bottleneck before optimizing, and compare before and after. Do not optimize on assumption, and keep code readable unless the gain is measured.
- Choose appropriate data structures and algorithms (maps/sets for lookups, avoid nested loops over large data, avoid repeated work inside loops).
- Do expensive work once: hoist invariants, cache computed results, and avoid redundant parsing, serialization, and copies.
- Run independent async operations concurrently with `Promise.all`/`asyncio.gather`, with a concurrency limit for large batches, and cancel abandoned requests with `AbortController`.
- Cache deliberately: define keys, expiry, and invalidation, use HTTP caching headers for responses, and never cache user-specific or secret data in shared caches.
- Avoid N+1 queries: batch or join, select only needed columns, paginate, and add indexes backed by `EXPLAIN`.
- Stream or chunk large files and payloads instead of loading them fully into memory.
- Compress responses, limit payload sizes, and send only fields the client uses.
- Prevent memory leaks: remove listeners, clear timers, close connections and file handles, and avoid unbounded caches or global collections.
- Keep builds lean: enable minification and tree shaking, analyze bundles, and prefer built-in features over new packages.
- Keep temporary profiling code (`console.time()`/`console.timeEnd()`, profilers) out of committed code once measurement is done.
- Preserve behavior: optimizations must not change results, and add or run tests that cover the optimized path.
