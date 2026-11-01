---
description: "Use when planning or running QA, acceptance testing, smoke tests, regression checks, exploratory testing, or release verification."
applyTo: ["**/{tests,e2e,playwright,__tests__}/**", "**/*.{test,spec}.{js,jsx,ts,tsx}", "**/test_*.py", "**/*_test.py"]
---

# QA testing

- Start from the requested behavior and acceptance criteria. Define expected results for the changed feature and its adjacent flows before testing.
- Use the existing test tools and environment; prioritize critical paths and risky changes rather than testing every surface indiscriminately.
- Test happy paths, invalid and boundary inputs, loading/empty/error states, retries, cancellation, and duplicate submissions where applicable.
- Verify authentication, roles, ownership, and tenant isolation with separate test users. Use synthetic data and an isolated database, never real customer credentials.
- Check direct navigation, deep links, refresh, back/forward history, and persistence after reload.
- For UI changes, test supported browsers, mobile and desktop layouts, keyboard navigation, focus, reduced motion, and relevant locales. Use the existing accessibility and Playwright instructions.
- Inspect browser console and network failures as well as visible output. A successful screenshot or HTTP 200 alone does not prove the feature works.
- Keep automated tests deterministic with isolated state, controlled time, and scoped network mocks. Do not hide flaky failures with sleeps, retries, or weakened assertions.
- Use approved visual baselines and inspect differences; never regenerate screenshots solely to make tests pass.
- Reproduce defects, record concise steps and expected/actual results, fix the cause, and rerun the original case plus focused regression checks.
- Keep test artifacts scoped and redact sensitive data. Report checks run, failures, and untested limitations in the task reply; do not create unsolicited report files.
- QA authorization does not permit production load tests, destructive operations, deployment, commits, pushes, or branch changes. Obtain the required explicit permission.
