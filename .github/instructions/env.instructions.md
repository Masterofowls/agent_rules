---
description: "Use when creating or modifying .env files, environment variables, or configuration secrets. Covers secret handling, naming, examples, and validation."
applyTo: ["**/.env", "**/.env.*", "**/*.env"]
---

# Environment Variable Guidelines

- Never commit real secrets, tokens, passwords, or private keys. Keep real `.env` files out of version control via `.gitignore`.
- Provide a committed `.env.example` with every required variable, safe placeholder values, and no real credentials.
- Use `UPPER_SNAKE_CASE` names, group related variables, and use clear prefixes such as `DB_` or `AUTH_`.
- Expose variables to client code only when intended, using the framework prefix (`VITE_`, `NEXT_PUBLIC_`), and never put secrets behind those prefixes.
- Do not hard-code values in source that belong in configuration; read them from the environment in one config module.
- Validate required variables at startup and fail fast with a clear message that names the missing variable but never prints its value.
- Do not log, echo, or display secret values in output, errors, or debugging.
- Keep separate files per environment (`.env.development`, `.env.production`, `.env.test`) and avoid sharing production secrets locally.
- Use `KEY=value` format without spaces around `=`, and quote values that contain spaces or special characters.
- Rotate any secret that has been exposed, and remove it from git history.
