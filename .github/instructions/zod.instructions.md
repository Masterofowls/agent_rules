---
description: "Use when validating data with TypeScript and Zod: shared schemas between client and server, inferred types, parsing input, forms, and env validation."
applyTo: ["**/*zod*.{js,ts}", "**/{schemas,validators,validation}/**/*.{js,ts}"]
---

# TypeScript + Zod

Apply these rules only when Zod is used by the project, confirmed by dependencies or imports. Otherwise keep the existing validation library; TypeScript files alone do not justify adding Zod.

- Define each schema once with Zod in a shared module (for example `src/shared/schemas/user.ts`) and import it in both client and server.
- Derive types from schemas: `type User = z.infer<typeof userSchema>`; do not write the same type by hand.
- Validate at every boundary: request bodies, query/params, responses from external APIs, `localStorage`, and environment variables.
- Use `safeParse` for expected invalid input and return field errors; use `parse` only where failure is a bug.
- Compose schemas with `.pick`, `.omit`, `.partial`, `.extend`, and `z.discriminatedUnion` instead of copying them.
- Set error messages in schemas or map `issues` to user messages in one place; keep Russian/i18n messages in locale files.
- Use coercion deliberately for query strings and form values; validate boolean strings explicitly instead of relying on truthiness. Normalize email addresses only under the project's policy, never trim passwords, and set explicit string and array limits.
- Validate env once at startup (`envSchema.parse(process.env)`) and export a typed config; fail fast.
- Use form, OpenAPI, or ORM adapters only when the project needs that integration and uses the corresponding tools. Reuse installed adapters; do not add packages just because a schema exists.
- Never trust client validation; the server always re-validates with the same schema.
- Avoid `any` and unsafe casts; use `unknown` and narrow with schemas.
