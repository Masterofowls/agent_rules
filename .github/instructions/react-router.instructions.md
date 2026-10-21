---
description: "Use when creating or modifying React Router routes, layouts, loaders, actions, navigation, or route modules. Covers route structure, data loading, and navigation."
applyTo: ["**/{routes,router,pages}/**/*.{js,jsx,ts,tsx}", "**/{routes,root,router}.{js,jsx,ts,tsx}"]
---

# React Router Guidelines

- Follow the project's existing mode and version (framework mode, data mode, or declarative mode) and do not mix modes in the same app.
- Import from the package already used by the project (`react-router` or `react-router-dom`) with ES module imports.
- Define routes centrally in one route configuration and use nested routes with layout routes and `<Outlet />` instead of repeating layout markup.
- Load data in route `loader`s and handle mutations in route `action`s when the project uses data routers; avoid fetching route data in `useEffect`.
- Use `async`/`await` in loaders and actions. Throw `Response` objects or errors for failures, and provide `errorElement` or `ErrorBoundary` per route.
- Use `<Link>`, `<NavLink>`, `<Form>`, `useNavigate`, and `redirect` for navigation instead of raw anchors or manual `window.location` changes.
- Prefer lazy route loading for large pages, and keep route components in their own component folders with separate CSS files.
- Read URL state with `useParams` and `useSearchParams` rather than parsing `window.location` manually.
- Create the router once at the app entry (`createBrowserRouter` + `RouterProvider`), and use `useRouteError` in error elements to display route failures.
- Use relative links and routes inside nested layouts, add a catch-all `*` route for 404 pages, and use `useNavigation` for pending UI during loads and submissions.
- Use `useFetcher` for mutations that should not trigger navigation, and `shouldRevalidate` only to avoid unneeded reloads.
- Make focused changes that preserve existing paths, route IDs, and navigation behavior.
