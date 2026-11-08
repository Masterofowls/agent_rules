"""Bounded operational checks with no credential-bearing diagnostic output."""

import argparse
import json
import os
import platform
import re
import shutil
import socket
import ssl
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


class CheckError(Exception):
    def __init__(self, message: str, code: int = 1) -> None:
        super().__init__(message)
        self.code = code


def execute(command: list[str], timeout: int, env: dict[str, str] | None = None) -> str:
    if not shutil.which(command[0]):
        raise CheckError(f"Required tool unavailable: {command[0]}", 2)
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            env=env,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise CheckError(f"{command[0]} timed out") from exc
    except OSError as exc:
        raise CheckError(f"Cannot start {command[0]}", 2) from exc
    if result.returncode:
        # Native errors can contain connection strings or private remote data.
        raise CheckError(f"{command[0]} failed (exit {result.returncode})")
    return result.stdout.strip()


def require_authorization(args: argparse.Namespace) -> None:
    if not args.authorized:
        raise CheckError("Explicit target authorization required (--authorized)", 2)


def target_url(value: str, schemes: tuple[str, ...]) -> None:
    try:
        parsed = urllib.parse.urlsplit(value)
        port = parsed.port
    except ValueError as exc:
        raise CheckError("Invalid URL", 2) from exc
    if (
        parsed.scheme not in schemes
        or not parsed.hostname
        or parsed.username is not None
        or parsed.password is not None
        or parsed.fragment
        or (port is not None and not 1 <= port <= 65535)
        or any(ord(char) < 33 for char in value)
    ):
        raise CheckError("URL requires a supported scheme and no credentials", 2)


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def check_url(args: argparse.Namespace) -> dict:
    require_authorization(args)
    target_url(args.url, ("http", "https"))
    opener = urllib.request.build_opener(NoRedirect)
    for method in ("HEAD", "GET"):
        request = urllib.request.Request(args.url, method=method)
        try:
            with opener.open(request, timeout=args.timeout) as response:
                status = response.status
        except urllib.error.HTTPError as exc:
            exc.close()
            if method == "HEAD" and exc.code in (405, 501):
                continue
            raise CheckError(f"HTTP check failed (status {exc.code})") from exc
        except urllib.error.URLError as exc:
            reason = exc.reason
            if isinstance(reason, ssl.SSLError):
                message = "TLS verification failed"
            elif isinstance(reason, socket.gaierror):
                message = "DNS lookup failed"
            elif isinstance(reason, TimeoutError):
                message = "HTTP request timed out"
            else:
                message = "HTTP connection failed"
            raise CheckError(message) from exc
        except (TimeoutError, OSError) as exc:
            raise CheckError("HTTP request failed or timed out") from exc
        if not 200 <= status < 300:
            raise CheckError(f"HTTP check failed (status {status})")
        return {"status": status, "method": method}
    raise CheckError("HTTP check failed")


def check_postgres(args: argparse.Namespace) -> dict:
    require_authorization(args)
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", args.service):
        raise CheckError("Use a libpq service name, not a connection string", 2)
    env = os.environ.copy()
    env.update(
        PGSERVICE=args.service,
        PGSSLMODE="verify-full",
        PGCONNECT_TIMEOUT=str(args.timeout),
        PGOPTIONS="-c default_transaction_read_only=on -c statement_timeout=5000",
    )
    output = execute(
        [
            "psql",
            "-X",
            "-w",
            "-At",
            "-v",
            "ON_ERROR_STOP=1",
            "-d",
            (
                f"service={args.service} sslmode=verify-full "
                f"connect_timeout={args.timeout} "
                "options='-c default_transaction_read_only=on -c statement_timeout=5000'"
            ),
            "-c",
            "SELECT 1",
        ],
        args.timeout,
        env,
    )
    if output != "1":
        raise CheckError("Database did not return the expected SELECT 1 result")
    return {"query": "SELECT 1", "tls": "verify-full", "read_only": True}


def check_ssh(args: argparse.Namespace) -> dict:
    require_authorization(args)
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.:-]*", args.host):
        raise CheckError("Invalid SSH host", 2)
    if not re.fullmatch(r"[A-Za-z0-9_][A-Za-z0-9_.-]*", args.user):
        raise CheckError("Invalid SSH user", 2)
    execute(
        [
            "ssh",
            "-T",
            "-o",
            "BatchMode=yes",
            "-o",
            "StrictHostKeyChecking=yes",
            "-o",
            f"ConnectTimeout={args.timeout}",
            "-o",
            "ConnectionAttempts=1",
            "-o",
            "ClearAllForwardings=yes",
            "-o",
            "ForwardAgent=no",
            "-p",
            str(args.port),
            "-l",
            args.user,
            args.host,
            "true",
        ],
        args.timeout,
    )
    return {"authenticated": True, "remote_command": "true"}


def check_ftp(args: argparse.Namespace) -> dict:
    require_authorization(args)
    target_url(args.url, ("ftp", "ftps"))
    credentials = Path(args.netrc_file).resolve()
    if not credentials.is_file():
        raise CheckError("Private netrc file not found", 2)
    if os.name != "nt" and credentials.stat().st_mode & 0o077:
        raise CheckError("Netrc file must not be accessible to group or others", 2)
    execute(
        [
            "curl",
            "--disable",
            "--silent",
            "--show-error",
            "--fail",
            "--globoff",
            "--ssl-reqd",
            "--proto",
            "=ftp,ftps",
            "--connect-timeout",
            str(args.timeout),
            "--max-time",
            str(args.timeout),
            "--netrc-file",
            str(credentials),
            "--list-only",
            args.url,
        ],
        args.timeout,
    )
    return {"encrypted_listing": True, "writes": False}


def check_git_leaks(args: argparse.Namespace) -> dict:
    repo = Path(args.repo).resolve()
    execute(["git", "-C", str(repo), "rev-parse", "--show-toplevel"], args.timeout)
    scopes = (
        ("git", "dir")
        if args.scope == "all"
        else ("git" if args.scope == "history" else "dir",)
    )
    for scope in scopes:
        execute(
            ["gitleaks", scope, str(repo), "--redact", "--no-banner"],
            args.timeout,
        )
    return {"scope": args.scope, "findings": False}


def check_tools(args: argparse.Namespace) -> dict:
    versions: dict[str, str | None] = {}
    for tool in args.tools:
        if tool not in ("node", "python", "python3", "npm", "git", "psql", "docker"):
            raise CheckError(f"Unsupported version probe: {tool}", 2)
        if tool == "python":
            versions[tool] = platform.python_version()
        elif shutil.which(tool):
            # npm.cmd needs explicit CMD execution on Windows.
            command = [tool, "--version"]
            if os.name == "nt" and tool == "npm":
                command = [
                    os.environ.get("COMSPEC", "cmd.exe"),
                    "/d",
                    "/c",
                    "npm --version",
                ]
            versions[tool] = execute(command, args.timeout)
        else:
            versions[tool] = None
    missing = [name for name, version in versions.items() if version is None]
    if missing:
        raise CheckError(f"Required tools missing: {', '.join(missing)}", 2)
    return {"versions": versions}


def setup_ubuntu(args: argparse.Namespace) -> dict:
    commands = [
        ["apt-get", "update"],
        [
            "apt-get",
            "install",
            "--yes",
            "--no-install-recommends",
            "ca-certificates",
            "curl",
            "git",
        ],
    ]
    if not args.apply:
        return {"preview": True, "commands": commands}
    require_authorization(args)
    if platform.system() != "Linux":
        raise CheckError("Setup requires an Ubuntu Linux host", 2)
    release = Path("/etc/os-release").read_text(encoding="utf-8")
    if not re.search(r'^ID=(?:"ubuntu"|ubuntu)$', release, re.MULTILINE):
        raise CheckError("Setup is supported only on Ubuntu", 2)
    if os.geteuid() != 0:
        raise CheckError("Approved setup must be run as root; no auto-elevation", 2)
    for command in commands:
        execute(command, args.timeout)
    return {"applied": True, "packages": ["ca-certificates", "curl", "git"]}


def detect_os() -> dict:
    system = platform.system()
    if system not in ("Windows", "Linux", "Darwin"):
        raise CheckError("Unsupported operating system", 2)
    return {
        "os": system,
        "architecture": platform.machine(),
        "wsl": system == "Linux" and "microsoft" in platform.release().lower(),
        "python": platform.python_version(),
    }


def bounded_integer(value: str) -> int:
    try:
        number = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Expected an integer") from exc
    if not 1 <= number <= 600:
        raise argparse.ArgumentTypeError("Timeout must be 1-600 seconds")
    return number


def ssh_port(value: str) -> int:
    try:
        number = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Expected a port number") from exc
    if not 1 <= number <= 65535:
        raise argparse.ArgumentTypeError("Port must be 1-65535")
    return number


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    tasks = root.add_subparsers(dest="task", required=True)
    for name in (
        "detect-os",
        "check-tools",
        "check-url",
        "check-postgres",
        "check-supabase",
        "check-ssh",
        "check-ftp",
        "check-git-leaks",
        "check-docker",
        "setup-ubuntu",
    ):
        task = tasks.add_parser(name)
        task.add_argument("--timeout", type=bounded_integer, default=15)
        task.add_argument("--authorized", action="store_true")
        if name == "check-url":
            task.add_argument("--url", required=True)
        elif name in ("check-postgres", "check-supabase"):
            task.add_argument("--service", required=True)
        elif name == "check-ssh":
            task.add_argument("--host", required=True)
            task.add_argument("--user", required=True)
            task.add_argument("--port", type=ssh_port, default=22)
        elif name == "check-ftp":
            task.add_argument("--url", required=True)
            task.add_argument("--netrc-file", required=True)
        elif name == "check-git-leaks":
            task.add_argument("--repo", default=".")
            task.add_argument(
                "--scope", choices=("all", "history", "files"), default="all"
            )
        elif name == "check-tools":
            task.add_argument(
                "--tools", nargs="+", default=["node", "python", "npm", "git"]
            )
        elif name == "setup-ubuntu":
            task.add_argument("--apply", action="store_true")
    return root


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        detect_os()
        handlers = {
            "check-tools": check_tools,
            "check-url": check_url,
            "check-postgres": check_postgres,
            "check-supabase": check_postgres,
            "check-ssh": check_ssh,
            "check-ftp": check_ftp,
            "check-git-leaks": check_git_leaks,
            "setup-ubuntu": setup_ubuntu,
        }
        if args.task == "detect-os":
            result = detect_os()
        elif args.task == "check-docker":
            version = execute(["docker", "--version"], args.timeout)
            execute(["docker", "info", "--format", "{{.ServerVersion}}"], args.timeout)
            result = {"client": version, "daemon": True}
        else:
            result = handlers[args.task](args)
    except CheckError as exc:
        print(
            json.dumps({"ok": False, "task": args.task, "error": str(exc)}),
            file=sys.stderr,
        )
        return exc.code
    except OSError:
        print(
            json.dumps(
                {
                    "ok": False,
                    "task": args.task,
                    "error": "Local configuration could not be read",
                }
            ),
            file=sys.stderr,
        )
        return 2
    print(json.dumps({"ok": True, "task": args.task, **result}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
