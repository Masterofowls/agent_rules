---
description: "Use when creating or modifying FastAPI apps, routers, endpoints, Pydantic schemas, dependencies, or middleware. Covers structure, async handling, validation, and security."
applyTo: ["**/{routers,routes,api,schemas,dependencies,endpoints}/**/*.py", "**/{main,app,schemas,dependencies}.py"]
---

# FastAPI Guidelines

- Follow the project's existing structure. For new APIs, split into `routers/`, `schemas/`, `services/`, and `dependencies` modules, and register routers with `APIRouter` and `include_router`.
- Define request and response bodies as Pydantic models, set `response_model`, and use explicit status codes.
- Use `async def` endpoints for non-blocking I/O with async libraries; use plain `def` for blocking code so FastAPI runs it in a threadpool. Never block the event loop.
- Use `Depends` for shared logic such as database sessions, authentication, and settings, and use `Annotated` for typed dependencies.
- Keep endpoints thin: put business logic in service modules.
- Raise `HTTPException` or register exception handlers for consistent error responses; do not leak internal details.
- Validate input with Pydantic and path/query constraints (`Query`, `Path`, `Field`) instead of manual checks.
- Load configuration from environment variables with `pydantic-settings`; never hard-code secrets.
- Restrict CORS origins, require authentication on protected routes, and hash passwords with a vetted library.
- Use `lifespan` for startup and shutdown logic instead of deprecated event handlers.
- Add tests with `TestClient` or `httpx.AsyncClient`, and use `logging` for debugging.
- Make focused changes that preserve existing routes, schemas, and response shapes.
