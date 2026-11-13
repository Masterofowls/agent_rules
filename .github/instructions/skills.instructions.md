---
description: "Use for every task. Maps requests such as check site performance, audit accessibility, test the app, review design, SEO, ORM work, and deployment to matching skills and instructions before acting."
applyTo: "**"
---

# Skills

- Before acting, check skill names and descriptions already in context. Load the smallest set needed for the current step, usually one primary workflow; do not load every keyword match.
- Invoke a required matching skill before its workflow, rather than merely mentioning it. Respect explicit host requirements and user requests for particular skills.
- Treat overlapping skills as alternatives unless they supply distinct required capabilities. Add another skill only when the current step needs it.
- For UI work, select one suitable primary design skill from `frontend-design`, `web-design-guidelines`, `design-taste-frontend`, `impeccable`, or `ui-ux-pro-max`; do not load the entire design catalog by default.
- For visual anti-slop work, load `no-ai-design-slop` when building or revising visuals and `audit-ai-design-slop` at the final visual review, not both at task startup.
- If no installed skill fits, proceed with applicable instructions for ordinary tasks. Use `find-skills` and a targeted search when discovery or installation is requested or a missing capability blocks the task; do not search for a skill on every small request.
- Skills add to the instruction files, not replace them; on conflict, follow the more specific rule.
- Do not load skills that are clearly unrelated to the task.

## Quick task associations

Match intent, not just exact words; Russian requests and synonyms use the same associations. Entries are candidates, not lists to load in full. Select by the current step and add complementary capabilities only when needed.

| Request or intent | Skills to invoke | Related instructions |
| --- | --- | --- |
| Check site performance, slow page, Lighthouse, Core Web Vitals | `web-perf` for focused performance checks or `web-quality-audit` for a broad audit; add `vercel-react-best-practices` for a measured React bottleneck | performance, optimization, images-media |
| Accessibility audit, a11y, keyboard, screen reader, WCAG | `accessibility`; `agent-browser` for browser checks | accessibility, qa-testing |
| QA, test the website, reproduce a browser bug, smoke test | `agent-browser`; `playwright-best-practices` when writing or debugging Playwright tests | qa-testing, testing-strategy, playwright, debugging |
| SEO audit, metadata, indexing, search visibility | `seo-audit` | seo |
| Design, redesign, layout, responsive or mobile UI | Choose one primary design skill; `no-ai-design-slop` during visual implementation and `audit-ai-design-slop` at final visual review | design, design-system, frontend, css, accessibility |
| Looks AI-made, generic UI, anti-slop audit | `audit-ai-design-slop`, `no-ai-design-slop`; use the design skills if changing UI | design, design-system |
| React rendering, hooks, component composition | `vercel-react-best-practices`; `vercel-composition-patterns` for composition changes | react, performance, project-structure |
| Drizzle schema, query, relation, migration | `drizzle-orm-patterns` | drizzle, orm, validation |
| PostgreSQL query or schema optimization | `supabase-postgres-best-practices` when applicable to the database task | psql, sql, orm, optimization |
| shadcn components in an existing compatible project | `shadcn` and applicable design skills | frontend, design-system; do not introduce Tailwind without permission |
| Configure deployment, Docker, release readiness | `deployment-patterns`; `deploy-to-vercel` only for an actual Vercel deployment request | deployment, docker-cicd, agent-permissions |
| FTP, FTPS, SFTP uploads or remote hosting files | Use a matching installed skill only if available; no assumed FTP skill | ftp, deployment, agent-permissions |
| SSH connection, remote VPS commands or services | `deployment-patterns` when deploying or managing deployment; otherwise match the current catalog | ssh, deployment, agent-permissions |
| Reusable helpers, scripts, shared validation or repository layout | Match the current catalog only when relevant; no assumed reuse skill | reusable-patterns, project-structure, validation |
| PowerShell, CMD, Bash, cross-platform script pairs or OS dispatch | Match a relevant installed skill if available; no assumed shell skill | powershell-cmd, shell-bash, reusable-patterns, agent-permissions |
| Check remote URL, PostgreSQL/Supabase, SSH, FTPS, Git leaks, tools, Docker, OS, or preview Ubuntu setup | `ops-checks`; reuse its bundled scripts, obtain target authorization before remote probes or setup | reusable-patterns, ssh, ftp, security, agent-permissions |
| Russian UI, translation, grammar, authorship credits | `russian-language` | russian, anti-ai-writing |
| Edit agent rules, instructions, prompts, or skills | `agent-customization` | agent-permissions, anti-ai-writing |
| Unexpected agent behavior or ignored instructions | `troubleshoot` | skills, debugging |
| Find or install a skill | `find-skills` | agent-permissions |
| Teach me, explain a topic or selected code, beginner to advanced, научи меня | `teach-topic`; load a domain skill only when its workflow is relevant | anti-ai-writing, agent-permissions |
| Quiz me, exercises, review my solution, practice, проверь мои знания | `practice-topic`; `teach-topic` for concept explanations | anti-ai-writing, agent-permissions |
| General web code best practices or security hardening | `best-practices` when its description matches | security, auth, validation |
| OpenAPI/Swagger contracts or SDK compatibility | Use the current framework's tooling; no assumed dedicated skill | openapi, api-design, validation |
| Shared repository, branch coordination, PRs or merge conflicts | Match installed skills only where relevant | shared-repository, git, code-review, agent-permissions |
| IaC plans, release operations, monitoring or recovery | `deployment-patterns` when its workflow applies | devops, deployment, docker-cicd, agent-permissions |
| DNS, TLS expiry, disk capacity or local Git worktree state | `ops-checks`; authorize exact remote hosts before DNS/TLS probes | reusable-patterns, devops, shared-repository |

## Routing safeguards

- Check the current skill catalog and each description before invocation. Never invent a skill name or assume installation on another machine.
- For explicit vulnerability reviews, use the available security-review workflow first; it is an agent workflow, not a skill named `security-review`. Follow its caller requirements and authorization limits.
- If a task has no listed association, select from the catalog by description. Prisma, NestJS, linting, and formatting still use their relevant instruction files even when no dedicated skill exists.
- Related instruction names refer to `*.instructions.md` files alongside this file. File globs alone may miss URL-only audits or command requests; read the relevant files explicitly when they are not already loaded.
- Before applying framework or library rules, confirm that the project uses the tool through its dependencies, imports, or configuration. For linting and formatting, load only the selected tool's instructions; a generic folder or package manifest is not proof of framework use.
- Invoke through the host's skill loader. If unavailable, read the matching installed `SKILL.md` and its required references; report unavailable capabilities rather than pretending invocation succeeded.
- If a named skill is not installed, continue with applicable instructions instead of repeatedly trying to load it or installing it without a request.
- Add applicable skills when the task changes scope; do not reinvoke already-loaded skills or load every table row for a broad request.
- Skills do not grant permission to deploy, commit, push, change branches, delete files, or scan unapproved targets.
- These associations guide selection; they are not executable aliases or enforced hooks. Verify the requested outcome with actual measurements or tests.

## Context and tool selection

- Read only instructions applicable to the active task, files, and phase. Do not open the entire instructions directory or reload content already supplied by the host.
- Load referenced skill documents, scripts, and examples only when needed. A routing-table entry does not require reading every related file before starting.
- Prefer an exact file or symbol lookup over a broad repository scan. Use available code intelligence for symbol relationships, glob for known filename patterns, and scoped text search for specific content.
- Discover deferred tools with one focused capability search; reuse returned tool definitions rather than searching again. Choose the simplest tool that directly answers the current question.
- Bound tool output with file filters, result limits, and line ranges. Inspect large saved results with targeted searches and narrow reads rather than dumping whole files or logs.
- Batch independent reads and checks; keep dependent steps sequential. Reuse verified results unless files or assumptions changed.
- Run focused tests and checks first, escalating when required by risk or results. Never omit required linting, formatting, security, or correctness checks solely to save context.
- Handle small tasks directly. Delegate only a substantial independent objective, request a concise evidence-backed result, and avoid re-reading the same delegated scope.
- For long tasks, retain a short summary of decisions, changed paths, and verification results instead of repeating raw logs. Keep replies concise without hiding failures or uncertainty.
- Narrow instruction `applyTo` patterns when authoring rules; reserve always-on files for genuinely universal policy. Hosts may inject matching instructions automatically, so do not claim selective reading can unload already-injected context.

## Token budget
- Optimize repeated input/output, not correctness: do not omit required evidence, permissions, tests, or error details just to shorten a request.
- Start with the exact task and a bounded evidence set. Read only the imports, callers, implementation, and tests needed for the current decision; expand when results reveal a dependency.
- Request structured summaries, selected columns, scoped diffs, and bounded log windows. After an oversized result, inspect the saved output with a targeted search instead of rerunning or dumping it.
- Reuse known file paths, tool schemas, verified results, and active skill context. Do not reload unchanged instructions or probe the same capability repeatedly.
- Keep one compact record of decisions, changed paths, failed checks, and unresolved work using the host's session state. Do not create extra repository notes or store temporary progress in durable memory.
- Use a separate agent only for a substantial independent objective; pass its task boundary and expected result, not the full conversation. Do not duplicate its investigation or fan out trivial lookups.
- Before context compaction, retain exact commands/outcomes and the next required action. Afterward, verify that the summaries still match current files before edits.
