---
description: "Use for every task, including terminal commands: preserve files, limit documentation and deletions, and require explicit authorization for deployment, commits, pushes, and branch changes."
applyTo: "**"
---

# Agent permissions

## Preserve existing work
- Read existing files before editing. Implement features with targeted patches; never fully rewrite existing files or functions unless a full rewrite is necessary for the requested change.
- If a full rewrite is necessary, explain why and obtain explicit user approval before replacing the file. Preserve unrelated logic, configuration, dependencies, and user changes.
- These rules apply equally to editor tools, terminal commands, scripts, generators, and delegated agents. Never bypass them by using shell redirection, bulk replacement, or deleting and recreating a file.
- Do not revert, overwrite, or clean up another contributor's changes. Check the worktree and diff before and after editing.

## Deletion
- Never delete an entire project, repository, or workspace, including through recursive removal, cleanup commands, or scripts.
- Do not delete existing project files unless removal is necessary for the requested task. Explain the exact paths and reason, and obtain explicit user approval before deleting them.
- Remove only specifically identified temporary files created for the current task; do not sweep unrelated files or directories.
- Never use broad deletion commands, recursive wildcards, or destructive Git cleanup to make implementation easier. Inspect resolved targets first.

## Git authorization
- Never commit or push changes on your own. Each action requires an explicit user request or approval; permission to commit does not imply permission to push.
- Never create, switch, or merge branches on your own. Obtain explicit authorization for the operation and intended branch.
- A request to implement, fix, test, or finish a task is not authorization to commit, push, or change branches.
- Do not amend commits, rebase, reset, force-push, delete branches, or rewrite history without explicit authorization for that operation.
- Read-only Git inspection is allowed. Leave completed changes in the current worktree and report what changed and what was verified.

## Scope
- Never deploy, publish, promote a release, or change live infrastructure without explicit user permission for the target and environment. Writing deployment configuration or finishing a feature does not grant deployment permission.
- Authorization applies only to the specified action and target in the current task; it is not standing permission for later tasks.
- When a tool, script, or package command could perform a restricted operation as a side effect, inspect it first and do not run it without the required authorization.
- These instructions guide agent behavior; they do not replace tool permissions, approval prompts, or enforced hooks.

## Documentation and instructions
- Keep instructions, explanations, and replies concise; include only what the task requires.
- Update existing documentation rather than creating duplicate guides. Do not create unsolicited plans, summaries, reports, or extra Markdown files.
- Create new documentation or instruction files only when requested or necessary for the change and no existing file fits. Avoid boilerplate, repeated rules, and line-by-line commentary.
