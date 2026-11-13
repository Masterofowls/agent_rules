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
- Keep migrations backward-compatible where possible and document recovery when reversal is not safe. Do not edit applied migrations; destructive changes require explicit target approval, a verified backup, and reviewed data effects.
- Use transactions where the dialect and operations support them; do not assume DDL is transactional. Scope `UPDATE` and `DELETE` with meaningful predicates and expected affected-row checks; a tautological `WHERE` is not a safety guard. Full-table operations require explicit approval.
- Use CTEs for readability and avoid deeply nested subqueries.
- Never store secrets or plaintext passwords, and grant least-privilege database access.
- Keep comments brief and only where logic is non-obvious.

## Data correctness and concurrency
- Model money and exact quantities with appropriate decimal/numeric types, not binary floating point. Define precision, units, timezone policy, and rounding at system boundaries.
- Handle `NULL` explicitly with `IS NULL`/`IS NOT NULL`; consider three-valued logic in `NOT IN`, joins, and aggregates. Verify duplicate rows and fan-out when joining one-to-many relationships.
- Use deterministic ordering with a unique tie-breaker for pagination. Apply ownership/tenant predicates to reads and writes, not just frontend filters.
- Choose isolation and locking for the invariant being protected. Keep transactions short, use a consistent lock order, and make bounded deadlock/serialization retries safe through idempotency.
- Review uniqueness, foreign-key behavior, cascading deletes, and upsert conflict targets. Check affected-row counts before committing destructive or bulk changes.

## Plans and migrations
- Measure query plans and realistic row counts before indexing. `EXPLAIN ANALYZE` executes the statement; never run it on mutating SQL or expensive production queries without authorization and a safe execution plan.
- Check index selectivity, write overhead, lock duration, temporary space, and deployment compatibility. Online/concurrent index features are dialect-specific and may not run inside a transaction.
- Prefer expand/backfill/contract migrations for deployed systems. Batch resumable backfills with bounded transactions; validate counts and constraints before removing old columns.
- Test against the real database dialect and representative data in an isolated environment, including empty sets, duplicates, nulls, concurrency, and rollback/recovery. Do not silently switch engines to make tests pass.
