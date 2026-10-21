---
description: "Use when creating or modifying Drizzle ORM schemas, queries, migrations, or drizzle.config files. Covers schema definition, typed queries, migrations, and safety."
applyTo: ["**/drizzle.config.{js,mjs,ts}", "**/{db,database,drizzle}/**/*.{js,ts}", "**/schema.{js,ts}"]
---

# Drizzle ORM Guidelines

- Follow the project's existing database dialect and Drizzle version (`pg-core`, `mysql-core`, or `sqlite-core`) and keep imports consistent with it.
- Define tables in schema files with explicit column types, `notNull`, `default`, `unique`, indexes, and foreign key `references`; export inferred types with `$inferSelect` and `$inferInsert`.
- Define relations with `relations()` and use the relational query API (`db.query`) for nested reads and the SQL-like builder for complex queries.
- Use the query builder and `sql` template with placeholders; never concatenate user input into raw SQL.
- Select only needed columns, add indexes for frequent filters and joins, and use `limit` and pagination for large reads.
- Use `db.transaction` for multi-step writes, and always include a `where` condition on `update` and `delete`.
- Generate migrations with `drizzle-kit generate` and apply them with `drizzle-kit migrate`. Do not edit applied migrations, and use `push` only for local development.
- Create the database client in one module and reuse it; read the connection string from environment variables and never hard-code it.
- Use async/await for all queries and handle database errors explicitly.
- Make focused changes: preserve existing table and column names, and treat renames and drops as migrations that need data safety.
