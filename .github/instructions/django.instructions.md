---
description: "Use when creating or modifying Django models, views, URLs, forms, serializers, admin, settings, migrations, or templates. Covers app structure, ORM, security, and migrations."
applyTo: ["**/{models,views,urls,forms,admin,serializers,signals,apps,settings}.py", "**/{models,views,serializers,settings,migrations}/**/*.py", "**/templates/**/*.html"]
---

# Django Guidelines

- Follow the project's existing Django version and app layout. Keep each app focused on one domain, with its own models, views, urls, and tests.
- Keep views thin: put business logic in models, managers, or service modules. Prefer class-based views or DRF viewsets when the project already uses them.
- Use the ORM and avoid raw SQL; when raw SQL is needed, always use parameterized queries.
- Prevent N+1 queries with `select_related` and `prefetch_related`, and use `only`/`values` for large reads.
- Create a migration for every model change with `makemigrations`. Never edit applied migrations, and keep schema and data migrations separate.
- Use `settings` and environment variables for configuration. Never hard-code `SECRET_KEY`, credentials, or `DEBUG=True` for production.
- Keep CSRF protection enabled, validate input through forms or serializers, and rely on template auto-escaping instead of `|safe`.
- Enforce permissions and authentication explicitly on every view or endpoint.
- Use `reverse`/`{% url %}` instead of hard-coded paths, and `get_object_or_404` for single-object lookups.
- Use `transaction.atomic` for multi-step writes.
- Add tests with Django's test framework or the project's existing test runner for new behavior.
- Make focused changes that preserve existing models, URLs, and API responses.
