---
description: "Use when configuring deployment to Vercel, Netlify, Cloudflare Pages, Fly.io, Render, GitHub Pages, GitLab Pages, DigitalOcean, or a custom VPS; covers builds, routing, secrets, runtimes, verification, and rollback."
applyTo: ["**/vercel.json", "**/netlify.toml", "**/wrangler.{toml,json,jsonc}", "**/fly.toml", "**/render.yaml", "**/.gitlab-ci.yml", "**/.github/workflows/*.{yml,yaml}", "**/.do/*.{yml,yaml}", "**/{deploy,deployment,infra,infrastructure}/**", "**/Dockerfile*", "**/Caddyfile", "**/*nginx*.conf"]
---

# Deployment

## Shared requirements
- Inspect the framework, runtime, lockfile, monorepo root, build command, output directory, and existing provider configuration before changing deployment.
- Follow the provider's current official documentation and installed CLI version; verify support for the exact framework and runtime. Do not assume all hosts support SSR, WebSockets, workers, or persistent storage.
- Prefer existing configuration and infrastructure. Add only the target provider's required files, not scaffolding for every platform.
- Creating deployment instructions or configuration is not permission to publish. Obtain explicit authorization for the target account, project, and environment before deploying or changing live infrastructure.
- Follow agent permissions: deployment authorization does not imply permission to commit, push, create or switch branches, merge, delete resources, or rewrite files.
- Require approval before creating billable resources or changing production DNS, databases, secrets, or traffic. Do not trigger existing automatic deployments accidentally.
- Use reproducible installs and production builds. Run applicable lint, format-check, type-check, tests, coverage, and build checks before release.
- Separate preview, staging, and production variables and databases. Store credentials in provider secret stores or protected CI variables, never repository files, image layers, build logs, or public browser variables.
- Distinguish build-time from runtime configuration. Static frontend environment values are bundled and public; changing them usually requires rebuilding.
- Configure base paths, asset URLs, SPA fallback, and API routing deliberately. Never rewrite missing assets or API errors to the SPA HTML page.
- Keep API endpoints, CORS, cookies, OAuth callback URLs, HTTPS, and security headers aligned with the deployed domain.
- Use least-privilege deployment credentials; prefer short-lived workload identity where supported. Inspect build scripts and dependencies before giving them access to secrets.
- Apply reviewed database migrations only with authorization for the target database; use backups and backward-compatible changes. Application rollback does not automatically reverse a migration.

## Vercel
- Use the framework preset and detected output settings unless the project requires an override. Set the correct monorepo root and supported Node/runtime version.
- Separate preview and production environment variables. Use a preview deployment for validation; production promotion or deployment requires authorization.
- Keep server functions within supported execution, size, and connection limits. Use compatible database drivers and pooling; local filesystem writes are not durable application storage.
- Preserve Next.js framework integration instead of replacing it with generic SPA rewrites. Check caching, route handlers, redirects, and image optimization in the deployed environment.

## Netlify
- Configure the base directory, build command, and publish directory in the existing setup or `netlify.toml`.
- For a static SPA, add a fallback after specific redirects and API/function routes. Do not apply SPA fallback blindly to framework-rendered applications.
- Use the supported framework adapter for SSR and the appropriate Functions or Edge Functions runtime.
- Scope environment variables to deploy contexts where supported. Test deploy previews, forms, redirects, headers, and function endpoints before production.

## Cloudflare Pages
- Confirm whether the application is a static Pages site or needs a supported server adapter; verify whether current framework guidance calls for Workers instead.
- Set the build output directory and compatibility settings supported by the selected adapter and runtime.
- Use Pages Functions and bindings only where supported; do not assume a full Node.js server or unrestricted Node APIs are available.
- Configure preview and production bindings and secrets separately. Use appropriate managed storage rather than local filesystem persistence.
- Verify asset handling, fallback behavior, caching, and function routes. Protect account tokens and do not include secret binding values in Wrangler configuration.

## Fly.io
- Use the existing Dockerfile and `fly.toml`; align service ports, health checks, regions, and process groups with the application.
- Bind the application to `0.0.0.0` on the configured internal port. Configure secrets through the provider, not committed environment values.
- Treat local disk as disposable unless an appropriate volume is configured. Volumes are region/machine-specific; do not assume shared storage or automatic replication.
- Plan resource sizing, autoscaling, graceful shutdown, and database connectivity. Verify machine health and logs after release.

## Render
- Choose the correct service type: static site, web service, private service, background worker, or scheduled job.
- Configure build/start commands and health checks in the existing dashboard settings or `render.yaml`, with secrets referenced rather than embedded.
- Web services must bind to `0.0.0.0` and the platform-provided port. Static sites need the correct publish directory and routing rules.
- Use explicitly configured persistent storage or external services for durable data. Verify plan-specific runtime, scaling, and availability limits before promising behavior.

## GitHub Pages
- Deploy static output only; GitHub Pages does not run a Node/Python backend or Next.js SSR. Verify static-export compatibility before choosing it.
- Set asset and router base paths for the actual URL, including a repository subpath when applicable.
- Do not assume server rewrites exist for client-side routes. Choose supported static route generation, hash routing, or a reviewed fallback and test direct deep links.
- Use the supported Pages Actions deployment flow with least-privilege permissions and the configured deployment environment. Do not create or push a deployment branch without authorization.
- Never put secrets into the static artifact; hosted JavaScript and configuration are public.

## GitLab Pages
- Build static output and publish it through the Pages CI syntax supported by the GitLab instance; do not copy version-specific YAML without checking compatibility.
- Configure the publish directory, artifacts, rules, and environment URL correctly. Account for project subpaths or unique-domain behavior.
- Use protected/masked CI variables where appropriate, but never bundle secrets into static output.
- Verify direct routes and asset paths; do not assume backend execution or arbitrary server rewrite support.

## DigitalOcean
- Distinguish App Platform managed deployment from a Droplet/VPS. Configure the selected service's build, runtime, health checks, and environment explicitly.
- For App Platform, use the supported app specification and appropriate static-site, service, or worker component.
- For Droplets, follow the VPS requirements below. Protect private networking, firewall rules, SSH access, and managed database credentials.
- Obtain approval for resource size, region, storage, backups, and recurring costs before provisioning.

## Custom VPS
- Use a supported, maintained OS, SSH keys, a non-root deployment user, least privilege, and a firewall exposing only required ports. Never lock out existing administrative access.
- Put the application behind an HTTPS reverse proxy such as Caddy or Nginx. Keep internal application and database ports private.
- Use systemd or the project's container/process supervisor for restart policies, graceful shutdown, and logs; do not rely on an interactive terminal session.
- Store secrets outside the repository with restrictive permissions. Configure production runtime, bind address, ports, log rotation, monitoring, and disk-space alerts.
- Use versioned releases or immutable images and a reversible traffic switch. Never delete the project directory to deploy a fresh version.
- Back up persistent data and verify restoration. Keep database migrations separate from replacing application files.
- Apply security updates and test certificate renewal, service restart, and recovery after reboot.

## Verification and rollback
- Verify the actual deployed URL, not only the local build: HTTPS, main page, deep links, assets, API health, authentication, and critical flows.
- Inspect deployment logs and browser/network errors; verify readiness rather than treating a successful upload as a successful release.
- Record the provider, environment, deployment identifier, URL, and checks performed without exposing credentials.
- Keep a known-good release and a documented rollback path. Do not delete old releases or provider projects without explicit approval.
- Report failed checks and remaining limitations. Never claim a deployment occurred when only configuration was added.
