---
description: "Use when working in a shared/group repository, coordinating contributors, creating or switching Git branches, preparing pull requests, or resolving merge conflicts."
applyTo: ["**/.github/pull_request_template.md", "**/.github/PULL_REQUEST_TEMPLATE/*.md", "**/CODEOWNERS", "**/.gitlab/merge_request_templates/*.md"]
---

# Shared repository work

- Inspect branch, worktree, staged changes, and relevant diffs before editing. Treat existing changes as another contributor's work unless ownership is clear; do not reset, clean, stash, stage, or commit them for convenience.
- Agree on the task boundary, branch/base, and ownership of overlapping files. Stop for coordination when unexpected edits conflict with the task; preserve unrelated changes without waiting unnecessarily.
- Branch creation, switching, merging, commits, pushes, rebases, resets, and history edits each require the permission specified in agent permissions. Record the exact intended operation and target; approval for one is not permission for the others.
- Follow the team's branch model and protected-branch rules. Use short-lived task branches where the project does; do not impose GitFlow or rename the default branch unasked.
- Before switching branches, identify uncommitted work and explain where it stays. Do not automatically stash or move it; an authorized isolated worktree can keep tasks separate.
- Inspect remote/tracking configuration before comparing branches. Local tracking refs may be stale; fetch from the approved remote when needed, but do not change remotes or fetch arbitrary repositories.
- Do not rebase published/shared history or force-push without explicit coordination and operation approval. `--force-with-lease` reduces one risk but does not authorize rewriting teammates' commits.
- Stage only task-owned paths or reviewed hunks. Review staged and unstaged diffs separately; do not include another contributor's files, generated reports, secrets, or incidental lockfile churn.
- Keep pull requests focused, describe behavior changes and checks, and flag migrations or deployment effects. Respect CODEOWNERS, required review, CI, and branch protection; do not merge your own work or bypass checks without authorization.
- Resolve conflicts by understanding the base and both sides' intent, not choosing `ours`/`theirs` wholesale. Coordinate semantic conflicts, regenerate generated files through their tool, and rerun affected tests/builds.
- Use separate test data, ports, temporary directories, and process IDs on shared machines. Do not stop services by name, delete shared caches, reinstall global tools, or modify shared infrastructure to unblock a local task.
- Leave a concise handoff with changed paths, checks, remaining conflicts, and relevant task references. Update existing project docs when needed; do not create unsolicited contribution guides or status files.
