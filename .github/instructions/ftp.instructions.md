---
description: "Use when working with remote files over FTP, FTPS, or SFTP, or uploading updates to static hosting; covers secure connections, scoped transfers, verification, and rollback."
applyTo: ["**/{deploy,deployment,scripts}/**", "**/*{ftp,sftp}*.{json,yml,yaml,toml,js,ts,py,ps1,sh}"]
---

# FTP, FTPS, and SFTP

- Confirm the authorized host, account, protocol, environment, and exact remote document root before connecting or transferring. Uploading to live hosting is deployment and requires explicit permission.
- Prefer SFTP over SSH or FTPS with certificate validation. FTP sends credentials and data unencrypted; do not silently fall back to it. Report the limitation and seek a secure alternative.
- SFTP and FTPS are different protocols; verify the host's supported protocol and port instead of guessing.
- Verify SSH host keys for SFTP or TLS certificates for FTPS. Never disable verification to bypass a connection error.
- Keep credentials in an approved credential store or private configuration. Never put passwords in URLs, command arguments, logs, tracked files, or transfer manifests.
- Inspect remote listings and resolved paths first. Treat remote path syntax as server-specific; prevent traversal, symlink escapes, and writes outside the approved root.
- Build and validate locally, then upload only intended release artifacts. Exclude source secrets, agent state, dependencies, and scratch files; review a transfer manifest or dry run before changing remote files.
- Preserve existing uploads, provider files, hidden configuration, and unrelated remote content. Never use destructive mirroring, delete-first deployment, or broad recursive removal.
- Replacing or deleting remote files requires authorization for the affected scope. Keep a recoverable copy of replaced files; do not download unrelated private data.
- Prefer staged uploads and atomic rename or release switching where supported. Otherwise plan asset ordering to avoid mixed releases; do not overwrite a live file during an incomplete transfer.
- Bound transfer concurrency and retries; surface failures and distinguish partial uploads from success. Verify sizes or checksums where supported, not timestamps alone.
- Verify the deployed URL, assets, deep links, and cache behavior after upload. Retain an approved rollback path and clean up only task-created staging files within the authorized scope.
