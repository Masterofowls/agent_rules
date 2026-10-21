---
description: "Use when creating or modifying pytest tests, fixtures, conftest files, or Python test configuration. Covers test structure, fixtures, parametrization, mocking, and async tests."
applyTo: ["**/test_*.py", "**/*_test.py", "**/conftest.py", "**/tests/**/*.py"]
---

# Pytest Guidelines

- Follow the project's existing test layout; place tests in `tests/` and name files `test_*.py` and functions `test_<behavior>`.
- Use plain `assert` statements and `pytest.raises` for expected exceptions; do not use `unittest` assertions in pytest-style tests.
- Test one behavior per test with a descriptive name, and follow arrange-act-assert.
- Share setup through fixtures, put shared fixtures in `conftest.py`, and choose the narrowest scope that works. Use `yield` fixtures for teardown.
- Use `@pytest.mark.parametrize` for multiple inputs instead of loops, and give cases readable `ids`.
- Use built-in fixtures (`tmp_path`, `monkeypatch`, `capsys`, `caplog`) before adding helpers or packages.
- Mock only external boundaries (network, time, filesystem, third-party services) with `monkeypatch` or `unittest.mock`; do not mock the code under test.
- Keep tests independent and deterministic: no shared mutable state, no reliance on test order, and no real network or production data.
- For async code, use the project's existing async plugin (`pytest-asyncio` or `anyio`) and mark tests consistently.
- Use markers (`slow`, `integration`) registered in configuration, and `skip`/`xfail` only with a clear reason.
- Use the framework's test tools for web code (Django's test client or `pytest-django`, FastAPI's `TestClient`, Flask's test client) and isolate the database per test.
- Add a regression test for every bug fix, and do not weaken or delete existing tests to make them pass.
- Run the smallest relevant selection first, such as `pytest path::test_name -x`.
