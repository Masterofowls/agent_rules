"""Install repository customizations without deleting existing agent data."""

import argparse
import hashlib
import json
import os
import platform
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
META = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n", re.DOTALL)
EVENTS = [
    ("UserPromptSubmit", None, "prompt"),
    ("PreToolUse", "Write|Edit|MultiEdit", "pre-edit"),
    ("Stop", None, "stop"),
]


def convert(text: str, claude: bool) -> str:
    match = META.match(text)
    if not match:
        raise ValueError("Instruction frontmatter missing")
    metadata = {}
    for line in match[1].splitlines():
        key, separator, value = line.partition(":")
        key = key.strip()
        if not separator or key not in ("description", "applyTo") or key in metadata:
            raise ValueError(
                "Frontmatter requires description and applyTo exactly once"
            )
        try:
            metadata[key] = json.loads(value.strip())
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"Frontmatter {key} must be a JSON string or array on one line"
            ) from exc
    if (
        not isinstance(metadata.get("description"), str)
        or not metadata["description"].strip()
    ):
        raise ValueError("Instruction description must be a nonempty string")
    patterns = metadata.get("applyTo")
    if isinstance(patterns, str):
        patterns = [patterns]
    if (
        not isinstance(patterns, list)
        or not patterns
        or any(
            not isinstance(pattern, str) or not pattern.strip() for pattern in patterns
        )
    ):
        raise ValueError("Instruction applyTo must contain nonempty string patterns")
    # The workspace React scope is intentionally narrower than user scope.
    if patterns == ["src/**/*.{js,jsx,ts,tsx,css}"]:
        patterns = ["**/*.{js,jsx,ts,tsx,css}"]
    lines = ["---", "description: " + json.dumps(metadata["description"])]
    if claude:
        if patterns != ["**"]:
            lines += ["paths:", *["  - " + json.dumps(p) for p in patterns]]
    else:
        lines += [
            "applyTo: " + json.dumps(patterns[0] if len(patterns) == 1 else patterns)
        ]
    return "\n".join([*lines, "---", match.string[match.end() :].lstrip("\r\n")])


def check_destination(path: Path) -> None:
    for target in (path, *path.parents):
        if target.is_symlink() or (
            hasattr(target, "is_junction") and target.is_junction()
        ):
            raise ValueError(f"Refusing linked destination: {target}")
    if path.exists() and not path.is_file():
        raise ValueError(f"Destination is not a regular file: {path}")


def put(path: Path, content: bytes, dry_run: bool) -> None:
    check_destination(path)
    if path.exists() and path.read_bytes() == content:
        return
    print(f"{'Would install' if dry_run else 'Installing'}: {path}")
    if dry_run:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        digest = hashlib.sha256(path.read_bytes()).hexdigest()[:16]
        backup = path.with_name(path.name + f".agent-rules-backup-{digest}")
        check_destination(backup)
        if not backup.exists():
            shutil.copy2(path, backup)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            dir=path.parent, prefix=path.name + ".", suffix=".tmp", delete=False
        ) as stream:
            temporary = Path(stream.name)
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        if path.exists():
            shutil.copymode(path, temporary)
        os.replace(temporary, path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()
    if path.read_bytes() != content:
        raise OSError(f"Verification failed: {path}")


def vscode_directory(home: Path) -> Path:
    if platform.system() == "Windows":
        base = home / "AppData" / "Roaming"
        if home == Path.home().resolve():
            base = Path(os.environ.get("APPDATA", str(base)))
    elif platform.system() == "Darwin":
        base = home / "Library" / "Application Support"
    else:
        base = home / ".config"
        if home == Path.home().resolve():
            base = Path(os.environ.get("XDG_CONFIG_HOME", str(base)))
    return base / "Code" / "User" / "prompts"


def owned_hook(command: str, script: Path, home: Path, action: str) -> bool:
    try:
        tokens = shlex.split(command, posix=platform.system() != "Windows")
    except ValueError:
        return False
    if len(tokens) != 3 or tokens[-1] != action:
        return False
    reference = (
        tokens[1].strip('"').replace("${HOME}", str(home)).replace("$HOME", str(home))
    )
    return Path(reference).expanduser().resolve() == script.resolve()


def register_hooks(home: Path, dry_run: bool) -> None:
    directory = home / ".claude"
    script = directory / "hooks" / "skill_router.py"
    path = directory / "settings.json"
    check_destination(script)
    check_destination(path)
    settings = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    hooks = settings.setdefault("hooks", {})
    if not isinstance(hooks, dict):
        raise TypeError("Existing Claude hooks must be an object")
    python = str(Path(sys.executable).resolve())
    if platform.system() == "Windows":
        command_base = f'"{python}" "{script}"'
    else:
        command_base = f"{shlex.quote(python)} {shlex.quote(str(script))}"
    for event, matcher, action in EVENTS:
        groups = hooks.setdefault(event, [])
        if not isinstance(groups, list):
            raise TypeError(f"Existing {event} hooks must be a list")
        command = f"{command_base} {action}"
        retained = []
        for group in groups:
            items = [
                item
                for item in group.get("hooks", [])
                if item.get("type") != "command"
                or not owned_hook(item.get("command", ""), script, home, action)
            ]
            if items or not group.get("hooks"):
                retained.append({**group, "hooks": items})
        groups[:] = retained
        group = {"hooks": [{"type": "command", "command": command, "timeout": 10}]}
        if matcher:
            group["matcher"] = matcher
        groups.append(group)
    put(script, (ROOT / "hooks" / "skill_router.py").read_bytes(), dry_run)
    put(path, (json.dumps(settings, indent=2) + "\n").encode(), dry_run)


def install(args: argparse.Namespace, claude_only: bool = False) -> None:
    home = Path(args.home).expanduser().resolve()
    vscode = (
        Path(args.vscode_prompts).expanduser().resolve()
        if args.vscode_prompts
        else vscode_directory(home)
    )
    # Validate all inputs before starting installation.
    rules = [
        (
            f.name,
            convert(f.read_text(encoding="utf-8"), False),
            convert(f.read_text(encoding="utf-8"), True),
        )
        for f in sorted((ROOT / ".github" / "instructions").glob("*.instructions.md"))
    ]
    if not rules:
        raise ValueError("No repository instructions found")
    settings_path = home / ".claude" / "settings.json"
    check_destination(settings_path)
    if settings_path.exists():
        settings = json.loads(settings_path.read_text(encoding="utf-8"))
        if not isinstance(settings, dict):
            raise ValueError("Claude settings must be an object")
        hooks = settings.get("hooks", {})
        if not isinstance(hooks, dict):
            raise TypeError("Claude hooks must be an object")
        for event, _, _ in EVENTS:
            groups = hooks.get(event, [])
            if not isinstance(groups, list) or any(
                not isinstance(group, dict)
                or not isinstance(group.get("hooks", []), list)
                or any(
                    not isinstance(item, dict)
                    or (
                        item.get("type") == "command"
                        and not isinstance(item.get("command"), str)
                    )
                    for item in group.get("hooks", [])
                )
                for group in groups
            ):
                raise TypeError(f"Invalid existing hook groups: {event}")
    if args.external_skills and not args.dry_run and not shutil.which("npx"):
        raise ValueError("Node.js/npx is required for --external-skills")
    files = []
    for name, copilot, claude in rules:
        if not claude_only:
            files.extend(
                [
                    (home / ".copilot" / "instructions" / name, copilot.encode()),
                    (vscode / name, copilot.encode()),
                ]
            )
        files.append(
            (
                home
                / ".claude"
                / "rules"
                / "agent-rules"
                / name.replace(".instructions", ""),
                claude.encode(),
            )
        )
    skills = (
        []
        if getattr(args, "rules_only", False)
        else sorted((ROOT / ".github" / "skills").iterdir())
    )
    for skill in skills:
        if not skill.is_dir() or not (skill / "SKILL.md").is_file():
            continue
        for source in sorted(skill.rglob("*")):
            if (
                not source.is_file()
                or source.is_symlink()
                or any(
                    part in ("__pycache__", ".ruff_cache", "htmlcov")
                    for part in source.parts
                )
                or source.name == ".coverage"
            ):
                continue
            relative = source.relative_to(skill)
            for destination in (
                home / ".agents" / "skills",
                home / ".claude" / "skills",
            ):
                if not claude_only or destination == home / ".claude" / "skills":
                    files.append(
                        (destination / skill.name / relative, source.read_bytes())
                    )
    for destination in [
        *(path for path, _ in files),
        settings_path,
        home / ".claude" / "hooks" / "skill_router.py",
    ]:
        check_destination(destination)
    for path, content in files:
        put(path, content, args.dry_run)
    register_hooks(home, args.dry_run)
    if args.external_skills:
        packages = json.loads((ROOT / "scripts" / "external-skills.json").read_text())
        for package in packages:
            command = [
                "npx",
                "--yes",
                "skills",
                "add",
                package,
                "-g",
                "-y",
                "-a",
                "github-copilot",
                "-a",
                "claude-code",
            ]
            if args.dry_run:
                print("Would download: " + package)
                continue
            if not shutil.which("npx"):
                raise ValueError("Node.js/npx is required for --external-skills")
            if os.name == "nt":
                command = [
                    os.environ.get("COMSPEC", "cmd.exe"),
                    "/d",
                    "/c",
                    subprocess.list2cmdline(command),
                ]
            subprocess.run(command, check=True, timeout=600)
    print("Setup complete. Reload agent sessions. Hooks registered for Claude only.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--home",
        default="",
        help="Alternate user directory for offline installation/testing",
    )
    parser.add_argument(
        "--vscode-prompts", help="Override VS Code profile prompts directory"
    )
    parser.add_argument(
        "--external-skills",
        action="store_true",
        help="Download third-party skills; may update matching installed skills",
    )
    parser.add_argument(
        "--rules-only",
        action="store_true",
        help="Update instructions and Claude hooks without changing skills",
    )
    args = parser.parse_args()
    if not args.home:
        args.home = str(Path.home())
        custom_home = False
    else:
        custom_home = True
    if args.external_skills and (custom_home or args.vscode_prompts):
        parser.error("--external-skills cannot be combined with custom destinations")
    if args.rules_only and args.external_skills:
        parser.error("--rules-only cannot be combined with --external-skills")
    try:
        install(args)
    except (OSError, ValueError, TypeError, subprocess.SubprocessError) as exc:
        print(f"Setup failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
