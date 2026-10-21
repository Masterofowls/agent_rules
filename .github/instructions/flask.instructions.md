---
description: "Use when creating or modifying Flask apps, blueprints, routes, extensions, or templates. Covers app factory, structure, validation, errors, and security."
applyTo: ["**/{app,wsgi,extensions}.py", "**/{routes,views,blueprints}/**/*.py"]
---

# Flask Guidelines

- Follow the project's existing structure. For new apps, use an application factory (`create_app`) and register features as blueprints.
- Keep route functions thin; put business logic in service modules and database access in models or repositories.
- Initialize extensions (database, migrations, login, etc.) in a separate module and bind them in the factory, avoiding circular imports.
- Load configuration from config classes and environment variables; never hard-code `SECRET_KEY` or credentials, and never run with `debug=True` in production.
- Validate and sanitize all request input (`request.json`, `request.args`, forms) with the validation approach already used in the project.
- Use `url_for` instead of hard-coded paths, and rely on Jinja2 auto-escaping instead of `|safe`.
- Register centralized error handlers with `@app.errorhandler` and return consistent responses and status codes without leaking internals.
- Enable CSRF protection for forms, use secure session cookie settings, and enforce authentication and authorization on protected routes.
- Use `async` views only when the project supports them; otherwise keep views synchronous and avoid blocking work in requests.
- Use `logging` (`app.logger`) for debugging instead of `print`.
- Add tests with the Flask test client and `pytest` following the project's existing setup.
- Make focused changes that preserve existing routes, endpoints, and response shapes.
