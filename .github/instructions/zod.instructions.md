---
description: "Use when validating data with TypeScript and Zod: shared schemas between client and server, inferred types, parsing input, forms, and env validation."
applyTo: ["**/*.{ts,tsx}", "**/{schemas,validators,shared}/**/*.{js,ts}"]
---

# TypeScript + Zod

- Define each schema once with Zod in a shared module (for example `src/shared/schemas/user.ts`) and import it in both client and server.
- Derive types from schemas: `type User = z.infer<typeof userSchema>`; do not write the same type by hand.
- Validate at every boundary: request bodies, query/params, responses from external APIs, `localStorage`, and environment variables.
- Use `safeParse` for expected invalid input and return field errors; use `parse` only where failure is a bug.
- Compose schemas with `.pick`, `.omit`, `.partial`, `.extend`, and `z.discriminatedUnion` instead of copying them.
- Set error messages in schemas or map `issues` to user messages in one place; keep Russian/i18n messages in locale files.
- Use `z.coerce` for query strings and form values, `.trim()` and `.toLowerCase()` for emails, and explicit limits (`min`, `max`) on strings and arrays.
- Validate env once at startup (`envSchema.parse(process.env)`) and export a typed config; fail fast.
- Connect to forms with `@hookform/resolvers/zod` and to OpenAPI with `zod-to-openapi`; keep ORM types (Drizzle) aligned using `drizzle-zod`.
- Never trust client validation; the server always re-validates with the same schema.
- Avoid `any` and unsafe casts; use `unknown` and narrow with schemas.
