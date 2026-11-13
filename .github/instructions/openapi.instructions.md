---
description: "Use when authoring, generating, validating, or reviewing OpenAPI/Swagger contracts, API documentation, SDK generation, or contract compatibility."
applyTo: ["**/*openapi*.{json,yaml,yml}", "**/*swagger*.{json,yaml,yml}", "**/{openapi,swagger}/**"]
---

# OpenAPI contracts

- Inspect the project's OpenAPI version and generator first. Preserve its single source of truth and tooling; do not upgrade the contract format or introduce another generator during an unrelated API change.
- Distinguish OpenAPI 3.0 schemas from 3.1+ JSON Schema semantics, especially nullability, references, and schema dialects. Use only features supported by the installed validator and client generators.
- Give operations stable, unique `operationId` values. Document path/query/header parameters, required fields, media types, request bodies, success/error responses, pagination, limits, and relevant response headers.
- Define path parameters as required and keep names consistent with the URL template. Distinguish missing, null, empty, and default values; `default` documents a value rather than proving server behavior.
- Document authentication through reusable security schemes and explicit operation requirements. An empty operation security requirement disables inherited authentication; alternatives in a security array are OR, schemes in one object are AND.
- Describe permission checks, rate limits, idempotency keys, and retry behavior in addition to authentication. A documented scheme is not proof that the server enforces it.
- Reuse component schemas without erasing meaningful request/response differences. Keep read-only/server-owned fields out of writable payloads; define discriminators and error shapes consistently.
- Use examples that pass schema validation and contain no real credentials, personal data, or private endpoints. Keep public documentation separate from internal operations.
- Resolve local `$ref` paths relative to the containing document. Do not fetch remote references or execute generators/plugins from untrusted specifications without source approval.
- Run the project's existing lint/validation, reference resolution, and generated-contract drift checks. Validate example payloads and test actual request/response behavior; syntax validation alone is insufficient.
- Review contract diffs for removed operations, renamed IDs, new required fields, narrowed enums/types, changed auth, and changed statuses. Treat these as potential breaking changes for clients.
- Generate SDKs only when requested or already part of the workflow; preserve generated-file boundaries and validate consumers with the existing checks. Document required usage briefly in existing API docs.
