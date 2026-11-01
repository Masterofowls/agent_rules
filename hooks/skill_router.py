"""Claude Code hook that routes tasks to skills and enforces the design skills.

Subcommands, one per hook event:
    prompt    UserPromptSubmit: names the skills that match the prompt.
    pre-edit  PreToolUse (Write|Edit|MultiEdit): blocks UI file edits until the
              design skills are loaded in this session.
    stop      Stop: blocks finishing after UI edits until audit-ai-design-slop ran.

Skills that are not installed in ~/.claude/skills are never required, so a
missing skill cannot lock the session.
"""

import json
import re
import sys
from pathlib import Path

SKILLS_DIR = Path.home() / ".claude" / "skills"

DESIGN_SKILLS = [
    "frontend-design",
    "web-design-guidelines",
    "design-taste-frontend",
    "impeccable",
    "ui-ux-pro-max",
    "no-ai-design-slop",
]
AUDIT_SKILL = "audit-ai-design-slop"

UI_FILE = re.compile(
    r"\.(css|scss|sass|less|styl|html?|jsx|tsx|vue|svelte|astro|mdx)$", re.I
)

# Mirrors the "Quick task associations" table in skills.instructions.md.
ROUTES = [
    (r"design|redesign|layout|responsive|mobile ui|\bui\b|\bux\b|landing|hero|"
     r"styl|css|tailwind|component|page|screen|dashboard|дизайн|вёрстк|верстк|"
     r"интерфейс|макет|страниц|стил",
     DESIGN_SKILLS + [AUDIT_SKILL]),
    (r"slop|generic|ai-made|looks ai|шаблонн", [AUDIT_SKILL, "no-ai-design-slop"]),
    (r"perform|slow|lighthouse|web vitals|\blcp\b|\bcls\b|\binp\b|скорост|тормоз|"
     r"производительн",
     ["web-perf", "web-quality-audit", "vercel-react-best-practices"]),
    (r"a11y|accessib|wcag|screen reader|keyboard nav|доступност",
     ["accessibility", "agent-browser"]),
    (r"\bqa\b|smoke test|test the (site|app|website)|reproduce|browser bug|"
     r"протестир", ["agent-browser"]),
    (r"playwright|e2e|end-to-end", ["playwright-best-practices"]),
    (r"\bseo\b|meta tags|indexing|ranking|sitemap", ["seo-audit"]),
    (r"react|hook|rerender|re-render", ["vercel-react-best-practices"]),
    (r"composition|compound component", ["vercel-composition-patterns"]),
    (r"drizzle", ["drizzle-orm-patterns"]),
    (r"postgres|psql|supabase|\bsql\b|migration|index", ["supabase-postgres-best-practices"]),
    (r"shadcn|components\.json", ["shadcn"]),
    (r"deploy|docker|ci/cd|\bci\b|release|production ready|деплой",
     ["deployment-patterns"]),
    (r"vercel", ["deploy-to-vercel", "vercel-cli-with-tokens"]),
    (r"russian|русск|перевод|translat|\bru\b locale|склонен|падеж",
     ["russian-language"]),
    (r"teach me|explain|help me understand|научи|объясни|разобраться",
     ["teach-topic"]),
    (r"quiz|exercise|practice|check my (solution|understanding)|задани|"
     r"потренир|проверь мои", ["practice-topic"]),
    (r"security|vulnerab|harden|best practice|modernize", ["best-practices"]),
    (r"find (a )?skill|install (a )?skill", ["find-skills"]),
    (r"writing|copy|text|readme|docs|commit message|текст", ["writing-guidelines", "unslop"]),
]


def installed(name):
    return (SKILLS_DIR / name).exists()


def read_input():
    try:
        return json.load(sys.stdin)
    except ValueError:
        return {}


def transcript_entries(path):
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                try:
                    yield json.loads(line)
                except ValueError:
                    continue
    except OSError:
        return


def tool_uses(path):
    for entry in transcript_entries(path):
        content = (entry.get("message") or {}).get("content")
        if not isinstance(content, list):
            continue
        for block in content:
            if isinstance(block, dict) and block.get("type") == "tool_use":
                yield block.get("name"), block.get("input") or {}


def loaded_skills(path):
    names = set()
    for name, args in tool_uses(path):
        if name == "Skill" and args.get("skill"):
            # Plugin skills are invoked as "plugin:skill".
            names.add(args["skill"].split(":")[-1])
    return names


def edited_ui_files(path):
    for name, args in tool_uses(path):
        if name in ("Write", "Edit", "MultiEdit") and UI_FILE.search(args.get("file_path", "")):
            return True
    return False


def emit(obj):
    json.dump(obj, sys.stdout, ensure_ascii=False)


def on_prompt(data):
    prompt = data.get("prompt", "").lower()
    matched = []
    for pattern, skills in ROUTES:
        if re.search(pattern, prompt):
            matched += [s for s in skills if installed(s) and s not in matched]
    lines = [
        "Skill routing (from ~/.claude/hooks/skill_router.py): check the skill "
        "catalog and invoke every skill that matches this task with the Skill "
        "tool before replying or editing files."
    ]
    if matched:
        lines.append("Matched by keywords, invoke the ones that apply: " + ", ".join(matched) + ".")
    if any(s in matched for s in DESIGN_SKILLS):
        lines.append(
            "UI work: load all design skills before editing UI files and run "
            f"{AUDIT_SKILL} before finishing. Edits to UI files are blocked until "
            "the design skills are loaded."
        )
    emit({"hookSpecificOutput": {
        "hookEventName": "UserPromptSubmit",
        "additionalContext": "\n".join(lines),
    }})


def on_pre_edit(data):
    path = (data.get("tool_input") or {}).get("file_path", "")
    if not UI_FILE.search(path):
        return
    have = loaded_skills(data.get("transcript_path", ""))
    missing = [s for s in DESIGN_SKILLS if installed(s) and s not in have]
    if not missing:
        return
    emit({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": (
            f"{Path(path).name} is a UI file and these design skills are not "
            f"loaded yet: {', '.join(missing)}. Invoke each with the Skill tool, "
            "apply their guidance, then retry the edit."
        ),
    }})


def on_stop(data):
    # Without this check a Stop block would re-trigger itself indefinitely.
    if data.get("stop_hook_active") or not installed(AUDIT_SKILL):
        return
    transcript = data.get("transcript_path", "")
    if not edited_ui_files(transcript) or AUDIT_SKILL in loaded_skills(transcript):
        return
    emit({
        "decision": "block",
        "reason": (
            f"UI files were edited but {AUDIT_SKILL} has not run. Invoke it, "
            "fix what it finds, then finish."
        ),
    })


HANDLERS = {"prompt": on_prompt, "pre-edit": on_pre_edit, "stop": on_stop}

if __name__ == "__main__":
    handler = HANDLERS.get(sys.argv[1] if len(sys.argv) > 1 else "")
    if handler:
        handler(read_input())
