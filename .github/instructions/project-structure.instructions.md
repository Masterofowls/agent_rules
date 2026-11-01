---
description: "Use when creating, moving, or organizing files and folders in a project: React, Redux, feature-based (feature-sliced) structure, backend layout, naming, and import boundaries."
applyTo: ["src/**", "**/{server,backend,api,app}/**/*.{js,ts,py}", "**/package.json"]
---

# Project structure

## Principles
- Group by feature (domain), not by file type; code that changes together lives together.
- Keep the existing structure of a project; follow it before introducing a new one, and never reorganize folders unasked.
- Every component or component group gets its own folder with its own `styles.css` (see the React instructions).
- Name folders in `kebab-case` or lowercase, components in `PascalCase`, hooks as `useThing`, everything else in `camelCase`.
- One main export per file; avoid dumping into `utils` and `helpers`; name files by what they hold.

## React feature-based layout (Feature-Sliced Design, light)
Layers from top to bottom; a layer imports only from layers below it, never above or sideways between features.

```
src/
  app/          providers, router, store setup, global styles, entry (main.jsx, App.jsx)
  pages/        route-level screens; compose features and widgets
  widgets/      large UI blocks made of several features (Header, ProductList)
  features/     user actions with business value (auth, add-to-cart, search)
    auth/
      components/login-form/LoginForm.jsx + styles.css
      api/        RTK Query endpoints (authApi.js)
      model/      slice, selectors, hooks, types (authSlice.js)
      lib/        feature-only helpers
      index.js    public API: export only what other layers may use
  entities/     business objects (user, product, order) with their UI, api, and model
  shared/       reusable code with no business logic
    ui/         design-system components (Button, Input, Modal)
    lib/        helpers, formatters, hooks
    api/        base API client, RTK Query base `createApi`
    config/     env, constants, routes
    styles/     tokens.css, reset.css, global.css
    assets/     images, fonts, icons
```
- Import a feature only through its `index.js`; do not reach into its internals.
- Small projects may start with `src/components`, `src/pages`, `src/hooks`, `src/store`, `src/styles`, and move to features when a domain grows past a few files.
- Put shared, business-free components in `shared/ui` (or `src/components` in small projects); put feature-specific components inside the feature.

## Redux and RTK
- Large projects: one store in `app/store.js`; each feature owns its slice in `model/` and its endpoints in `api/`.
- Inject feature slices and endpoints into the root reducer and the base API (`injectEndpoints`) instead of one giant file.
- Keep selectors next to the slice; export typed hooks (`useAppDispatch`, `useAppSelector`) from `app/` or `shared/lib`.
- Keep server data in RTK Query, UI and client state in slices; do not duplicate fetched data in slices.

## Routing and pages
- One folder per page in `pages/`, with its route component, styles, and a lazy-loaded export (`React.lazy`); keep the route table in `app/router`.
- Pages stay thin: layout and composition only, logic lives in features and entities.

## Backend layout (Express, FastAPI, Django, Flask)
- Node: `src/` with `routes/`, `controllers/`, `services/`, `models/` (or `db/`), `middleware/`, `schemas/` (Zod), `config/`, `utils/`; the route calls the controller, the controller calls a service, the service touches the database.
- FastAPI: `app/` with `main.py`, `routers/`, `schemas/`, `services/`, `models/`, `dependencies.py`, `core/config.py`.
- Django: one app per domain (`apps/users`, `apps/orders`), each with `models.py`, `views.py`, `serializers.py`, `urls.py`, `tests/`.
- Flask: app factory in `app/__init__.py` with blueprints per domain.
- Keep business logic out of route handlers; keep config and secrets in environment variables.

## Monorepo and full-stack
- Use workspaces (`apps/web`, `apps/api`, `packages/shared`) when client and server share code; keep shared Zod schemas and types in `packages/shared`.
- Next.js: keep `app/` for routing only and import features from `src/features`; colocate `loading.jsx`, `error.jsx`, and route handlers with their route.

## Tests and root files
- Colocate tests with code (`Component.test.jsx`) and keep E2E tests in `e2e/` at the root.
- Root keeps config only: `package.json`, `vite.config.js`, `.oxlintrc.json`, `.env.example`, `Dockerfile`, `README.md`; no stray scripts or scratch files.
- Use relative imports as the project rules require; add an alias (`@/`) only if the project already uses one.
- Do not create placeholder or copy files (`Component copy.jsx`, `old/`). Delete existing unused files or folders only when necessary for the requested task and explicitly approved under the agent permissions.
