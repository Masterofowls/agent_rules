---
description: "Use when handling errors and logging: React error boundaries, Sentry, structured server logs, log levels, and safe error responses."
applyTo: ["**/*.{js,jsx,ts,tsx,py}"]
---

# Error handling and logging

## Frontend
- In React, use the framework's existing error boundaries or the installed boundary implementation where recovery is useful. Do not add `react-error-boundary` just to satisfy this rule.
- Boundaries do not catch async or event-handler errors; use `try/catch` with `async/await` there and show an error state.
- Handle loading, empty, and error states in every data view; show actionable messages, never raw errors.
- Use the project's approved error-reporting service with release and environment context. Do not introduce Sentry or another external service, upload source maps, or send user identifiers without approval and a data-handling policy.
- Use route-level `errorElement` with React Router and `error.tsx` in Next.js.

## Backend
- Use one central error handler middleware; throw typed errors (`AppError` with `status`, `code`); never swallow errors silently.
- Use the existing structured logger (or standard-library logging); do not add logging packages solely to satisfy this rule.
- For services, log structured entries with level, time, message, and request correlation where available. Omit user identifiers unless the project's data-handling policy explicitly permits them.
- Levels: `error` for failures needing action, `warn` for recoverable issues, `info` for key events, `debug` only in development.
- Never log passwords, tokens, secrets, or full personal data; redact fields.
- Return safe responses: a stable error code and message to the client, full details only in logs.
- Handle `unhandledRejection` and `uncaughtException`: log, then exit cleanly and let the process manager restart.

## Operations
- Configure error-rate alerts, health, and readiness endpoints when service operations are in scope; do not add infrastructure during a narrow code change.
- Remove temporary debug logging before finishing (see the debugging instructions).
