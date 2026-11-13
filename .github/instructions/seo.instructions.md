---
description: "Use when creating or modifying pages, HTML documents, metadata, routes, sitemaps, or robots files where search engine optimization matters. Covers metadata, semantic markup, structured data, crawlability, and indexing."
applyTo: ["**/*.html", "**/{app,pages}/**/*.{jsx,tsx}", "**/{robots.txt,sitemap.xml}"]
---

# SEO Guidelines

- Give indexable pages unique, descriptive titles and descriptions. Roughly 50-60 and 150-160 characters are editorial guides, not search-engine limits or ranking guarantees; prioritize accuracy and avoid truncating useful meaning to meet a count.
- Set `<html lang>`, a responsive `<meta name="viewport">`, and a `<link rel="canonical">` to the preferred URL to prevent duplicate content.
- Use one `<h1>` per page and a logical heading hierarchy with semantic elements (`header`, `nav`, `main`, `article`, `section`, `footer`).
- Add Open Graph and Twitter Card tags (`og:title`, `og:description`, `og:image`, `og:url`, `twitter:card`) with an absolute image URL.
- Use clean, readable, lowercase, hyphenated URLs, and keep them stable; add redirects when URLs change.
- Use descriptive link text and real `<a href>` links so crawlers can follow them; do not rely on click handlers for navigation.
- Provide meaningful `alt` text for images and use descriptive file names.
- Add relevant JSON-LD that matches visible content, prices, availability, and authorship; validate it against the search engine's current supported features. Do not invent reviews, ratings, or FAQs, and do not promise rich-result eligibility.
- Render important content on the server or at build time (SSR/SSG) rather than only client-side; in Next.js use the Metadata API, `generateMetadata`, `sitemap`, and `robots` conventions.
- Maintain `robots.txt` and an up-to-date `sitemap.xml`; use `noindex` only on pages meant to stay out of search results, and never block CSS or JS needed for rendering.
- Keep pages fast and mobile-friendly, since Core Web Vitals affect ranking.
- Return correct HTTP status codes (200, 301, 404, 410) and provide a useful 404 page.
- Avoid hidden text, keyword stuffing, and duplicated content across pages.

## Indexing and URL policy
- Keep canonical URLs absolute and consistent across HTML, redirects, internal links, metadata, and sitemaps. Canonicals are hints, not redirects; do not canonicalize distinct pages to a generic home page.
- Put only preferred, indexable 200-status URLs in sitemaps. Exclude redirects, errors, private pages, and `noindex` URLs; set `lastmod` only for meaningful content changes.
- `robots.txt` controls crawling, not privacy or guaranteed deindexing. Use authentication for private content; crawlers must be able to fetch a page to see its `noindex`. Inspect both HTML robots tags and `X-Robots-Tag`.
- Keep previews and staging authenticated or consistently `noindex`; verify production does not inherit those settings. Do not change live indexing controls without target authorization.
- For multilingual sites, use valid language/region tags, reciprocal `hreflang` links, and self-canonicals for each language. Use `x-default` only where a genuine default selector/page exists.
- Define policies for filters, sorting, tracking parameters, pagination, and internal search. Do not accidentally hide useful paginated content or produce unlimited crawlable URL combinations.
- Preserve query parameters deliberately in redirects, avoid redirect chains/loops, and return real 404/410 responses instead of soft-404 pages with status 200.

## Verification
- Inspect rendered HTML and actual HTTP responses on representative routes, including mobile and direct navigation. Check metadata, crawlable links, status codes, canonicals, robots, sitemap URLs, and structured data together.
- Use the existing SEO skill and local tools; do not submit private/staging content to third-party validators without approval. Search Console or indexing submissions need authorization for the property.
- Measure crawl/indexing evidence and Core Web Vitals separately. A Lighthouse score or valid schema is not proof of indexing, ranking, or traffic growth.
