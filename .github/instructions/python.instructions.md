---
description: "Use when creating or modifying Python files. Covers style, typing, error handling, async code, dependencies, and safe changes."
applyTo: "**/*.py"
---

# Python Guidelines

- Follow the project's existing Python version, formatting, naming, and structure. Default to PEP 8 and modern Python 3 syntax.
- Add type hints to function signatures and public interfaces; use built-in generics and `X | None` when the project's Python version supports them.
- Use `pathlib`, f-strings, comprehensions, dataclasses, and context managers where they keep code clearer.
- Catch specific exceptions, never use bare `except:`, and do not silence errors without handling or logging them.
- Use `async`/`await` consistently in async code and never call blocking functions inside async functions.
- Use the `logging` module instead of `print` for debugging, and never log secrets or personal data.
- Use absolute imports within packages unless the project already uses relative imports; avoid wildcard imports.
- Keep functions small and focused. Avoid mutable default arguments and unnecessary class hierarchies or overloading.
- Prefer the standard library before adding packages. Use the project's existing virtual environment and dependency manager (`uv`, `poetry`, or `pip`) and do not upgrade dependencies unrelated to the task.
- Read configuration and secrets from environment variables, never hard-code them.
- Make focused changes that preserve existing behavior; add tests following the project's existing test framework when behavior changes.
- Keep comments and docstrings brief and only where they clarify non-obvious behavior.
