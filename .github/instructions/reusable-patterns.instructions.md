---
description: "Use when creating or extracting reusable code, utilities, validation, URL availability checks, or maintenance scripts within a project or across projects."
applyTo: ["**/{src,app,shared,lib,scripts,tools}/**/*.{js,jsx,ts,tsx,py,ps1,sh}", "**/package.json"]
---

# Reusable code and scripts

- Search for existing implementations before adding logic. Reuse compatible helpers, schemas, and scripts instead of copying near-identical code.
- For URL, PostgreSQL/Supabase, SSH, FTPS, Git-leak, runtime, Docker, OS, and Ubuntu setup checks, load the installed `ops-checks` skill and reuse its bundled scripts when suitable. Do not recreate them from memory; inspect their options, permissions, and limitations first.
- Extract shared behavior when there is a real repeated use or an explicit reuse requirement. Do not turn one small task into a generic framework.
- Keep domain-specific logic in its feature; share only code whose meaning and contract are genuinely common. Do not couple unrelated features through a catch-all utility file.
- Separate reusable logic from CLI, UI, network, and filesystem adapters where useful. Importing a module must not run a script, connect remotely, or mutate data.
- Accept explicit inputs instead of hard-coded domains, credentials, paths, or project-specific globals. Use only configuration required by actual callers.
- Define types or schemas, meaningful return values, and explicit failure behavior. CLI failures need nonzero exit codes and actionable, redacted diagnostics.
- URL checks need bounded timeouts, redirect limits, and deliberate status criteria. Distinguish DNS, TLS, timeout, and HTTP failures; define whether a HEAD failure permits a bounded GET fallback. Do not treat any response as proof that a feature works.
- Server-side URL checkers must prevent SSRF; allow authorized destinations and reject unintended private-network access. Do not scan arbitrary hosts.
- Reuse form schemas and pure validation logic across compatible callers, while retaining server validation and authorization. Avoid importing DOM or server-only dependencies into shared contracts.
- Make reusable scripts safe to rerun. Mutating scripts should support inspection or dry-run where practical and must not perform deletion or deployment on import or by default.
- For cross-project reuse, keep dependencies minimal and pass project-specific behavior explicitly. Create a shared package only when requested or justified by real consumers.
- Test representative callers, invalid inputs, failures, and regressions. Run the existing linter and formatter on code changes; document brief usage in existing docs, not extra guides.

## Cross-platform script pairs
- Every reusable project shell task must have both a `.ps1` and a `.sh` entry point with the same base name, such as `check-url.ps1` and `check-url.sh`, in the same scripts directory.
- When adding or modifying a reusable script, create or update its counterpart in the same change. Do not silently migrate every unrelated legacy script; report missing pairs outside the task scope.
- Keep both entry points equivalent in options, defaults, validation, outputs, exit codes, timeouts, and side effects. Never leave a placeholder counterpart or a wrapper that requires the other platform's shell.
- Prefer thin platform wrappers around shared logic in a runtime the project already requires, when suitable. Do not duplicate complex business logic or add a runtime solely for dispatch.
- When a project has several reusable script pairs, provide one shared OS-aware launcher before adding more per-task OS detection. Reuse an existing task runner or a launcher in the project's existing cross-platform runtime.
- The launcher must detect the execution OS first, select PowerShell and the `.ps1` entry point on Windows or the supported shell and `.sh` entry point on Unix, forward arguments without string interpolation, and preserve the child exit status.
- A `.ps1` or `.sh` file is not inherently universal. If no cross-platform runtime exists, provide paired launcher entry points with a shared command contract rather than promising one file can run natively everywhere.
- Handle WSL and Git Bash explicitly, allow only known task names, and fail clearly on unsupported systems or missing interpreters. Do not install interpreters or elevate automatically.
- Test both implementations with the same success and failure cases, including quoted paths and invalid input. State any platform not executed; syntax checks alone do not establish behavioral parity.
