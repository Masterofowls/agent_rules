---
description: "Use when configuring or running Prettier for JavaScript, TypeScript, CSS, HTML, JSON, Markdown, or supported templates."
applyTo: ["**/.prettierrc*", "**/prettier.config.{js,cjs,mjs,ts}", "**/.prettierignore", "**/package.json"]
---

# Prettier

- Inspect the existing formatter and configuration first. Use Prettier only when the project has adopted it; do not add it alongside another formatter for the same files without a clear need.
- Keep formatting options in one shared config and use `.prettierignore` for generated, vendored, and build output.
- Respect `.editorconfig` and the repository's existing conventions; do not impose personal style changes in a feature task.
- Use the project-installed version and package manager. Prefer scripts in `package.json` over downloading or invoking an unpinned global version.
- Provide separate format and non-mutating check scripts (commonly `prettier --write .` and `prettier --check .`) when tooling setup is in scope.
- For routine changes, format only changed files and inspect the resulting diff. Never use a broad formatting run to rewrite unrelated files.
- Do not use Prettier as a linter or assume formatting verifies correctness or types.
- If Prettier conflicts with the existing formatter or syntax support, follow the existing toolchain and report the limitation instead of forcing a conversion.
