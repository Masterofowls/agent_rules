---
description: "Use when creating or modifying TypeScript files. Covers typing, modules, error handling, and safe changes."
applyTo: "**/*.ts"
---

# TypeScript Guidelines

- Follow the project's existing TypeScript version, configuration, formatting, and naming conventions.
- Prefer precise types and inferred types where clear. Avoid `any`; use `unknown` with appropriate narrowing when the value is not known.
- Use `type` and `interface` consistently with nearby code. Model data and function contracts explicitly when it improves safety and clarity.
- Prefer ES module imports and exports. Use relative paths for local modules unless the project already establishes another convention.
- Handle nullable values and external input explicitly; do not hide type errors with non-null assertions or broad casts.
- Use async/await for asynchronous flows when it improves readability, and handle errors according to existing project conventions.
- Keep functions focused and changes surgical. Reuse existing helpers and avoid unnecessary abstractions or dependencies.
- Preserve the project's compiler and lint settings. Do not weaken strictness or suppress diagnostics to make a change pass.
- Add tests for behavior changes when the project has an established test pattern.
