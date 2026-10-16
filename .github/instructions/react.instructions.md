---
description: "Use when creating or modifying React components, styles, or frontend tooling. Covers component structure, React conventions, CSS, and project dependencies."
applyTo: "src/**/*.{js,jsx,ts,tsx,css}"
---

# React Guidelines

- Follow the existing project structure and conventions. For new components, use an individual component or component-group folder, such as `src/components/component/Component.jsx`, with styles in a separate `styles.css` file.
- Use ES modules (`import`/`export`) and relative paths for local imports.
- Write function components using named function declarations and default exports, using the component's actual name (for example, `export default function Button() { ... }`).
- Prefer standard React hooks (`useState`, `useEffect`, `useRef`, `useMemo`, `useContext`, `useCallback`, and `useReducer`). Use other hooks when they provide a clear benefit.
- Prefer concise conditional expressions when they remain readable; use `if` statements for complex branching or early returns.
- Use `async`/`await` for asynchronous code rather than `.then()` chains.
- Define event handlers once and pass references such as `onClick={handleClick}` or `onChange={handleChange}`.
- Reuse the project's existing theme, design tokens, and prebuilt styling or component system where available. Keep component styles consistent with the rest of the application and avoid unnecessary custom CSS.
- Use Vite and Oxlint for new project setup when appropriate. Preserve the existing build and lint tools in established projects unless a migration is requested.
- Use the latest stable React version supported by the project's dependencies and tooling. Don't upgrade dependencies as an unrelated change.
- Avoid unnecessary dependencies, complex abstractions, and function overloading. Prefer built-in platform and framework capabilities.
- Make focused changes: preserve existing behavior and avoid rewriting entire files or functions when a smaller change will do.
- Add useful debugging support when needed, but avoid noisy logs or leaving temporary diagnostics in production code.
- Keep comments brief and add them only when they clarify non-obvious behavior.
