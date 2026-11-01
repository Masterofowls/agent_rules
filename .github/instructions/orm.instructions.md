---
description: "Use when working with an ORM or database persistence, including TypeORM, Sequelize, SQLAlchemy, Django ORM, Prisma, and Drizzle."
applyTo: ["**/{db,database,models,entities,repositories,migrations}/**/*.{js,ts,py,sql}", "**/*.{entity,repository}.ts"]
---

# ORM and persistence

- Reuse the existing ORM and supported database dialect. Do not add a second ORM or abstraction layer without a concrete requirement.
- Keep query types and runtime validation distinct. Database constraints remain necessary even when inputs pass application validation.
- Use parameterized queries; whitelist dynamic column names and ordering. Never pass request objects directly to create or update methods.
- Enforce tenant and ownership restrictions in reads and writes, not only in UI or controllers.
- Bound list queries, select needed fields, use deterministic pagination, and inspect query plans for measured bottlenecks.
- Prevent N+1 queries with deliberate relation loading or batching. Avoid eager-loading every relation by default.
- Keep atomic work in one transaction and one transaction client/session. Use appropriate isolation or optimistic concurrency for conflicting updates.
- Reuse connection pools; configure timeouts and limits for the deployment. Close request-scoped sessions and roll back failed transactions.
- TypeORM: use the configured DataSource and repositories; disable automatic schema synchronization in production and use reviewed migrations.
- Sequelize: pass the same transaction to related writes and use migrations instead of production `sync({ force: true })` or `sync({ alter: true })`.
- SQLAlchemy: use scoped Session or AsyncSession lifecycles, explicit rollback on failure, and Alembic migrations; never share one session across concurrent requests.
- Django ORM: use `select_related`, `prefetch_related`, and `transaction.atomic` where appropriate; retain Django migration conventions.
- Drizzle and Prisma projects also follow their dedicated instruction files.
- Treat drops, truncation, schema resets, bulk deletion, and production migration execution as operations requiring explicit authorization. Inspect the exact environment first.
- Test constraints, transactions, and migrations using the production database dialect; mocks alone do not verify persistence behavior.
