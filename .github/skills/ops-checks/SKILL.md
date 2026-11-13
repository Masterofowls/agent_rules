---
name: ops-checks
description: "Reuse bundled scripts to check URLs, DNS resolution, TLS certificate expiry, disk space, Git worktree state or secret leaks, Supabase/PostgreSQL, SSH, FTPS, runtimes, Docker, OS, or preview Ubuntu VPS setup. Load for operational checks instead of writing replacement scripts."
---

# Reusable operational checks

- Read this file and the bundled scripts before using them. Reuse the implementation, not a remembered copy; locate this skill in the current catalog, never assume another machine's absolute path.
- Requires Python 3.10+; checks additionally require the named system tools. Nothing installs tools automatically.
- Use `python scripts/run.py TASK OPTIONS` as the OS-aware launcher, or the matching `scripts/TASK.ps1` / `scripts/TASK.sh` entry point. PowerShell uses `python`; Unix uses `python3`.
- Exit codes: 0 success, 1 check failed, 2 invalid input/permission/missing tool. Output is JSON; error diagnostics go to stderr without raw remote output or credentials.

| Task | Options and purpose |
| --- | --- |
| `detect-os` | Detect Windows, Linux, macOS, WSL environment, architecture, and Python version |
| `check-tools` | `--tools node python git` (default: node, python, npm, git); reports installed versions, fails if any requested tool is missing |
| `check-url` | `--url https://HOST/PATH --authorized`; HEAD, bounded GET fallback for 405/501, accepts 2xx only, no redirects |
| `check-postgres` | `--service SERVICE --authorized`; `psql` read-only SELECT 1 with TLS hostname verification |
| `check-supabase` | Same as PostgreSQL; use a Supabase direct/pooler service configured for the correct host, user, port, and database |
| `check-ssh` | `--host HOST --user USER --port 22 --authorized`; OpenSSH batch authentication and remote `true` only |
| `check-ftp` | `--url ftps://HOST/PATH/ --netrc-file PRIVATE_FILE --authorized`; curl encrypted directory listing, no uploads |
| `check-git-leaks` | `--repo PATH --scope all` (or `history`, `files`); Gitleaks v8 `git` and/or `dir`, redacted output, no report file |
| `check-docker` | Docker client version and daemon availability |
| `check-dns` | `--host HOST --authorized`; system-resolver A/AAAA connectivity, returns deduplicated address counts |
| `check-tls` | `--host HOST --port 443 --min-days 14 --authorized`; trusted TLS chain/hostname and certificate-expiry threshold |
| `check-disk` | `--path PATH --min-free-gib 1 --min-free-percent 10`; both local free-space thresholds must pass; no cleanup |
| `check-git-state` | `--repo PATH [--require-clean]`; branch/detached state and staged, unstaged, untracked, conflict counts; no filenames, fetch, or Git mutations |
| `setup-ubuntu` | Preview only by default; `--apply --authorized` runs a minimal package setup as root on Ubuntu |

All tasks accept `--timeout SECONDS` (1-600, default 15 per subprocess/request). Use a suitable package-install timeout, such as 600, for approved Ubuntu setup.

## Credentials and authorization
- Remote checks require explicit user authorization for the exact target before passing `--authorized`; the flag is an acknowledgement, not a substitute for permission.
- PostgreSQL uses a private libpq service file (`PGSERVICEFILE`) and password file (`PGPASSFILE`), with a trusted root certificate configured for `verify-full`. Never pass a database URL or password in arguments. Supabase pooler connectivity does not verify RLS or application permissions.
- SSH requires a previously verified entry in known_hosts and a loaded key or existing SSH configuration. The check does not disable host-key verification or ask for passwords.
- FTPS uses curl's private netrc file; restrict its permissions. Both `ftp://` with required explicit TLS and `ftps://` are supported, but unencrypted FTP is not. The directory listing is discarded.
- URL checks access only the exact authorized URL, with no redirect following. These CLI tools are not a public SSRF-safe service; do not expose them to arbitrary web input.
- DNS and TLS probes run in an isolated child process, so the overall timeout includes name resolution. They use the system resolver and trusted certificate store; no `insecure` bypass or certificate output. DNS does not validate authoritative records, DNSSEC, MX/TXT, or propagation. TLS checks direct TLS, not STARTTLS, and does not prove revocation status or certificate renewal works.
- Disk thresholds are GiB (1024^3 bytes) and percentage of total capacity; equality passes. Git state is a snapshot, not a branch-synchronization or secret scan. Dirty state is reported normally unless `--require-clean` is requested; no remote tracking information is refreshed.
- Git leak results are suppressed to avoid leaking findings into chat. A clean scan is not proof that no secret ever existed; inspect findings separately using approved, redacted local tooling. The check does not rewrite history.
- Ubuntu setup installs only `ca-certificates`, `curl`, and `git`; it does not provision users, firewall, SSH, Docker, databases, or an application. Run on the intended VPS after inspection, with explicit approval. It never downloads and executes a setup script or elevates itself.

## Validation
Run from this skill directory:
```text
python -m unittest discover -s tests -v
ruff check --target-version py310 scripts tests
ruff format --target-version py310 scripts tests
ruff format --target-version py310 --check scripts tests
coverage run --branch --source=scripts -m unittest discover -s tests
coverage report --fail-under=80
```
Use the project's existing environment/runner if available. Remote checks require tools, credentials, and authorized services; mocked tests do not certify live connectivity. Do not create extra guides or copy this bundle into unrelated projects unless requested.
