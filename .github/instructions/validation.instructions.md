---
description: "Use when validating request data, forms, configuration, uploads, or external API responses with Zod, Pydantic, class-validator, or existing schemas."
applyTo: ["**/{schemas,validators,validation,dto,forms,api,routes,routers}/**/*.{js,jsx,ts,tsx,py}", "**/*.dto.ts"]
---

# Runtime validation

- Validate untrusted data at boundaries. Static types, client-side validation, and ORM models do not replace server-side validation.
- Reuse the project's validation library and schemas; do not add multiple competing validators.
- Share safe request contracts between client and server when supported, but never export server secrets or internal database models to the browser.
- Define create, update, and response contracts explicitly. Reject or strip unknown fields according to the API contract; never allow mass assignment of roles, ownership, or other server-controlled fields.
- Check string lengths, array sizes, numeric ranges, enum values, upload size and content, and cross-field rules. Require bounded pagination.
- Distinguish missing, null, empty, zero, and false. Do not replace valid falsy values with defaults.
- Coerce intentionally: the string `"false"` must not become true through truthiness; reject invalid dates, non-finite numbers, and malformed IDs.
- Normalize only when the domain allows it. Do not trim passwords, alter display names, or lowercase whole email addresses without an explicit normalization policy.
- Return stable field paths and localized, actionable errors through the existing error format; do not log sensitive submitted values.
- Validate environment variables once at startup and fail explicitly on invalid configuration. Validate external service responses before using them.
- Pydantic projects follow the installed version; NestJS uses its existing validation pipes; TypeScript schema projects follow the Zod instructions.
- Test valid input and boundary cases, unexpected fields, malformed types, cross-field failures, and authorization separately. Validation is not authorization.
