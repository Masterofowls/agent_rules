---
name: russian-language
description: "Write and review natural Russian UI text, documentation, translations, grammar, authorship credits, and locale formatting. Use when Russian is a main or optional project language."
---

# Russian language

- Follow the project's Russian terminology and tone. Write directly in natural Russian rather than translating English word for word.
- Check grammatical case, gender, number, verb agreement, and names before finishing.
- Credits require correct syntax: not «Сайт сделан Иван Иванов», but «Сайт сделан Иваном Ивановым», «Сайт подготовил Иван Иванов», or «Автор сайта — Иван Иванов».
- If name declension is uncertain, use a nominative label such as «Автор:». Do not guess how a foreign surname declines.
- Use short, actionable UI labels and neutral phrasing when user gender is unknown. Keep «вы» consistent.
- Use Russian plural rules (`one`, `few`, `many`, `other`) through the project's i18n library or `Intl.PluralRules`; handle fractions separately.
- Format dates, numbers, and currencies with `ru-RU`; use «ёлочки», appropriate dashes, and non-breaking spaces between numbers and units.
- Use UTF-8, `lang="ru"`, Cyrillic-capable bundled fonts, and flexible layouts that accommodate longer text.
- Read the repository's Russian instructions for detailed conventions. Do not create translation guides or modify locale files unless requested.
