---
description: "Use when creating or editing Dockerfiles, docker-compose, GitHub Actions workflows, CI/CD pipelines, deployment, or environment separation."
applyTo: ["**/Dockerfile*", "**/docker-compose*.{yml,yaml}", "**/.dockerignore", "**/.github/workflows/*.{yml,yaml}"]
---

# Docker and CI/CD

## Docker
- Use small pinned base images (`node:22-alpine`, `python:3.13-slim`), never `latest`.
- Use multi-stage builds: build stage with dev dependencies, final stage with only production files.
- Copy dependency manifests first and install, then copy source, to use layer caching; use `npm ci`.
- Run as a non-root user; no secrets in image layers or build args; pass secrets at runtime.
- Add `.dockerignore` (`node_modules`, `.git`, `.env*`, build output); add a `HEALTHCHECK`; one process per container.
- Use `docker-compose` for local dev with named volumes and separate `dev` and `prod` configs.

## GitHub Actions
- Pipeline order: install, lint (Oxlint), typecheck, test, build, deploy; fail fast and run jobs in parallel where possible.
- Pin actions to a major version or commit SHA; set minimal `permissions` (`contents: read`).
- Cache dependencies (`actions/setup-node` with `cache: npm`); run `npm ci`; test on the Node version used in production.
- Run `npm audit` and optionally CodeQL; upload test and Playwright reports as artifacts.
- Use `concurrency` to cancel outdated runs on the same branch.

## Environments and deploy
- Separate `development`, `staging`, and `production` with their own variables and secrets (GitHub Environments, with approvals for production).
- Never reuse production secrets or databases in other environments.
- Deploy from the main branch only after checks pass; build once and promote the same artifact.
- Run database migrations as a separate, reviewed step; support rollback.
- Add preview deployments for pull requests when possible (Vercel, Netlify).
