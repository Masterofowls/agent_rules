---
description: "Use when configuring or running linting, Oxlint, JavaScript and TypeScript checks, or repository lint scripts."
applyTo: ["**/.oxlintrc.json", "**/oxlint.config.{js,ts,mjs}", "**/*eslint*", "**/package.json", "**/pyproject.toml"]
---

# Linting

- For every code change, run the project's linter on the changed files or the narrowest relevant scope before finishing. Do not skip linting because the change seems small.
- If no linter or usable lint command exists, report that explicitly; do not claim linting passed or add tooling outside the task's scope without approval.
- Prefer Oxlint over ESLint for new JavaScript and TypeScript setups. Inspect existing scripts, configurations, and supported rules first.
- Do not remove an existing linter, plugin, or dependency as an incidental change. Migrations must preserve necessary coverage and be explicitly requested.
- Keep existing checks that Oxlint does not support until an equivalent is verified. Do not claim linting replaces TypeScript type-checking.
- Follow the installed Oxlint version and documented configuration format; do not guess rule names or copy ESLint options unsupported by Oxlint.
- Enable relevant correctness, React hooks, accessibility, and import rules where supported. Apply framework-specific settings only to matching projects.
- Use the package manager and lockfile already in the repository. Add scripts to the existing manifest rather than a separate toolchain.
- Run the narrowest existing lint command covering the change, then the relevant type-check and tests. Record failures without suppressing them.
- Use autofix only on scoped files and inspect the diff afterward. Do not combine a feature change with repository-wide lint fixes.
- Do not disable a rule globally to hide one error. Use a narrow suppression only when justified, with a short reason.
- Exclude generated output, vendor code, and build artifacts, not source files with unresolved errors.
- For Python, use the existing Ruff or other configured linter; Oxlint does not lint Python.
- See the focused ESLint, Oxlint, Ruff, and Pylint instructions for tool-specific configuration and checks.
- Run the same checks in CI and locally; no skipping hooks or checks without explicit user authorization.
