---
description: "Use when preparing or reviewing pull requests, writing commit messages, or doing code review: small PRs, checklists, and conventional commits."
applyTo: ["**/.github/pull_request_template.md", "**/.github/PULL_REQUEST_TEMPLATE/*.md", "**/CONTRIBUTING.md", "**/commitlint.config.{js,cjs,mjs,ts}"]
---

# Code review and pull requests

## Pull requests
- Keep PRs small and focused on one change (ideally under 400 changed lines); split refactors from features.
- Title in conventional-commit style; description says what changed, why, how to test, and links the issue; add screenshots for UI changes.
- Open a draft PR early; rebase or merge main before review; CI must pass before merge.
- Do not mix formatting-only changes with logic changes.

## Conventional commits
- Format: `type(scope): short imperative subject`; types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`.
- Subject under 72 characters, no trailing period; body explains why when it is not obvious.
- Mark breaking changes with `!` or a `BREAKING CHANGE:` footer.
- One logical change per commit; never commit secrets, build output, or debug code.

## Author checklist
- Code builds, Oxlint and typecheck pass, tests added or updated and passing.
- No `console.log` debugging, commented-out code, or unrelated edits left.
- Accessibility, responsive layout, and security were considered for UI and API changes.
- Docs and `.env.example` updated when behavior or config changed.

## Reviewer checklist
- Correctness and edge cases first; then security, performance, readability, and tests.
- Check that existing code was edited, not rewritten, and that no unneeded dependencies were added.
- Give specific, kind, actionable comments; separate blockers from nits; explain why.
- Approve when the change is good enough and safe, not perfect; verify by running it for risky changes.
