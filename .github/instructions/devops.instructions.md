---
description: "Use when managing DevOps, infrastructure as code, CI/CD release controls, Kubernetes/Helm, monitoring, backups, operational recovery, or incident response."
applyTo: ["**/*.{tf,tfvars,hcl}", "**/{infra,infrastructure,terraform,k8s,kubernetes,helm,monitoring}/**", "**/ansible.cfg", "**/playbooks/*.{yaml,yml}"]
---

# DevOps operations

- Confirm the account, environment, region, cluster/context, workspace, and current state before running tools. Read-only inspection is not permission to provision, restart, scale, destroy, change traffic, or deploy.
- Reuse existing infrastructure and configuration management. Do not introduce Terraform, Kubernetes, Helm, or another platform solely to satisfy these rules.
- Plan and review infrastructure changes before apply: resource replacements/deletions, dependencies, cost, permissions, quotas, network exposure, and rollback/recovery. A dry-run or successful plan is not proof of a safe rollout.
- Keep IaC state and secrets in approved encrypted backends with locking and least-privilege access. Do not commit private state, credentials, sensitive tfvars, or plan files; preserve safe templates.
- Do not use targeted applies, force-unlock state, import resources, or reconcile drift without explicit scope and coordination. Protect shared state from concurrent operators.
- Prefer short-lived identity/OIDC over long-lived CI keys. Grant minimal job permissions, restrict production environments, and keep untrusted pull-request code away from privileged runners and secrets.
- Pin deployment tooling and supply-chain inputs deliberately. Build immutable artifacts with provenance where supported; scan them through approved local/CI tooling without sending private images or source to external services.
- Separate startup, liveness, and readiness checks. Avoid dependency outages causing restart storms; configure graceful termination, connection draining, resource limits, and bounded retries for the selected platform.
- Measure service error rate, latency, traffic, and saturation with useful alerts tied to the project's agreed objectives. Redact logs and metrics labels; avoid personal identifiers and high-cardinality payloads.
- Back up persistent data under an agreed retention/encryption policy and test restoration in isolation. Replication and snapshots alone do not establish recovery; define achievable RPO/RTO.
- During incidents, establish scope and evidence before changes. Keep diagnostics bounded, avoid destructive probes, coordinate operators, and obtain approval for production remediation or rollback.
- Keep brief recovery and operating notes in existing runbooks/docs when operations are in scope. Report verified state and unresolved risks; never claim a service is healthy from an upload, plan, or single liveness response.
