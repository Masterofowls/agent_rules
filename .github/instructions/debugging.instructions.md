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
- Always catch async errors with `try`/`catch` around `await`, log the error with context, and rethrow or surface it; never swallow errors silently. Use `error.cause` to preserve the original error.
- In React, wrap sections in Error Boundaries and log with `componentDidCatch` or `onCaughtError`; use `useEffect` logs sparingly to trace renders, and remember Strict Mode runs effects twice in development.
- Use `console.table` for arrays of objects, `console.group` for related output, `console.time()`/`console.timeEnd()` for timing, and `console.trace()` for call stacks.
- Prefer the debugger over log spam: set breakpoints, use conditional breakpoints and `debugger` temporarily, and use browser DevTools (Network, Performance, React DevTools Profiler) or `python -m pdb`/`breakpoint()`.
- For network issues, check status codes, request and response payloads, CORS, and timing in the Network tab or server logs before changing code.
- Include correlation context (request ID, user ID without sensitive data) in server logs so failures can be traced across services.
- Make errors actionable: clear messages that state what failed, with the relevant values, and never expose stack traces or internals to end users.
- Remove temporary diagnostics (`debugger`, ad-hoc `console.log`, timing calls) before finishing; keep only intentional, leveled logging.
- Add a regression test for each fixed bug when the project has an established test setup.
