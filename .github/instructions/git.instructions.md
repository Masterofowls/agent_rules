---
description: "Use when committing, branching, merging, rebasing, writing commit messages, or editing .gitignore and .gitattributes. Covers commit hygiene, branches, history safety, and ignored files."
applyTo: ["**/.gitignore", "**/.gitattributes"]
---

# Git Guidelines

- Follow the always-on agent permissions: commits, pushes, branch creation, switching, and merging each require explicit user authorization. Implementation requests do not grant that permission.
- Make small, focused commits that each do one logical change, and review the diff before committing.
- Write commit messages with a concise imperative subject line (about 50-72 characters), such as `Add login form validation`, and a body explaining why when needed. Follow Conventional Commits when the project uses them.
- Use short, descriptive branch names such as `feature/login-form` or `fix/null-user`, and keep branches current with the main branch.
- Never commit secrets, `.env` files, credentials, build output, `node_modules`, virtual environments, or large generated files; keep them in `.gitignore`.
- Do not rewrite history or force-push without explicit authorization; `--force-with-lease` is not a substitute for approval.
- Do not use destructive commands (`reset --hard`, `clean -fd`, `checkout .`) without explicit authorization for the exact operation and confirmation that no work will be lost. Never delete an entire project.
- Prefer `git status` and `git diff` to check state before staging, and stage specific files instead of `git add .` when unrelated changes exist.
- Resolve merge conflicts carefully by preserving both sides' intent, and run the build and tests afterward.
- Do not change git config, remotes, or hooks without being asked, and never skip hooks with `--no-verify` unless requested.
- Keep `.gitignore` patterns specific and grouped by purpose; use `.gitattributes` for line endings and binary files.

## Required ignore entries
- When setting up or maintaining a project's `.gitignore`, include these baseline entries. Directory patterns also match nested directories.

```gitignore
# Private environment files
.env
.env.local
.env.*
!.env.example
!.env.sample
!.env.template

# Dependencies, local agent state, and caches
node_modules/
.copilot/
.cursor/
.claude/
.cache/
.mcp-server/
```

- Add stack-specific build output, virtual environments, test reports, caches, logs, and local credential files as applicable. Do not ignore source code, migrations, lockfiles, or shared configuration indiscriminately.
- Preserve safe, tracked team customizations with narrow exceptions when deliberately shared; never include credentials in those exceptions. Keep shared `.github/instructions` trackable.
- Check effective patterns with `git check-ignore`; `.gitignore` does not untrack files already committed. Do not remove tracked files or rewrite history without authorization.
