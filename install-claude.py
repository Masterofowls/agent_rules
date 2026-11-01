"""Install .github/instructions/*.instructions.md as Claude Code rules.

Copilot's `applyTo` becomes Claude Code's `paths`; rules with `applyTo: "**"`
get no `paths` so Claude Code loads them in every session.

Also copies hooks/skill_router.py into .claude/hooks/ and registers it in
.claude/settings.json, keeping any settings and hooks already there.

Usage:
    python install-claude.py              # user-level: ~/.claude/rules/agent-rules/
    python install-claude.py <project>    # project-level: <project>/.claude/rules/agent-rules/
"""

import json
import re
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent
SRC = REPO / ".github" / "instructions"
HOOK_SCRIPT = REPO / "hooks" / "skill_router.py"
# (event, matcher, subcommand)
HOOKS = [
    ("UserPromptSubmit", None, "prompt"),
    ("PreToolUse", "Write|Edit|MultiEdit", "pre-edit"),
    ("Stop", None, "stop"),
]
FRONTMATTER = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n", re.S)


def parse_frontmatter(text):
    match = FRONTMATTER.match(text)
    if not match:
        return {}, text
    meta = {}
    for line in match.group(1).splitlines():
        key, _, value = line.partition(":")
        value = value.strip()
        if value.startswith(("[", '"')):
            value = json.loads(value)
        meta[key.strip()] = value
    return meta, text[match.end():]


def convert(text):
    meta, body = parse_frontmatter(text)
    apply_to = meta.get("applyTo", "**")
    patterns = [apply_to] if isinstance(apply_to, str) else apply_to
    lines = ["---"]
    if meta.get("description"):
        lines.append(f"description: {json.dumps(meta['description'], ensure_ascii=False)}")
    if patterns != ["**"]:
        lines.append("paths:")
        lines += [f"  - {json.dumps(p)}" for p in patterns]
    lines.append("---")
    return "\n".join(lines) + "\n" + body.lstrip("\r\n")


def install_hooks(claude_dir, script_ref):
    hooks_dir = claude_dir / "hooks"
    hooks_dir.mkdir(exist_ok=True)
    shutil.copy2(HOOK_SCRIPT, hooks_dir / HOOK_SCRIPT.name)

    settings_path = claude_dir / "settings.json"
    settings = {}
    if settings_path.exists():
        settings = json.loads(settings_path.read_text(encoding="utf-8"))
    hooks = settings.setdefault("hooks", {})
    for event, matcher, sub in HOOKS:
        command = f'python "{script_ref}" {sub}'
        groups = hooks.setdefault(event, [])
        # Drop an older registration of this script so reinstalls do not duplicate it.
        for group in groups:
            group["hooks"] = [h for h in group.get("hooks", [])
                              if HOOK_SCRIPT.name not in h.get("command", "")]
        groups[:] = [g for g in groups if g["hooks"]]
        group = {"hooks": [{"type": "command", "command": command, "timeout": 10}]}
        if matcher:
            group["matcher"] = matcher
        groups.append(group)
    settings_path.write_text(json.dumps(settings, indent=2) + "\n", encoding="utf-8")
    print(f"Registered {HOOK_SCRIPT.name} in {settings_path}")


def main():
    project = len(sys.argv) > 1
    root = Path(sys.argv[1]) if project else Path.home()
    dest = root / ".claude" / "rules" / "agent-rules"
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    for src in sorted(SRC.glob("*.instructions.md")):
        name = src.name.replace(".instructions.md", ".md")
        text = src.read_text(encoding="utf-8")
        (dest / name).write_text(convert(text), encoding="utf-8", newline="\n")
        print(f"{name}")
    print(f"Installed to {dest}")
    script_ref = ("$CLAUDE_PROJECT_DIR" if project else "$HOME") + f"/.claude/hooks/{HOOK_SCRIPT.name}"
    install_hooks(root / ".claude", script_ref)


if __name__ == "__main__":
    main()
