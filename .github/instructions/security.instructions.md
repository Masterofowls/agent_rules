---
description: "Use when writing or reviewing web code for security: XSS, CSRF, CORS, CSP headers, input sanitizing, secrets in client code, dependency audits, and safe cookies."
applyTo: "**/*.{js,jsx,ts,tsx,py,html}"
---

# Web security

## Injection and XSS
- Never trust input; validate on the server with a schema and sanitize before rendering.
- Avoid HTML injection sinks; if rendering untrusted HTML is required, sanitize it with a maintained, context-appropriate sanitizer such as DOMPurify. Never execute untrusted input with `eval` or `Function`; HTML sanitization does not make executable code safe.
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

## Authorization and infrastructure
- Enforce permissions, record ownership, and tenant boundaries on every server operation, including downloads and background jobs. Do not trust client-provided roles or object IDs.
- Prevent mass assignment: explicitly allow writable fields and keep roles, ownership, and private columns server-controlled.
- Protect outbound requests against SSRF with destination allow-lists, redirect checks, and private-network restrictions. Do not fetch arbitrary user URLs from privileged servers.
- Prevent path traversal with validated identifiers and containment checks; do not pass untrusted paths or commands to a shell.
- Verify webhook signatures against the original payload, enforce replay protections where supported, and make event processing idempotent.
- Configure session expiration, rotation, and logout invalidation; follow the dedicated authentication instructions.

## Security verification
- Run supported secret, dependency, and static-analysis checks on affected surfaces. Review actionable findings; never silence audits or force unrelated upgrades to obtain a clean result.
- Test rejected input, unauthorized access, cross-tenant requests, CSRF protections, and safe error responses in an isolated environment.
- Security testing requires authorization for the exact target. Never scan third-party systems, perform destructive probes, or send production data to external audit services without permission.
- Report evidence, impact, and remediation concisely; do not claim the application is secure solely because automated checks passed.
