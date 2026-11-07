---
description: "Use when adding images, video, audio, or fonts: responsive srcset, avif/webp, lazy loading, video optimization, and font loading."
applyTo: ["**/*.{jsx,tsx,html,css}", "src/**/*.{js,ts}"]
---

# Images, media, and fonts

## Images
- Use `avif` or `webp` with a `jpeg`/`png` fallback through `<picture>`; use SVG for icons and logos; compress every asset.
- Provide responsive images with `srcset` and `sizes`; never ship an image larger than its largest display size (times 2 for retina).
- Always set `width` and `height` (or `aspect-ratio`) to prevent layout shift.
- Use `loading="lazy"` and `decoding="async"` below the fold; for the main hero/LCP image use `fetchpriority="high"` and no lazy loading.
- Write meaningful `alt` text (see the accessibility instructions); use `object-fit` for cropping.
- Use the framework image component when available (`next/image`, Vite image plugins) and an image CDN when practical.

## Video and audio
- Compress video (`mp4` H.264 plus `webm`/AV1); keep short background loops under about 2MB; use `preload="metadata"` and a `poster`.
- Autoplay only `muted playsinline` videos; provide controls, captions (`<track>`), and a reduced-motion alternative.
- Lazy-load embeds (YouTube, maps) with a facade or `loading="lazy"` on `iframe`.

## Fonts
- Choose a project-specific font or pairing that supports the design system and audience; do not repeat one default font across unrelated projects.
- Use free-to-download font files with a compatible license, bundle optimized WOFF2 assets in the repository, and retain required license/attribution. Do not fetch fonts from Google Fonts API or another external font API.
- Subset bundled fonts to required scripts and weights; include Cyrillic when Russian is used and test glyph coverage. Prefer variable fonts where they reduce file count.
- Declare local `@font-face` sources and `font-display: swap`; preload only the critical local font file and provide a metric-matched system fallback.
- Use the design-system font tokens throughout the UI; do not apply one-off font families to individual components.

## Delivery
- Serve static assets with long-lived `Cache-Control` and hashed filenames, over a CDN, with Brotli or gzip.
- Check Lighthouse and Core Web Vitals (LCP, CLS, INP) after media changes.
