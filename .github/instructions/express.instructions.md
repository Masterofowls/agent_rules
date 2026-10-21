---
description: "Use when creating or modifying Express servers, routes, middleware, controllers, or REST API code. Covers structure, async handling, validation, errors, and security."
applyTo: ["**/{server,api,routes,controllers,middleware,middlewares}/**/*.{js,ts}", "**/{server,app}.{js,ts}"]
---

# Express Guidelines

- Follow the existing project structure. For new APIs, separate app setup, routes, controllers, and middleware into individual files or folders.
- Use ES modules (`import`/`export`) and relative paths for local imports.
- Use async/await in handlers. Use Express 5 native async error handling when available; otherwise forward errors with `next(error)`.
- Define handlers as named functions and pass references, such as `router.get('/', getItems)`.
- Use `express.Router()` per resource and keep route files limited to routing; put business logic in controllers or services.
- Validate and sanitize all request input (body, params, query, headers) before use, with the validation approach already used in the project.
- Use one centralized error-handling middleware with consistent JSON error responses and correct HTTP status codes. Do not leak stack traces or internal details in production.
- Apply security basics: restrict CORS to known origins, set secure headers, limit request body size, and never hard-code secrets; use environment variables.
- Add useful request and error debugging logs, and never log secrets or personal data.
- Prefer built-in Express and Node.js features (`express.json()`, `fetch`, `crypto`) before adding packages.
- Make focused changes: preserve existing routes, response shapes, and middleware order.
