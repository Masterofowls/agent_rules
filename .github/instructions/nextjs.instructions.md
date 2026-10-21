---
description: "Use when creating or modifying Next.js apps, App Router pages, layouts, route handlers, server actions, or next.config files. Covers server/client boundaries, data fetching, routing, and performance."
applyTo: ["**/{app,pages}/**/*.{js,jsx,ts,tsx}", "**/next.config.{js,mjs,ts}"]
---

# Next.js Guidelines

- Follow the project's router. Prefer the App Router (`app/`) for new work; do not mix in `pages/` patterns unless the project already uses them.
- Use Server Components by default. Add `'use client'` only to components that need state, effects, refs, event handlers, or browser APIs, and keep client components small and as deep in the tree as possible.
- Fetch data in Server Components with `async`/`await` and the built-in `fetch`. Do not fetch in `useEffect` when a server fetch works.
- Use framework conventions: `layout`, `page`, `loading`, `error`, `not-found`, `route` handlers, and Server Actions for mutations.
- Use `next/link`, `next/image`, `next/font`, and the Metadata API instead of raw anchors, `img` tags, manual font loading, or manual head tags.
- Keep secrets and server-only logic out of client components; expose browser variables only with the `NEXT_PUBLIC_` prefix.
- Validate input in Server Actions and route handlers, and handle errors with proper status codes or error boundaries.
- Follow the component folder structure and CSS rules from the React guidelines, and keep styling consistent with the global theme.
- Use the latest stable Next.js conventions supported by the project's version; do not upgrade as an unrelated change.
- Preserve existing routes, caching, and rendering behavior when editing.
