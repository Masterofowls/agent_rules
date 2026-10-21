---
description: "Use when creating or modifying SQL queries, schemas, migrations, indexes, or database scripts. Covers readability, safety, performance, and schema design."
applyTo: "**/*.sql"
---

# SQL Guidelines

- Follow the project's existing SQL dialect, naming, and formatting. Use uppercase keywords and `snake_case` identifiers.
- Select explicit columns instead of `SELECT *`, and use explicit `JOIN ... ON` syntax with clear table aliases.
- Always use parameterized queries in application code; never build SQL by concatenating user input.
- Filter early with `WHERE`, avoid functions on indexed columns in predicates, and check plans with `EXPLAIN` for slow queries.
- Add indexes for frequent filters, joins, and sort columns, and avoid redundant indexes.
- Design schemas with primary keys, foreign keys, `NOT NULL`, `UNIQUE`, and `CHECK` constraints, and use appropriate data types.
- Write migrations that are reversible and safe for existing data; do not edit applied migrations, and avoid destructive changes without a backup or confirmation.
- Wrap multi-statement changes in transactions, and require a `WHERE` clause on `UPDATE` and `DELETE` statements.
- Use CTEs for readability and avoid deeply nested subqueries.
- Never store secrets or plaintext passwords, and grant least-privilege database access.
- Keep comments brief and only where logic is non-obvious.
