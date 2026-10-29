---
description: "Use when handling errors and logging: React error boundaries, Sentry, structured server logs, log levels, and safe error responses."
applyTo: ["**/*.{js,jsx,ts,tsx,py}"]
---

# Error handling and logging

## Frontend
- Wrap the app and each major route in an error boundary (`react-error-boundary`) with a friendly fallback and a retry action.
- Boundaries do not catch async or event-handler errors; use `try/catch` with `async/await` there and show an error state.
- Handle loading, empty, and error states in every data view; show actionable messages, never raw errors.
- Report unexpected errors to Sentry (`@sentry/react`) with release, environment, and user ID (no personal data); upload source maps; set `tracesSampleRate` low in production.
- Use route-level `errorElement` with React Router and `error.tsx` in Next.js.

## Backend
- Use one central error handler middleware; throw typed errors (`AppError` with `status`, `code`); never swallow errors silently.
- Log with a structured logger (pino, winston; `structlog` or `logging` JSON in Python), not `console.log`.
- Log one JSON object per line with `level`, `time`, `message`, `requestId`, `userId`, and context; add a request ID to every request and response.
- Levels: `error` for failures needing action, `warn` for recoverable issues, `info` for key events, `debug` only in development.
- Never log passwords, tokens, secrets, or full personal data; redact fields.
- Return safe responses: a stable error code and message to the client, full details only in logs.
- Handle `unhandledRejection` and `uncaughtException`: log, then exit cleanly and let the process manager restart.

## Operations
- Alert on error rate and latency; add health (`/health`) and readiness endpoints.
- Remove temporary debug logging before finishing (see the debugging instructions).
