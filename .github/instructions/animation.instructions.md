---
description: "Use when adding animation, transitions, or motion: Framer Motion, GSAP, CSS transitions, performance-safe transforms, and reduced motion."
applyTo: ["**/*.{jsx,tsx,css}", "src/**/*.{js,ts}"]
---

# Animation

## Choose the simplest tool
- Prefer CSS transitions and `@keyframes` for hover, focus, and simple state changes; use the View Transitions API for page transitions when supported.
- Use Framer Motion (`motion`) for React mount/unmount, layout, gestures, and shared-element animation.
- Use GSAP for complex timelines, scroll-driven sequences, and SVG; clean up with `gsap.context()` and `ctx.revert()` in `useEffect`.
- Do not add an animation library for effects CSS can do.

## Performance
- Animate only `transform` and `opacity`; avoid animating `width`, `height`, `top`, `left`, `margin`, or `box-shadow`.
- Use `will-change` sparingly and remove it after use; avoid layout thrashing and animating many elements at once.
- Use `requestAnimationFrame` instead of `setInterval` for manual animation; use `IntersectionObserver` to start animations only when visible.
- Lazy-load heavy animation libraries and Lottie files; keep animation assets small.

## Design
- Keep motion short and purposeful: 150-300ms for UI feedback, up to 500ms for larger transitions; use ease-out for entering and ease-in for leaving.
- Define duration and easing as design tokens and reuse them.
- Animate to explain change (state, hierarchy, feedback), not to decorate; avoid looping or distracting motion.

## Accessibility
- Respect `prefers-reduced-motion`: disable or replace motion with fades (`@media (prefers-reduced-motion: reduce)`; Framer Motion `useReducedMotion`; GSAP `matchMedia`).
- Never flash content more than three times per second; never hide essential content behind animation.
- Provide pause controls for autoplaying or long animations; keep focus visible during transitions.
