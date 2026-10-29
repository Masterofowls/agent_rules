---
description: "Use when designing or changing REST APIs: resource naming, HTTP methods, status codes, pagination, error format, versioning, and OpenAPI."
applyTo: ["**/{api,routes,routers,controllers,endpoints}/**/*.{js,ts,py}", "**/openapi.{json,yaml,yml}"]
---

# API design

## REST conventions
- Use plural nouns for resources (`/users`, `/users/{id}/orders`); no verbs in paths; keep nesting to two levels.
- Methods: `GET` read, `POST` create, `PUT` replace, `PATCH` partial update, `DELETE` remove; `GET` is safe and idempotent.
- Use JSON with consistent `camelCase` (or `snake_case` in Python APIs) across the whole API.
- Use ISO 8601 UTC dates and string IDs.

## Status codes
- `200` OK, `201` created (with `Location`), `204` no content, `400` bad request, `401` unauthenticated, `403` forbidden, `404` not found, `409` conflict, `422` validation error, `429` too many requests, `500` server error.
- Never return `200` with an error body.

## Pagination, filtering, sorting
- Paginate every list endpoint; prefer cursor pagination for large or changing data, `page`/`limit` for simple cases; cap `limit`.
- Return `{ data, meta: { nextCursor, total } }` consistently.
- Filter and sort with query params (`?status=active&sort=-createdAt`); whitelist allowed fields.

## Error format
- One error shape everywhere, for example `{ "error": { "code": "VALIDATION_FAILED", "message": "...", "details": [{ "field": "email", "message": "..." }] } }`; consider RFC 9457 problem details.
- Messages are safe for users; codes are stable for clients; never leak internals.

## Versioning and compatibility
- Version in the path (`/api/v1`); add fields without breaking; never remove or rename within a version; deprecate with notice and `Sunset` header.

## Docs and validation
- Describe the API in OpenAPI and keep it in sync (generate from Zod/Pydantic schemas when possible).
- Validate all request bodies, params, and queries with schemas; return typed responses.
- Support idempotency keys for payments and other unsafe retries; set cache headers (`ETag`, `Cache-Control`) on `GET`.
