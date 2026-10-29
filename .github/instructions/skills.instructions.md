---
description: "Use for every task. Requires checking and using available agent skills before acting, including design, web design, and anti AI-slop skills."
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
