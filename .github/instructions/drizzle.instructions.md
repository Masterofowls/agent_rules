---
description: "Use when creating or modifying Drizzle ORM schemas, queries, migrations, or drizzle.config files. Covers schema definition, typed queries, migrations, and safety."
applyTo: ["**/drizzle.config.{js,mjs,ts}", "**/{db,database,drizzle}/**/*.{js,ts}", "**/schema.{js,ts}"]
---

# Drizzle ORM Guidelines

- Follow the project's existing database dialect and Drizzle version (`pg-core`, `mysql-core`, or `sqlite-core`) and keep imports consistent with it.
- Define tables in schema files with explicit column types, `notNull`, `default`, `unique`, indexes, and foreign key `references`; export inferred types with `$inferSelect` and `$inferInsert`.
- Define relations and nested reads with the APIs supported by the installed Drizzle version; use the SQL-like builder for complex queries. ORM relations do not replace database foreign key constraints.
- Use the query builder and `sql` template with placeholders; never concatenate user input into raw SQL.
- Select only needed columns, add indexes for frequent filters and joins, and use `limit` and pagination for large reads.
- Use `db.transaction` for multi-step writes, and always include a `where` condition on `update` and `delete`.
- Generate migrations with `drizzle-kit generate` and apply them with `drizzle-kit migrate`. Do not edit applied migrations, and use `push` only for local development.
- Create the database client in one module and reuse it; read the connection string from environment variables and never hard-code it.
- Use async/await for all queries and handle database errors explicitly.
- Make focused changes: preserve existing table and column names, and treat renames and drops as migrations that need data safety.

## Query and migration safety
- Validate request data separately from table definitions; expose only allowed write fields and apply tenant or ownership predicates to every relevant operation.
- Propagate the transaction client through related writes. Keep network calls outside transactions and use the driver's supported transaction behavior.
- Parameterize values and whitelist dynamic identifiers or sort fields; a raw SQL fragment is not safe merely because it is wrapped in `sql`.
- Use stable ordering with pagination and inspect query plans before adding indexes or changing relation loading.
- Reuse the configured driver, pool, schema exports, and runtime. Do not assume every driver supports the same transaction or relational features.
- Review generated SQL for destructive changes; test migrations against the production dialect. Never apply production migrations, reset data, or force schema synchronization without explicit authorization.
- Do not introduce schema-to-validator packages unless needed; use the installed version's supported integration and exclude server-owned or private fields.
