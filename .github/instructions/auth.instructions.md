---
description: "Use when implementing authentication, sessions, JWT, cookies, OAuth, password hashing, or rate limiting."
applyTo: ["**/{auth,session,sessions,login,middleware,middlewares}/**/*.{js,ts,py}", "**/*{auth,Auth,session,Session}*.{js,ts,tsx,py}"]
---

# Authentication and sessions

## Sessions vs JWT
- Prefer server-side sessions in `HttpOnly`, `Secure`, `SameSite=Lax` cookies for web apps; they are revocable and simple.
- Use JWT for stateless APIs, mobile clients, or service-to-service calls; keep access tokens short-lived (5-15 min) with a rotating refresh token.
- Never store tokens in `localStorage` or `sessionStorage`; use `HttpOnly` cookies.
- Always verify signature, `exp`, `iss`, and `aud`; use a strong algorithm (RS256/ES256 or HS256 with a long secret); never accept `alg: none`.
- Keep JWT payloads minimal; no sensitive data.

## Passwords
- Hash with Argon2id (or bcrypt cost 12+, scrypt); never MD5/SHA for passwords; never store plain text.
- Enforce length (12+) over complexity; check against breached-password lists; allow password managers and paste.
- Use constant-time comparison; return generic errors ("Invalid email or password").
- Reset links are single-use, expire quickly, and are stored hashed.

## OAuth and SSO
- Use a proven library or provider (Auth.js, Lucia, Passport, Clerk, Auth0, Supabase Auth); do not write your own crypto.
- Use Authorization Code flow with PKCE; validate `state` and `nonce`; register exact redirect URIs.
- Request the minimum scopes; link accounts only by verified email.

## Protection
- Rate limit login, signup, reset, and verification endpoints per IP and per account; add lockout or backoff.
- Support MFA (TOTP or passkeys/WebAuthn) for sensitive accounts.
- Regenerate the session ID on login and privilege change; invalidate on logout and password change.
- Check authorization on the server for every request (role and ownership); never trust client-side checks.
- Log auth events (login, failure, reset) without secrets.
