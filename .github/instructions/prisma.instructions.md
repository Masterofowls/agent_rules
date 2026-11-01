---
description: "Use when editing Prisma schemas, Prisma Client queries, migrations, seeds, or prisma.config files."
applyTo: ["**/*.prisma", "**/prisma.config.{js,ts,mjs}", "**/prisma/**", "**/*prisma*.{js,ts}", "**/*Prisma*.ts"]
---

# Prisma ORM

- Follow the installed Prisma version, configured generator, client output path, database driver, and adapter. Do not copy setup from a different major version or introduce another ORM.
- Define nullability, defaults, unique constraints, foreign keys, and indexes explicitly. Keep existing database mappings with `@map` and `@@map`.
- Use generated Prisma types; define request and response schemas separately so private columns and server-owned fields are not exposed.
- Reuse the project's Prisma Client and connection pool. Avoid creating a client per request; follow the existing development hot-reload and serverless strategy.
- Select only required fields, bound list sizes, and use stable ordering for pagination. Measure queries before adding eager relations or indexes.
- Avoid N+1 queries; use supported relation loading or bounded batch queries as appropriate for the installed version.
- Use `$transaction` for atomic writes and its transaction client throughout the operation. Keep external network calls outside transactions.
- Parameterize raw queries with tagged templates or supported parameter APIs. Never interpolate untrusted strings into SQL or use unsafe raw-query methods for user input.
- Map known constraint and not-found errors to safe application errors; retain diagnostic details only in server logs.
- Generate and review migrations in development; apply reviewed migrations with the project's deployment command. Never edit already-applied migrations.
- Never run reset, force-reset, destructive schema push, or production migrations without explicit authorization for the target database. Preserve data with staged, backward-compatible migrations.
- Keep seeds explicit, repeatable, and environment-scoped. Never seed or clear production data as a side effect of tests.
- Validate migration and query behavior against the same database dialect used in production.
