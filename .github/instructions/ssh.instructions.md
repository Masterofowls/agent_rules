---
description: "Use when connecting over SSH to a remote VPS, running remote commands, transferring files with SCP or SFTP, or managing remote services."
applyTo: ["**/{deploy,deployment,infra,infrastructure,scripts}/**", "**/*ssh*.{json,yml,yaml,toml,ps1,sh}", "**/ssh_config"]
---

# SSH and remote VPS work

- Confirm the authorized host, user, environment, and intended operations. Permission to connect or inspect is not permission to deploy, restart services, change infrastructure, or delete files.
- Prefer SSH keys and a least-privilege account. Store private keys outside the repository with restrictive permissions; never reveal key material or put passwords in commands or logs.
- Verify the server host-key fingerprint through a trusted source. Stop on unexpected key changes; never disable strict host-key checking or clear known-host entries to bypass warnings.
- Use the existing SSH configuration where suitable. Do not modify global SSH settings, enable agent forwarding, or open tunnels without an explicit need and authorization.
- Begin with scoped read-only checks of host identity, working directory, target files, service state, and available resources. Inspect files before editing; preserve unrelated remote work.
- Quote commands and paths for the remote shell, not just the local shell. Never interpolate untrusted values into shell commands; use explicit paths and arguments.
- Use non-interactive execution for automation with bounded connection/command timeouts and checked exit statuses. Never report success on partial output or a failed command.
- Use elevated privileges only for approved operations. Never change firewall, SSH access, ownership, permissions, or user accounts broadly as a troubleshooting shortcut.
- Keep recoverable backups or versioned releases for approved edits. Do not replace a whole configuration when a targeted patch suffices, or delete project directories to redeploy.
- Use the configured service manager for persistent processes; do not rely on the SSH session or leave temporary debugging services running.
- For approved service changes, validate configuration before reload and verify health afterward. Maintain a rollback path that preserves administrative access.
- Keep logs scoped and redacted, close sessions and temporary tunnels after use, and report the actual remote checks performed.
