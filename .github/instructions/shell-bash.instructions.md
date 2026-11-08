---
description: "Use when writing or running shell or Bash commands and .sh scripts; covers safe quoting, portable tooling, exit codes, permissions, and cross-platform scripts."
applyTo: ["**/*.sh", "**/.shellcheckrc", "**/{scripts,tools}/**"]
---

# Shell and Bash

- Declare the intended interpreter with a shebang. Use POSIX syntax for `/bin/sh`; use Bash syntax only when Bash is required and available.
- Check the execution environment, not just the physical host: Linux, macOS, WSL, and Git Bash have different paths and utilities.
- Quote variable expansions and use arrays for Bash argument lists. Never use `eval` or concatenate untrusted values into commands.
- Resolve paths relative to the script where appropriate, not the caller's directory. Handle spaces, Unicode, leading dashes, and symlinks deliberately.
- Use LF line endings and configure executable permissions when the execution method requires them. Do not assume GNU options exist on macOS/BSD tools.
- Choose deliberate failure handling. For Bash, `set -euo pipefail` can help but does not replace explicit status checks; understand exceptions in conditionals, pipelines, and substitutions.
- Preserve exit statuses, write errors to stderr, and keep stdout stable for structured output. Do not hide failures with `|| true` unless the specific failure is expected and explained.
- Use traps to clean up only task-owned temporary resources and handle interruption. Never combine recursive deletion with wildcards or unresolved targets.
- Prefer least privilege; use `sudo` only for an explicitly authorized operation that needs it. Never elevate an entire script unnecessarily or disable security controls.
- Check dependencies and versions before execution; do not download and pipe remote scripts directly into a shell.
- Bound network timeouts, concurrency, and retries. Keep credentials out of URLs, command arguments, traces, and logs.
- Follow the paired `.ps1`/`.sh` contract. Use ShellCheck and shfmt when configured, and test the supported shells and operating systems.
