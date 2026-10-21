---
description: "Use when creating or modifying Playwright end-to-end tests, page objects, fixtures, or playwright.config files. Covers locators, assertions, waiting, isolation, and reliable browser tests."
applyTo: ["**/playwright.config.{js,ts,mjs}", "**/{e2e,playwright}/**/*.{js,ts}", "**/*.e2e.{js,ts}", "**/tests/**/*.spec.{js,ts}"]
---

# Playwright Guidelines

- Follow the project's existing Playwright layout, configuration, and language (`@playwright/test`), and keep end-to-end tests separate from unit tests.
- Locate elements the way users do: `getByRole`, `getByLabel`, `getByText`, and `getByTestId` as a fallback; avoid brittle CSS or XPath selectors tied to structure.
- Use web-first assertions that auto-retry (`await expect(locator).toBeVisible()`, `toHaveText`, `toHaveURL`); do not assert on one-time values like `isVisible()` results.
- Never use fixed waits such as `page.waitForTimeout()`; rely on auto-waiting, assertions, or `waitForResponse`/`waitForURL` for specific events.
- Keep tests isolated and independent: each test gets its own context, creates its own data, and does not depend on test order.
- Reuse login with `storageState` set up in a setup project instead of logging in through the UI in every test.
- Use fixtures and page objects to share setup and repeated flows, and keep them small and focused.
- Mock or stub third-party and unstable network calls with `page.route`, and test against a dedicated test environment, never production.
- Configure `baseURL`, retries on CI, `trace: 'on-first-retry'`, and screenshots or video on failure in `playwright.config`, and use `webServer` to start the app.
- Use `test.step` and descriptive test names for readable reports, and tag tests (`@smoke`) for selective runs.
- Cover accessibility-critical flows and keyboard interaction where relevant, optionally with `@axe-core/playwright`.
- Do not weaken, skip, or delete tests to make a change pass; fix flakiness at the root cause.
- Run the smallest relevant selection first, such as `npx playwright test path/to/file.spec.ts -g "name"`, and debug with `--ui` or `--trace on`.
