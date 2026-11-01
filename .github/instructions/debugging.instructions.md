---
description: "Use when adding debugging, logging, diagnosing errors, or troubleshooting bugs in JavaScript, TypeScript, React, or Python code. Covers structured logging, error context, debug flags, browser and runtime tools, and cleanup."
applyTo: ["**/*.{js,jsx,ts,tsx,py}"]
---

# Debugging Guidelines

- Reproduce the bug first and find the root cause before changing code; confirm the fix by re-running the failing case.
- Add debugging at boundaries where failures happen: API calls, async operations, event handlers, state updates, and data parsing. Log inputs, outputs, and key decisions, not every line.
- Use structured, labeled messages (`console.debug('[Cart] add item', { id, qty })`) with levels (`debug`, `info`, `warn`, `error`); in Python use the `logging` module with `logger.debug(...)` and lazy `%s` formatting instead of `print`.
- Gate verbose logs behind a debug flag or log level (`import.meta.env.DEV`, `process.env.DEBUG`, `logging.DEBUG`) so they never run in production.
- Never log secrets, tokens, passwords, or personal data, and redact sensitive fields before logging objects.
- Handle async failures at the appropriate boundary; catch only to recover, add context, or translate the error. Avoid wrapping every `await` or logging the same failure at every layer. Never swallow errors silently; preserve the original cause when wrapping.
- In React, wrap sections in Error Boundaries and log with `componentDidCatch` or `onCaughtError`; use `useEffect` logs sparingly to trace renders, and remember Strict Mode runs effects twice in development.
- Use `console.table` for arrays of objects, `console.group` for related output, `console.time()`/`console.timeEnd()` for timing, and `console.trace()` for call stacks.
- Prefer the debugger over log spam: set breakpoints, use conditional breakpoints and `debugger` temporarily, and use browser DevTools (Network, Performance, React DevTools Profiler) or `python -m pdb`/`breakpoint()`.
- For network issues, check status codes, request and response payloads, CORS, and timing in the Network tab or server logs before changing code.
- Include correlation context (request ID, user ID without sensitive data) in server logs so failures can be traced across services.
- Make errors actionable: clear messages that state what failed, with the relevant values, and never expose stack traces or internals to end users.
- Remove temporary diagnostics (`debugger`, ad-hoc `console.log`, timing calls) before finishing; keep only intentional, leveled logging.
- Add a regression test for each fixed bug when the project has an established test setup.

## Framework and database diagnostics
- Record the smallest reproducible case, expected result, actual result, and relevant environment before editing. Change one supported hypothesis at a time.
- NestJS: inspect provider registration, module exports, guard and pipe order, and exception mapping before changing application structure.
- Next.js: distinguish server, client, build, and hydration failures; inspect cache behavior and runtime boundaries rather than disabling rendering or caching globally.
- ORM failures: inspect parameterized query shape, constraints, migrations, transaction scope, pool exhaustion, and query timing. Do not enable production payload logging or expose connection strings.
- Keep debug instrumentation opt-in and bounded. Disable SQL parameter logging or redact sensitive values.
- Do not reset databases, remove files, replace dependencies, or rewrite modules to bypass a symptom. Follow agent permissions for destructive and Git operations.
- Verify the original failure is gone and adjacent behavior is preserved; report the commands run and any remaining limitation without claiming untested success.
