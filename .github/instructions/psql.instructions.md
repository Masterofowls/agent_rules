---
description: "Use when creating or modifying PostgreSQL scripts, psql commands, PL/pgSQL functions, or Postgres-specific SQL. Covers psql usage, Postgres types, transactions, and safe operations."
applyTo: ["**/*.psql", "**/*.pgsql"]
---

# PostgreSQL and psql Guidelines

- Follow the SQL guidelines, and use PostgreSQL-specific features only when the project targets Postgres.
- Connect with `psql` using a connection URI or `PG*` environment variables and `~/.pgpass`/`pgpass.conf`; never put passwords in scripts or command lines.
- Run scripts with `psql -v ON_ERROR_STOP=1 -f file.sql` so failures stop execution, and use `--single-transaction` for all-or-nothing changes.
- Use PostgreSQL types appropriately: `timestamptz` for timestamps, `uuid`, `jsonb`, `numeric` for money, `text` instead of arbitrary `varchar` limits, and `generated always as identity` over `serial`.
- Create indexes on large tables with `CREATE INDEX CONCURRENTLY`, and choose index types (`btree`, `gin`, `gist`) to match the query.
- Use `EXPLAIN (ANALYZE, BUFFERS)` to inspect slow queries, but do not run `ANALYZE` on destructive statements outside a transaction.
- Use `psql` meta-commands (`\d`, `\dt`, `\df`, `\x`) only in interactive helpers, not in portable SQL files.
- Wrap destructive operations in a transaction, review affected rows before `COMMIT`, and always include a `WHERE` clause on `UPDATE` and `DELETE`.
- Write PL/pgSQL functions with explicit argument types, `SECURITY INVOKER` by default, and a fixed `search_path` for `SECURITY DEFINER`.
- Grant least-privilege roles and avoid running application workloads as a superuser.
