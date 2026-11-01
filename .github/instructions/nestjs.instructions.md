---
description: "Use when developing NestJS modules, controllers, providers, DTOs, guards, pipes, interceptors, or nest-cli configuration."
applyTo: ["**/nest-cli.json", "**/*.{module,controller,service,guard,pipe,interceptor,filter,dto}.ts"]
---

# NestJS

- Confirm the installed NestJS version and existing architecture before changing code. Organize modules by domain; avoid generating duplicate application scaffolding.
- Keep controllers thin: validate and map HTTP input, call an injected service, and return the response. Business logic belongs in services.
- Use constructor injection and explicit provider tokens for interfaces. Export only providers another module needs; avoid global modules and circular dependencies.
- Use runtime DTO classes with the existing validation library, or the project's schema-based pipes. TypeScript interfaces alone do not validate requests.
- Configure validation centrally; reject unexpected fields where the API contract requires it. Parse IDs, booleans, and pagination explicitly rather than relying on unchecked transformation.
- Use guards for authentication and authorization, pipes for validation, interceptors for cross-cutting response or timing behavior, and exception filters for safe error mapping.
- Check roles, permissions, and record ownership on the server. Do not treat successful authentication as authorization.
- Validate configuration at startup with the existing ConfigModule setup; never put secrets in decorators or source code.
- Reuse the existing database provider and pool. Keep transactions inside the service operation and propagate the transaction client to dependent writes.
- Use Nest's logger or the configured structured logger with request IDs; redact credentials and private payloads.
- Document request DTOs, responses, authentication, and error statuses with the existing OpenAPI setup.
- Use TestingModule for focused service tests and the existing HTTP test client for endpoints; cover invalid input, authorization, and failure paths.
- Enable shutdown hooks where required by the deployment and close database connections and workers cleanly.
