---
description: "Use when creating or modifying JavaScript files. Covers modern syntax, modules, asynchronous code, errors, and maintainable changes."
applyTo: "**/*.js"
---

# JavaScript Guidelines

- Follow the project's existing JavaScript version, formatting, naming, and module conventions.
- Prefer `const` by default and use `let` only when reassignment is needed. Avoid `var`.
- Use ES modules (`import`/`export`) and relative paths for local imports unless the project already establishes another convention.
- Prefer clear, small functions and straightforward control flow. Avoid unnecessary abstractions, overloading, and dependencies.
- Use async/await for readable asynchronous flows; handle rejected operations and errors explicitly.
- Validate and normalize data at boundaries, especially values from users, files, and network responses.
- Keep changes focused and preserve existing behavior. Reuse project utilities rather than duplicating logic.
- Avoid leaving temporary debugging logs in production code. Add tests for behavior changes when the project has an established test pattern.
