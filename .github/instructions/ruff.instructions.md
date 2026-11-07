---
description: "Use when configuring or running Ruff for Python linting, formatting, import sorting, rule selection, or pyproject.toml."
applyTo: ["**/*.py", "**/pyproject.toml", "**/ruff.toml", "**/.ruff.toml"]
---

# Ruff

- Inspect the existing Python toolchain and Ruff version first. Reuse its configuration in `pyproject.toml` or the project's existing Ruff config.
- Prefer Ruff for new Python linting and formatting setups when it covers the project's needs. Do not add it beside an existing linter/formatter without a reason.
- Configure targeted rule families for correctness, imports, and the project's style; avoid enabling every rule family without reviewing new findings.
- Keep the selected Python version and source roots accurate; scope per-file ignores narrowly and explain non-obvious exceptions.
- Use Ruff's formatter consistently when selected; do not run Black and Ruff formatting over the same files as competing formatters.
- Provide separate, repeatable lint, format, and non-mutating format-check commands using the project runner.
- Run the linter and formatter on changed Python files. Use `ruff check` and `ruff format --check` for verification where supported; format only scoped files when edits are needed.
- Review autofix and format diffs. Do not apply fixes repository-wide in a narrow task.
- Do not suppress a rule globally to make CI pass; use a narrow per-file or line suppression only with justification.
- Keep type checking separate (for example, mypy or pyright when configured); Ruff alone does not verify all types.
