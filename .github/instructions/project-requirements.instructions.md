---
description: "Use for every project task: require linting, formatting, meaningful test coverage, code quality checks, safe debugging, a proper .gitignore, and a clear file structure."
applyTo: "**"
---

# Project requirements

## Baseline
- Every code project must have reproducible linting, formatting, tests with coverage reporting, code quality checks, debugging support, a project-specific `.gitignore`, and a clear file structure.
- Inspect the existing toolchain first. Reuse working tools and conventions; add missing baseline setup when creating a project or when project setup is in scope.
- During a narrow feature or bug fix, do not silently expand the task into a toolchain migration or repository-wide reorganization. Report missing baseline requirements and obtain approval for unrelated setup.
- For documentation-only or configuration-only projects, use applicable validation and document why runtime tests or coverage do not apply. Do not invent meaningless tests or dependencies.

## Linting and formatting
- For every code change, run both the project's linter and formatter on the changed files or the narrowest relevant scope before finishing. Do not skip either because a change seems small.
- If either tool or command is unavailable, state that it was not run and why; never claim it passed. Do not expand a narrow task into adding or migrating tooling without approval.
- Provide documented, repeatable lint, format, and non-mutating format-check commands using the existing package manager or task runner.
- Prefer Oxlint for new JavaScript and TypeScript projects; keep required checks it does not support. Use the existing language-appropriate linter for other stacks.
- Use one compatible formatter per language and shared configuration. Follow the linting and formatting instructions; do not reformat unrelated files.
- TypeScript projects need a separate type-check command; linting alone does not verify types.

## Tests and coverage
- Provide a non-interactive test command and a coverage command. Prefer Vitest in new Vite projects and retain established runners elsewhere.
- Cover critical behavior, failure paths, permissions, validation, and regressions. Balance unit, integration, and critical end-to-end tests using the testing strategy.
- Measure applicable lines, branches, functions, and statements. Include untested source files in coverage collection; exclude only justified generated or third-party code.
- Preserve existing coverage thresholds. For new setups, establish and document measurable thresholds appropriate to project risk; do not impose an arbitrary percentage on every project.
- Enforce agreed thresholds in CI. Never lower them, remove tests, or exclude difficult source files just to make checks pass.
- Keep coverage reports and temporary test artifacts out of source control unless the project explicitly tracks them.

## Code quality and debugging
- Validate input at boundaries, handle errors explicitly, preserve type safety, and avoid duplicated logic or unnecessary dependencies.
- Provide safe diagnostic logging or debugger instructions appropriate to the stack. Gate verbose logs, redact secrets and personal data, and remove temporary instrumentation.
- New behavior needs tests; fixes need regression coverage where applicable. Run focused checks first and report exactly what passed or failed.
- Use the same lint, format-check, type-check, test/coverage, and build commands locally and in CI where applicable. Do not suppress failures or claim unrun checks passed.

## Git hygiene
- Maintain a project-specific `.gitignore` for dependencies, build output, caches, virtual environments, coverage, local logs, and private environment files.
- Include `.env`, `.env.local`, private `.env.*` variants, `node_modules/`, `.copilot/`, `.cursor/`, `.claude/`, `.cache/`, and `.mcp-server/`; follow the Git instructions for safe template exceptions and other stack-specific entries.
- Keep safe templates such as `.env.example`, source files, migrations, and the chosen package manager's lockfile trackable. Do not ignore broad source paths to conceal errors.
- Verify important ignore patterns with `git check-ignore`. Adding a pattern does not remove an already-tracked secret; report exposure and follow an authorized remediation process.
- Do not remove tracked files, rewrite history, commit, push, or change branches without the authorization required by the agent permissions.

## Structure and documentation
- Follow the project structure instructions and existing framework conventions. Group related feature code, keep component styles local, and maintain clear import boundaries.
- Separate source, tests, assets, configuration, and generated output where appropriate. Avoid catch-all files, duplicate implementations, and unnecessary architectural layers.
- Document installation, development, linting, formatting, tests, coverage, type-checking, builds, and safe debugging in the existing README or contributor documentation.
- Keep documentation brief and update existing files. Do not generate extra guides, plans, reports, or instruction files unless requested or necessary.
- Keep changes focused; never rewrite whole files, delete projects, or reorganize existing folders to satisfy this checklist without the required necessity and approval.
