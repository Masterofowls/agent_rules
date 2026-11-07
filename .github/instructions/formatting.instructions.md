---
description: "Use when formatting code, configuring Prettier, Oxfmt, Ruff, Black, EditorConfig, or format scripts."
applyTo: ["**/.editorconfig", "**/*prettier*", "**/*oxfmt*", "**/package.json", "**/pyproject.toml"]
---

# Formatting

- For every code change, run the project's formatter on the changed files before finishing, then inspect the diff for unrelated churn. Do not skip formatting because the change seems small.
- If no formatter or usable format command exists, report that explicitly; do not claim formatting passed or add tooling outside the task's scope without approval.
- Follow the project's formatter, EditorConfig, indentation, quotes, line endings, and trailing-comma conventions.
- Use the existing formatter: Prettier or Oxfmt for supported JavaScript and TypeScript projects, Ruff format or Black for Python. Do not add competing formatters.
- Check the installed formatter's language support before using it on CSS, HTML, SQL, or templates.
- Configure shared rules once. Keep generated, vendored, and build files out of formatting runs.
- Format only changed files or ranges where supported; never rewrite the whole repository as a side effect of a feature.
- Inspect the formatted diff for behavior changes and unrelated churn. Respect existing worktree changes.
- Keep formatter checks separate from linting and type-checking; run the repository's existing format-check command.
- Do not change line endings or normalize every file without a specific request.
- Add or change formatting configuration only when required; preserve established team conventions.
- If formatting changes are the task, keep them separate from logic changes. Commit or push only with explicit user authorization.
- See the Prettier and Ruff instructions for tool-specific configuration and verification.
