---
description: "Use when configuring or running Oxlint, its JavaScript and TypeScript rules, plugins, overrides, and repository lint scripts."
applyTo: ["**/.oxlintrc.json", "**/oxlint.config.{js,ts,mjs}"]
---

# Oxlint

- Prefer Oxlint for new JavaScript and TypeScript projects. Inspect the installed version and supported rules/plugins before configuring it.
- Preserve the project's established linter and plugin coverage; do not remove ESLint or introduce Oxlint-only behavior during an unrelated feature change.
- Configure rules in the format supported by the installed version. Do not copy ESLint configuration keys or assume every ESLint plugin/rule has an Oxlint equivalent.
- Enable correctness rules and applicable TypeScript, React Hooks, accessibility, and import checks only when supported and relevant to the codebase.
- Keep formatter responsibilities separate. Oxlint does not replace Prettier/Oxfmt or TypeScript type checking.
- Add or update a repeatable package script and CI check when lint-tool setup is in scope; use the repository's package manager and lockfile.
- Run lint on changed files or the narrowest relevant scope. Apply autofixes only to scoped files and inspect the diff.
- Do not turn off rules globally to suppress findings. Prefer a local, justified suppression with an explanation.
- Ignore generated, vendored, and build output, not problematic source files.
- If Oxlint does not cover a required check, retain or add the smallest compatible complementary check; document the distinct responsibility.
