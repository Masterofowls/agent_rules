---
description: "Use when committing, branching, merging, rebasing, writing commit messages, or editing .gitignore and .gitattributes. Covers commit hygiene, branches, history safety, and ignored files."
applyTo: ["**/.gitignore", "**/.gitattributes"]
---

# Git Guidelines

- Make small, focused commits that each do one logical change, and review the diff before committing.
- Write commit messages with a concise imperative subject line (about 50-72 characters), such as `Add login form validation`, and a body explaining why when needed. Follow Conventional Commits when the project uses them.
- Use short, descriptive branch names such as `feature/login-form` or `fix/null-user`, and keep branches current with the main branch.
- Never commit secrets, `.env` files, credentials, build output, `node_modules`, virtual environments, or large generated files; keep them in `.gitignore`.
- Do not rewrite shared history: avoid force-pushing to shared branches, and use `--force-with-lease` only on your own branches.
- Do not use destructive commands (`reset --hard`, `clean -fd`, `checkout .`) without confirming that no work will be lost.
- Prefer `git status` and `git diff` to check state before staging, and stage specific files instead of `git add .` when unrelated changes exist.
- Resolve merge conflicts carefully by preserving both sides' intent, and run the build and tests afterward.
- Do not change git config, remotes, or hooks without being asked, and never skip hooks with `--no-verify` unless requested.
- Keep `.gitignore` patterns specific and grouped by purpose; use `.gitattributes` for line endings and binary files.
