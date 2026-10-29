---
description: "Use when a project has Russian as the main or an optional language: UI text, copy, i18n files, docs, credits, errors. Covers grammar, cases, agreement, typography, and natural phrasing."
applyTo: ["**/*.{jsx,tsx,html,json,md}", "**/{locales,i18n,lang,translations}/**", "src/**/*.{js,ts}"]
---

# Russian language

Applies when Russian is the main or an optional language. Use the `russian-language` skill for details.

## Natural phrasing
- Write natural Russian, not word-for-word English; rephrase when a literal translation sounds off.
- Never use a person's name in the nominative after "сделан/создан/подготовлен"; the agent takes the instrumental case.
  - Wrong: "Этот сайт сделан Иван Иванов".
  - Right: "Сайт подготовил Иванов Иван", "Сайт сделан Ивановым Иваном", "Автор сайта — Иван Иванов".
- Prefer the active voice and short sentences; avoid chains of genitives and bureaucratic noun stacks.
- Do not use machine-translation patterns such as "Вы можете..." everywhere; use imperatives for actions ("Войти", "Сохранить").

## Cases and agreement
- Decline names, titles, and nouns correctly; use the right case after prepositions and verbs (в/на + предложный, к + дательный, без/для/от + родительный).
- Match adjectives, verbs, and numerals to gender, number, and case; check gender when addressing the user ("Вы вошли" / "Вы зарегистрированы").
- Avoid gendered phrasing when the gender is unknown: use neutral wording ("Регистрация выполнена") instead of "Вы зарегистрировались/зарегистрировалась".
- For names that may not decline (foreign, some surnames), rephrase so the name stays in the nominative ("Автор: Иван Иванов", "Разработчик — Иван Иванов").

## Plurals and numbers
- Russian has three plural forms (1 файл, 2 файла, 5 файлов); never build plurals with `+ "s"` or a single suffix.
- Use `Intl.PluralRules("ru")` or the i18n library's plural rules with `one`, `few`, `many`, `other` forms.
- Format numbers, dates, currency, and units with `Intl` and the `ru-RU` locale (`1 234,56`, `29 октября 2026 г.`, `₽`).
- Use a non-breaking space between number and unit and before the dash and abbreviations ("5 МБ", "10 ₽").

## Typography
- Use «ёлочки» as primary quotes and „лапки“ for nested quotes; use the long dash "—" with spaces for dashes and "–" for ranges.
- Do not put a space before `.`, `,`, `:`, `;`, `!`, `?`; keep `…` as one character.
- Prefer "ё" where it avoids ambiguity (все/всё); stay consistent across the project.
- Capitalize only the first word of a heading and proper nouns; do not use Title Case.
- Do not use all caps for body text; use CSS `text-transform` for styling, not typed capitals.

## UI text
- Button and menu labels: short infinitive or imperative, consistent across the app ("Сохранить", "Отмена", "Удалить").
- Error messages say what happened and how to fix it, politely and without blame ("Не удалось сохранить. Проверьте подключение и повторите попытку.").
- Use formal "вы" (lowercase in UI text; capital "Вы" only in formal letters) consistently; never mix "ты" and "вы".
- Keep terms uniform: one Russian word per concept (for example always "войти", not "залогиниться").
- Avoid unnecessary anglicisms and transliteration when a normal Russian word exists, but keep established terms ("email", "сайт", "браузер").

## Implementation
- Store all text in locale files (for example `locales/ru.json`); never hard-code strings in components.
- Set `<html lang="ru">`, use the `ru` locale for `Intl`, and set `lang="ru"` on mixed-language fragments.
- Use UTF-8 everywhere; fonts must include Cyrillic (test with "ЁёЪъЫы"), and verify the fallback font also has Cyrillic.
- Leave room for text growth: Russian is about 10-30% longer than English; use flexible layouts, no fixed-width buttons, and `hyphens: auto` with `lang="ru"` for long words.
- Sort and compare with `localeCompare("ru")` or `Intl.Collator("ru")`.
- When Russian is optional, provide a language switcher, store the choice, and keep keys identical across locales.
- Proofread all Russian output for spelling, agreement, and case before finishing.
