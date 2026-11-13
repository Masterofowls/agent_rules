---
description: "Use when creating or modifying Next.js apps, App Router pages, layouts, route handlers, server actions, or next.config files. Covers server/client boundaries, data fetching, routing, and performance."
applyTo: ["**/{app,pages}/**/*.{js,jsx,ts,tsx}", "**/next.config.{js,mjs,ts}"]
---

# Next.js Guidelines

Apply these rules only when the project uses Next.js, confirmed by dependencies, imports, or configuration. An `app/` or `pages/` folder alone is not evidence; keep other frameworks' routing and rendering conventions.

- Follow the project's router. Prefer the App Router (`app/`) for new work; do not mix in `pages/` patterns unless the project already uses them.
- Use Server Components by default. Add `'use client'` only to components that need state, effects, refs, event handlers, or browser APIs, and keep client components small and as deep in the tree as possible.
- Fetch data in Server Components with `async`/`await` and the built-in `fetch`. Do not fetch in `useEffect` when a server fetch works.
- Use framework conventions: `layout`, `page`, `loading`, `error`, `not-found`, `route` handlers, and Server Actions for mutations.
- Use `next/link`, `next/image`, `next/font/local`, and the Metadata API where appropriate. Bundle font files and licenses in the repository; do not use build-time font downloads or external font APIs.
- Keep secrets and server-only logic out of client components; expose browser variables only with the `NEXT_PUBLIC_` prefix.
- Validate input in Server Actions and route handlers, and handle errors with proper status codes or error boundaries.
- Follow the component folder structure and CSS rules from the React guidelines, and keep styling consistent with the global theme.
- Use the latest stable Next.js conventions supported by the project's version; do not upgrade as an unrelated change.
- Preserve existing routes, caching, and rendering behavior when editing.

## Server boundaries and mutations
- Authenticate and authorize every Server Action and route handler independently; a hidden UI control or protected parent layout is not sufficient.
- Keep database clients, credentials, and privileged helpers in server-only modules. Pass only serializable, explicitly selected data to Client Components.
- Validate mutation inputs and surface expected failures through the existing form or API error contract. Revalidate affected data only after a successful mutation.
- Use request APIs (`cookies`, `headers`, route `params`, and `searchParams`) according to the installed version, including asynchronous access when required.
- Do not catch framework redirect or not-found control flow as an ordinary application failure.

## Rendering, caching, and testing
- Make caching decisions explicit for the installed Next.js version. Never share personalized or tenant-specific responses through a public cache.
- Use supported revalidation and cache-tag APIs; test both fresh and invalidated data instead of assuming framework defaults.
- Avoid hydration mismatches from random values, time, browser globals, or locale-dependent rendering. Do not use `suppressHydrationWarning` as a general fix.
- Keep URL state, loading boundaries, errors, metadata, and redirects consistent across direct navigation and client navigation.
- Use the runtime supported by the database driver and dependencies; do not move Node-only code to an Edge runtime.
- Validate production builds and critical routes with the existing checks. Use the project's configured linter rather than assuming a `next lint` command exists.
