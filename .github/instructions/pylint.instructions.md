---
description: "Use when configuring or running Pylint in an existing Python project, including pyproject.toml, pylint config, plugins, and diagnostics."
applyTo: ["**/.pylintrc", "**/pylintrc", "**/pylint.toml"]
---

# Pylint

- Use Pylint when the project already relies on it or requires checks not covered by its configured Ruff setup. For new Python projects, consider Ruff first to keep tooling lean.
- Do not add Pylint alongside Ruff for overlapping checks unless the project has a documented need and distinct responsibilities.
- Follow the installed Pylint version and keep configuration in the existing `pyproject.toml` or project config file.
- Configure the actual Python version, package roots, generated code, and plugin requirements correctly. Keep ignores and disables narrow.
- Run Pylint on changed modules or the narrowest relevant package, using the repository's pinned environment and command.
- Fix meaningful correctness findings; do not blanket-disable message categories or lower the CI threshold to silence existing issues.
- Keep formatting in the selected formatter (usually Ruff format or Black); Pylint is not a formatter.
- Keep type-checking separate and use the project's configured type checker where applicable.
- Review output after any automated fixes; do not rewrite or reformat unrelated modules.
