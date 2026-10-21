---
description: "Use when creating or modifying pages, HTML documents, metadata, routes, sitemaps, or robots files where search engine optimization matters. Covers metadata, semantic markup, structured data, crawlability, and indexing."
applyTo: ["**/*.html", "**/{app,pages}/**/*.{jsx,tsx}", "**/{robots.txt,sitemap.xml}"]
---

# SEO Guidelines

- Give every page a unique, descriptive `<title>` (about 50-60 characters) and a unique `<meta name="description">` (about 150-160 characters).
- Set `<html lang>`, a responsive `<meta name="viewport">`, and a `<link rel="canonical">` to the preferred URL to prevent duplicate content.
- Use one `<h1>` per page and a logical heading hierarchy with semantic elements (`header`, `nav`, `main`, `article`, `section`, `footer`).
- Add Open Graph and Twitter Card tags (`og:title`, `og:description`, `og:image`, `og:url`, `twitter:card`) with an absolute image URL.
- Use clean, readable, lowercase, hyphenated URLs, and keep them stable; add redirects when URLs change.
- Use descriptive link text and real `<a href>` links so crawlers can follow them; do not rely on click handlers for navigation.
- Provide meaningful `alt` text for images and use descriptive file names.
- Add JSON-LD structured data (`Organization`, `Article`, `Product`, `BreadcrumbList`, `FAQPage`) that matches visible page content, and validate it.
- Render important content on the server or at build time (SSR/SSG) rather than only client-side; in Next.js use the Metadata API, `generateMetadata`, `sitemap`, and `robots` conventions.
- Maintain `robots.txt` and an up-to-date `sitemap.xml`; use `noindex` only on pages meant to stay out of search results, and never block CSS or JS needed for rendering.
- Keep pages fast and mobile-friendly, since Core Web Vitals affect ranking.
- Return correct HTTP status codes (200, 301, 404, 410) and provide a useful 404 page.
- Avoid hidden text, keyword stuffing, and duplicated content across pages.
