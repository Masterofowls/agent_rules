---
description: "Use for every task. Maps requests such as check site performance, audit accessibility, test the app, review design, SEO, ORM work, and deployment to matching skills and instructions before acting."
applyTo: "**"
---

# Skills

- Before starting any task, check the available skills and load every skill that matches the task.
- Invoke a matching skill first, before writing code or replying. Never just mention it.
- If several skills apply, use all of them and follow their instructions together.
- For any UI, frontend, layout, styling, or visual work, always use the design skills: `frontend-design`, `web-design-guidelines`, `design-taste-frontend`, `impeccable`, `ui-ux-pro-max`.
- For UI work, also apply `no-ai-design-slop` while building and `audit-ai-design-slop` before finishing: avoid generic gradients, default fonts, template layouts, and filler copy.
- If no installed skill matches, search with `npx skills find <query>` and suggest a good candidate before proceeding without one.
- Skills add to the instruction files, not replace them; on conflict, follow the more specific rule.
- Do not load skills that are clearly unrelated to the task.

## Quick task associations

Match intent, not just exact words; Russian requests and synonyms use the same associations. Load listed skills only when available and applicable to the actual task.

| Request or intent | Skills to invoke | Related instructions |
| --- | --- | --- |
| Check site performance, slow page, Lighthouse, Core Web Vitals | `web-perf`, `web-quality-audit`; `vercel-react-best-practices` for React bottlenecks | performance, optimization, images-media |
| Accessibility audit, a11y, keyboard, screen reader, WCAG | `accessibility`; `agent-browser` for browser checks | accessibility, qa-testing |
| QA, test the website, reproduce a browser bug, smoke test | `agent-browser`; `playwright-best-practices` when writing or debugging Playwright tests | qa-testing, testing-strategy, playwright, debugging |
| SEO audit, metadata, indexing, search visibility | `seo-audit` | seo |
| Design, redesign, layout, responsive or mobile UI | `frontend-design`, `web-design-guidelines`, `design-taste-frontend`, `impeccable`, `ui-ux-pro-max`, `no-ai-design-slop`; `audit-ai-design-slop` before finishing | design, design-system, frontend, css, accessibility |
| Looks AI-made, generic UI, anti-slop audit | `audit-ai-design-slop`, `no-ai-design-slop`; use the design skills if changing UI | design, design-system |
| React rendering, hooks, component composition | `vercel-react-best-practices`; `vercel-composition-patterns` for composition changes | react, performance, project-structure |
| Drizzle schema, query, relation, migration | `drizzle-orm-patterns` | drizzle, orm, validation |
| PostgreSQL query or schema optimization | `supabase-postgres-best-practices` when applicable to the database task | psql, sql, orm, optimization |
| shadcn components in an existing compatible project | `shadcn` and applicable design skills | frontend, design-system; do not introduce Tailwind without permission |
| Configure deployment, Docker, release readiness | `deployment-patterns`; `deploy-to-vercel` only for an actual Vercel deployment request | deployment, docker-cicd, agent-permissions |
| Russian UI, translation, grammar, authorship credits | `russian-language` | russian, anti-ai-writing |
| Edit agent rules, instructions, prompts, or skills | `agent-customization` | agent-permissions, anti-ai-writing |
| Unexpected agent behavior or ignored instructions | `troubleshoot` | skills, debugging |
| Find or install a skill | `find-skills` | agent-permissions |
| Teach me, explain a topic or selected code, beginner to advanced, научи меня | `teach-topic`; load a domain skill only when its workflow is relevant | anti-ai-writing, agent-permissions |
| Quiz me, exercises, review my solution, practice, проверь мои знания | `practice-topic`; `teach-topic` for concept explanations | anti-ai-writing, agent-permissions |
| General web code best practices or security hardening | `best-practices` when its description matches | security, auth, validation |

## Routing safeguards

- Check the current skill catalog and each description before invocation. Never invent a skill name or assume installation on another machine.
- For explicit vulnerability reviews, use the available security-review workflow first; it is an agent workflow, not a skill named `security-review`. Follow its caller requirements and authorization limits.
- If a task has no listed association, select from the catalog by description. Prisma, NestJS, linting, and formatting still use their relevant instruction files even when no dedicated skill exists.
- Related instruction names refer to `*.instructions.md` files alongside this file. File globs alone may miss URL-only audits or command requests; read the relevant files explicitly when they are not already loaded.
- Invoke through the host's skill loader. If unavailable, read the matching installed `SKILL.md` and its required references; report unavailable capabilities rather than pretending invocation succeeded.
- Add applicable skills when the task changes scope; do not reinvoke already-loaded skills or load every table row for a broad request.
- Skills do not grant permission to deploy, commit, push, change branches, delete files, or scan unapproved targets.
- These associations guide selection; they are not executable aliases or enforced hooks. Verify the requested outcome with actual measurements or tests.
