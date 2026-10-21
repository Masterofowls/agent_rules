---
description: "Use when building website or app frontends, UI components, pages, layouts, forms, or interactive elements. Covers choosing pre-made component libraries (Radix, React Aria, Ant Design, Material UI, shadcn, Untitled UI, Magic UI, Aceternity UI, React Bits) and avoiding Tailwind by default."
applyTo: ["**/*.{jsx,tsx,css,html}", "src/**/*.{js,ts}"]
---

# Frontend Component Library Guidelines

- Use pre-made components from established libraries instead of building common UI from scratch (buttons, inputs, selects, dialogs, menus, tabs, tooltips, tables, forms, navigation, toasts, accordions, date pickers).
- Check the project's existing UI library first and keep using it; do not mix several libraries for the same kind of component.
- Prefer libraries that do not require Tailwind, in this order:
  1. Radix (Themes or Primitives) and React Aria Components, which are unstyled and styled with the project's own `styles.css` files.
  2. Ant Design and Material UI (Material Design) for complete styled component sets.
- Use Tailwind-based libraries only when the above lack the component or the project already uses Tailwind: shadcn/ui, Untitled UI, Magic UI, Aceternity UI, and React Bits.
- Do not add Tailwind, PostCSS plugins, or a Tailwind config to a project that does not already use it without asking the user first. Prefer the plain CSS or CSS-in-JS variants when a library offers them (for example React Bits CSS versions).
- Use animated and decorative components (Magic UI, Aceternity UI, React Bits) sparingly for hero sections and highlights, not for core controls. Respect `prefers-reduced-motion` and keep them off the critical rendering path.
- Prefer accessible primitives (Radix, React Aria) for interactive widgets so keyboard support, focus management, and ARIA come built in; do not rebuild them by hand.
- Configure one shared theme (colors, typography, spacing, radius, dark mode) through the library's theme tokens or CSS variables, so every component matches the global theme.
- Wrap library components in small project components only to apply theme defaults or shared behavior; do not copy-paste and heavily fork library code.
- Import only the components used, with named imports and ES modules, so tree shaking keeps the bundle small, and check bundle size before adding a library.
- For copy-in libraries (shadcn, Magic UI, Aceternity UI, React Bits), add components through their CLI or documented install steps, place them in their own component folder, and keep their CSS in a separate stylesheet when the project is not using Tailwind.
- Follow each library's current documentation for installation and API, and use the latest stable version supported by the project's React version.
- Build custom components only when no suitable library component exists, and keep them consistent with the chosen library's design and the project's theme.
- Do not add a new UI library or dependency without confirming it is needed and not already provided by the existing one.
