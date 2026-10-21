---
description: "Use when creating or modifying Vite configuration, project setup, environment variables, aliases, or build and dev scripts. Covers config, env handling, and tooling."
applyTo: ["**/vite.config.{js,mjs,ts}", "**/.env*", "**/.oxlintrc.json"]
---

# Vite and Tooling Guidelines

- Use Vite for new frontend projects and keep its configuration minimal; edit `vite.config` in small, targeted changes instead of rewriting it.
- Use the official Vite plugins for the framework in use (for example `@vitejs/plugin-react`) and avoid adding plugins when built-in features suffice.
- Expose client variables only through `VITE_`-prefixed environment variables, access them through `import.meta.env`, and never commit secrets or real `.env` values.
- Use Oxlint for linting new projects. Preserve the existing linter in established projects unless a migration is requested.
- Keep scripts standard (`dev`, `build`, `preview`, `lint`) and do not change them without need.
- Avoid new dependencies unless required, and do not run unrelated dependency upgrades.
