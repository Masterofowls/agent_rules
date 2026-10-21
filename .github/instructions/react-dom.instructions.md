---
description: "Use when creating or modifying React DOM entry points, root rendering, portals, hydration, or flushSync. Covers createRoot, StrictMode, portals, and client/server rendering APIs."
applyTo: ["**/{main,index,client,entry-client,entry-server}.{js,jsx,ts,tsx}"]
---

# React DOM Guidelines

- Use the React 18+ client API: `createRoot(document.getElementById('root')).render(...)` from `react-dom/client`. Never use the removed `ReactDOM.render` or `ReactDOM.hydrate`.
- Create the root once at the app entry point, and guard against a missing root element with a clear error.
- Wrap the app in `<StrictMode>` in development to surface unsafe effects and impure rendering; do not remove it to hide warnings.
- Put global providers (router, store, theme) around `<App />` in the entry file, keeping the entry file small.
- For server-rendered apps, hydrate with `hydrateRoot` from `react-dom/client`, and ensure server and client markup match to avoid hydration errors. Avoid reading `window`, random values, or dates during render.
- Use `createPortal` from `react-dom` for modals, tooltips, and overlays that must render outside their parent DOM, and clean up portal containers.
- Use `flushSync` only when a synchronous DOM update is truly required, since it hurts performance.
- Use `react-dom/server` APIs (`renderToPipeableStream`, `renderToString`) only in server entry files, never in client bundles.
- Use `root.unmount()` when tearing down a manually created root, and register error handlers (`onCaughtError`, `onUncaughtError`, `onRecoverableError`) for debugging.
- Prefer React refs and state over direct DOM manipulation (`document.querySelector`); use `useRef` when DOM access is necessary.
- Make focused changes that preserve the existing mounting and provider order.
