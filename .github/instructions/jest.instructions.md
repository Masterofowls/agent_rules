---
description: "Use when creating or modifying Jest unit or component tests, mocks, or Jest configuration. Covers test structure, mocking, async tests, and React Testing Library usage."
applyTo: ["**/*.{test,spec}.{js,jsx,ts,tsx}", "**/__tests__/**/*.{js,jsx,ts,tsx}", "**/jest.config.{js,cjs,mjs,ts}", "**/jest.setup.{js,ts}"]
---

# Jest Guidelines

- Follow the project's existing test location and naming (`*.test.js` next to the source or in `__tests__/`), and use ES module imports.
- Use `describe` for grouping and `it`/`test` with behavior-focused names; follow arrange-act-assert and test one behavior per test.
- Test behavior and public output rather than implementation details or internal state.
- For React, use React Testing Library: query by role, label, or text (`getByRole`, `getByLabelText`), simulate users with `userEvent`, and avoid testing by class names or component internals.
- Use `findBy*` and `waitFor` for async UI, and `async`/`await` in async tests; always await or return promises.
- Use `jest.fn()`, `jest.spyOn()`, and `jest.mock()` only for external boundaries (network, timers, modules with side effects); do not mock the unit under test.
- Reset mocks and timers between tests (`restoreMocks`/`clearMocks` config or `afterEach`), and use fake timers (`jest.useFakeTimers()`) instead of real delays.
- Keep tests independent and deterministic: no shared mutable state, no dependence on order, and no real network calls; mock HTTP with the project's existing tool.
- Prefer explicit assertions (`toEqual`, `toBe`, `toThrow`, `toHaveBeenCalledWith`) over broad snapshots; use snapshots only for small, stable output.
- Use `it.each` for multiple input cases instead of loops.
- Add a regression test for every bug fix, and never weaken, skip, or delete tests to make a change pass.
- Run the smallest relevant selection first, such as `npx jest path/to/file.test.js -t "name"`.
