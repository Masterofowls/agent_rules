"""Install .github/instructions/*.instructions.md as Claude Code rules.

Copilot's `applyTo` becomes Claude Code's `paths`; rules with `applyTo: "**"`
get no `paths` so Claude Code loads them in every session.

Usage:
    python install-claude.py              # user-level: ~/.claude/rules/agent-rules/
    python install-claude.py <project>    # project-level: <project>/.claude/rules/agent-rules/
"""

import json
import re
import shutil
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent / ".github" / "instructions"
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


def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.home()
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


if __name__ == "__main__":
    main()
