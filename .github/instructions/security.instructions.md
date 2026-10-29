---
description: "Use when writing or reviewing web code for security: XSS, CSRF, CORS, CSP headers, input sanitizing, secrets in client code, dependency audits, and safe cookies."
applyTo: "**/*.{js,jsx,ts,tsx,py,html}"
---

# Web security

## Injection and XSS
- Never trust input; validate on the server with a schema and sanitize before rendering.
- Do not use `dangerouslySetInnerHTML`, `innerHTML`, or `eval`; if unavoidable, sanitize with DOMPurify.
- Use parameterized queries or an ORM; never build SQL by string concatenation.
- Escape output by context (HTML, attribute, URL, JS); validate URLs and allow only `http`, `https`, and `mailto` schemes.
- Validate file uploads by type, size, and content; store outside the web root with generated names.

## CSRF, CORS, headers
- Use `SameSite=Lax` or `Strict` cookies plus a CSRF token for state-changing requests that use cookies.
- Restrict CORS to an explicit origin allow-list; never `*` with credentials.
- Set security headers (helmet for Express): `Content-Security-Policy`, `Strict-Transport-Security`, `X-Content-Type-Options: nosniff`, `Referrer-Policy`, `Permissions-Policy`, `frame-ancestors`.
- Start CSP strict (`default-src 'self'`) and use nonces instead of `unsafe-inline`.
- Serve everything over HTTPS and redirect HTTP.

## Secrets and config
- No secrets in client code, repository, logs, or `VITE_*`/`NEXT_PUBLIC_*` variables; those are public.
- Keep secrets in environment variables or a secret manager; rotate if leaked; commit only `.env.example`.
- Call third-party APIs that need secrets from the server only.

## Dependencies
- Run `npm audit` (or `pip-audit`) in CI; update vulnerable packages; commit lockfiles.
- Prefer built-in logic and few dependencies; check package maintenance and popularity before adding.
- Pin or range versions deliberately; enable Dependabot or Renovate.

## Errors and data
- Do not expose stack traces, SQL errors, or internal paths to users.
- Collect the minimum personal data; encrypt sensitive data at rest and in transit; never log passwords, tokens, or card data.
- Apply rate limits to login, signup, reset, and public APIs.
