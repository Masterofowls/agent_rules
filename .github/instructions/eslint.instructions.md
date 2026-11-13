---
description: "Use when configuring or maintaining ESLint in an existing JavaScript or TypeScript project, including plugins, flat config, and lint scripts."
applyTo: ["**/*eslint*", "**/eslint.config.{js,mjs,cjs,ts}"]
---

# ESLint

- Prefer Oxlint for new JavaScript and TypeScript projects. Use ESLint when the project already relies on it or needs rules/plugins not adequately covered by the configured Oxlint version.
- Do not migrate, remove, or add a second linter as an incidental change. Keep existing custom rules and plugin coverage until replacements are verified.
- Follow the installed ESLint version and configuration style; for new ESLint 9+ configuration use flat config unless project tooling requires otherwise.
- Scope language and framework plugins to relevant file patterns. Avoid enabling browser globals, Node globals, or TypeScript parser settings indiscriminately.
- Keep formatting in the project's formatter; avoid overlapping stylistic rules when Prettier or Oxfmt is used.
- Keep type-aware lint rules distinct from a TypeScript compiler/type-check command. Do not claim ESLint proves type safety.
- Run the existing lint script on changed files or the narrowest supported scope. Inspect autofix changes and avoid `--fix` across unrelated files.
- Do not disable rules globally to clear an error. Use a narrow, justified suppression and retain the rule for the rest of the project.
- Exclude only generated, vendored, and build output. Never hide source errors by broadening ignores.
- If both ESLint and Oxlint are intentionally used, document their non-overlapping responsibilities and run both relevant checks.
