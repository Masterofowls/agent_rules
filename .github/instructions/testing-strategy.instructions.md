---
description: "Use when planning tests: testing pyramid, Vitest for Vite projects, component and E2E balance, mocking, coverage, and visual regression."
applyTo: ["**/*.{test,spec}.{js,jsx,ts,tsx}", "**/vitest.config.{js,ts,mjs}", "**/__tests__/**/*.{js,jsx,ts,tsx}"]
---

# Testing strategy

## Pyramid
- Many fast unit tests, a moderate number of integration/component tests, few end-to-end tests for critical flows (sign in, checkout, core feature).
- Test behavior users see, not implementation details; prefer accessible queries (`getByRole`, `getByLabelText`).
- Every bug fix gets a regression test.

## Vitest
- In Vite projects use Vitest instead of Jest: shares `vite.config`, native ESM and TypeScript, faster watch mode.
- Use `jsdom` or `happy-dom` environment, `@testing-library/react`, and `@testing-library/user-event`; setup file for `jest-dom` matchers.
- Same API as Jest (`describe`, `it`, `expect`, `vi.fn`, `vi.mock`); keep tests next to the code (`Component.test.jsx`).
- Use `vi.useFakeTimers()` for timers and reset mocks between tests (`restoreMocks: true`).
- Keep Jest only in projects that already use it (see the Jest instructions).

## Integration and API
- Mock the network with MSW, not by stubbing `fetch` in each test; test RTK Query and API layers against it.
- Test server routes with Supertest or the framework test client against a test database; reset state between tests.

## E2E and visual regression
- Use Playwright for E2E (see the Playwright instructions); run on Chromium, Firefox, and WebKit in CI.
- Use Playwright screenshots (`toHaveScreenshot`) or Chromatic/Storybook for visual regression; test key pages at mobile and desktop widths in light and dark themes; keep baselines in the repo and review diffs.
- Disable animations and mask dynamic content for stable screenshots.

## Quality
- Tests are deterministic and independent; no sleeps, no shared state, no real network or time.
- Cover critical logic first; track coverage but do not chase 100%.
- Run tests in CI on every pull request; keep the suite fast.
