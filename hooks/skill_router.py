"""Claude Code hook that suggests skills and requires one primary design skill.

Subcommands, one per hook event:
    prompt    UserPromptSubmit: names the skills that match the prompt.
    pre-edit  PreToolUse (Write|Edit|MultiEdit): gates visual edits on one
              primary design skill, without gating handler-only changes.
    stop      Stop: requires an audit invocation after the latest visual edit.

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
    r"\.(css|scss|sass|less|styl|html?|jsx|tsx|vue|svelte|astro|mdx)$", re.IGNORECASE
)
MARKUP = re.compile(r"<[A-Za-z/>]|\b(className|style|class)\s*=|aria-", re.IGNORECASE)
HANDLER_CODE = re.compile(
    r"^(?:await\b|throw\b|(?:async\s+)?function\s+handle\w+\b|"
    r"(?:const|let)\s+handle\w+\s*=)"
)

# Mirrors the "Quick task associations" table in skills.instructions.md.
ROUTES = [
    (
        (
            r"design|redesign|layout|responsive|mobile ui|\bui\b|\bux\b|landing|hero|"
            r"styl|css|tailwind|component|page|screen|dashboard|дизайн|вёрстк|верстк|"
            r"интерфейс|макет|страниц|стил"
        ),
        DESIGN_SKILLS + [AUDIT_SKILL],
    ),
    (r"slop|generic|ai-made|looks ai|шаблонн", [AUDIT_SKILL, "no-ai-design-slop"]),
    (
        (
            r"perform|slow|lighthouse|web vitals|\blcp\b|\bcls\b|\binp\b|скорост|тормоз|"
            r"производительн"
        ),
        ["web-perf", "web-quality-audit", "vercel-react-best-practices"],
    ),
    (
        r"a11y|accessib|wcag|screen reader|keyboard nav|доступност",
        ["accessibility", "agent-browser"],
    ),
    (
        (
            r"\bqa\b|smoke test|test the (site|app|website)|reproduce|browser bug|"
            r"протестир"
        ),
        ["agent-browser"],
    ),
    (r"playwright|e2e|end-to-end", ["playwright-best-practices"]),
    (r"\bseo\b|meta tags|indexing|ranking|sitemap", ["seo-audit"]),
    (r"react|hook|rerender|re-render", ["vercel-react-best-practices"]),
    (r"composition|compound component", ["vercel-composition-patterns"]),
    (r"drizzle", ["drizzle-orm-patterns"]),
    (
        r"postgres|psql|supabase|\bsql\b|migration|index",
        ["supabase-postgres-best-practices"],
    ),
    (r"shadcn|components\.json", ["shadcn"]),
    (
        r"deploy|docker|ci/cd|\bci\b|release|production ready|деплой",
        ["deployment-patterns"],
    ),
    (
        r"devops|terraform|kubernetes|\bhelm\b|ansible|observability|incident|recovery",
        ["deployment-patterns"],
    ),
    (
        r"\bdns\b|\btls\b|certificate expir|disk (space|capacity)|git state|worktree",
        ["ops-checks"],
    ),
    (r"vercel", ["deploy-to-vercel", "vercel-cli-with-tokens"]),
    (
        r"russian|русск|перевод|translat|\bru\b locale|склонен|падеж",
        ["russian-language"],
    ),
    (r"teach me|explain|help me understand|научи|объясни|разобраться", ["teach-topic"]),
    (
        (
            r"quiz|exercise|practice|check my (solution|understanding)|задани|"
            r"потренир|проверь мои"
        ),
        ["practice-topic"],
    ),
    (r"security|vulnerab|harden|best practice|modernize", ["best-practices"]),
    (r"find (a )?skill|install (a )?skill", ["find-skills"]),
    (
        r"writing|copy|text|readme|docs|commit message|текст",
        ["writing-guidelines", "unslop"],
    ),
]


def installed(name):
    return (SKILLS_DIR / name / "SKILL.md").is_file()


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


def completed_tool_uses(path):
    pending = {}
    for entry_index, entry in enumerate(transcript_entries(path)):
        content = (entry.get("message") or {}).get("content")
        if not isinstance(content, list):
            continue
        for block_index, block in enumerate(content):
            if not isinstance(block, dict):
                continue
            if block.get("type") == "tool_use" and block.get("id"):
                pending[block["id"]] = (
                    block.get("name"),
                    block.get("input") or {},
                    (entry_index, block_index),
                )
            elif block.get("type") == "tool_result":
                call = pending.pop(block.get("tool_use_id"), None)
                if call and not block.get("is_error"):
                    yield (*call, (entry_index, block_index))


def loaded_skills(path):
    names = set()
    for name, args, _, _ in completed_tool_uses(path):
        if name == "Skill" and args.get("skill"):
            # Plugin skills are invoked as "plugin:skill".
            names.add(args["skill"].split(":")[-1])
    return names


def is_visual_edit(args):
    path = args.get("file_path", "")
    if not UI_FILE.search(path) or re.search(r"\.(test|spec)\.[^.]+$", path):
        return False
    if Path(path).suffix.lower() not in (".jsx", ".tsx"):
        return True
    changes = args.get("edits", [args])
    strings = [
        change[key]
        for change in changes
        for key in ("old_string", "new_string", "content")
        if isinstance(change.get(key), str)
    ]
    # Only recognizable handler code can bypass the gate; plain text is unknown.
    return not strings or not all(
        HANDLER_CODE.search(text.strip()) and not MARKUP.search(text)
        for text in strings
    )


def pending_visual_audit(path):
    pending = False
    last_edit = (-1, -1)
    for name, args, started, completed in completed_tool_uses(path):
        if name in ("Write", "Edit", "MultiEdit") and is_visual_edit(args):
            pending = True
            last_edit = completed
        elif (
            name == "Skill"
            and args.get("skill", "").split(":")[-1] == AUDIT_SKILL
            and started > last_edit
        ):
            pending = False
    return pending


def emit(obj):
    json.dump(obj, sys.stdout, ensure_ascii=False)


def on_prompt(data):
    prompt = data.get("prompt", "").lower()
    matched = []
    for pattern, skills in ROUTES:
        if re.search(pattern, prompt):
            matched += [s for s in skills if installed(s) and s not in matched]
    lines = [
        (
            "Skill routing (from ~/.claude/hooks/skill_router.py): check the skill "
            "catalog descriptions and invoke the smallest set needed for the current "
            "step. Keyword matches are candidates, not a bulk-loading checklist."
        )
    ]
    if matched:
        lines.append(
            "Matched by keywords, invoke the ones that apply: "
            + ", ".join(matched)
            + "."
        )
    if any(s in matched for s in DESIGN_SKILLS):
        lines.append(
            "UI work: select one primary design skill before visual edits and run "
            f"{AUDIT_SKILL} after the latest visual edit. Visual edits are blocked until "
            "a primary design skill is loaded. Defer the audit until final visual review."
        )
    emit(
        {
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": "\n".join(lines),
            }
        }
    )


def on_pre_edit(data):
    args = data.get("tool_input") or {}
    path = args.get("file_path", "")
    if not is_visual_edit(args):
        return
    have = loaded_skills(data.get("transcript_path", ""))
    primary = [s for s in DESIGN_SKILLS if s != "no-ai-design-slop" and installed(s)]
    if not primary or any(s in have for s in primary):
        return
    emit(
        {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": (
                    f"{Path(path).name} has a visual edit. Select and invoke one suitable "
                    f"primary design skill: {', '.join(primary)}. Do not load all of them. "
                    "Apply its guidance, then retry the edit."
                ),
            }
        }
    )


def on_stop(data):
    # Without this check a Stop block would re-trigger itself indefinitely.
    if data.get("stop_hook_active") or not installed(AUDIT_SKILL):
        return
    transcript = data.get("transcript_path", "")
    if not pending_visual_audit(transcript):
        return
    emit(
        {
            "decision": "block",
            "reason": (
                f"Visual edits need a successful {AUDIT_SKILL} invocation after "
                "the latest edit. Invoke it, review the result, fix findings, and "
                "repeat the audit if you make further visual edits."
            ),
        }
    )


HANDLERS = {"prompt": on_prompt, "pre-edit": on_pre_edit, "stop": on_stop}

if __name__ == "__main__":
    handler = HANDLERS.get(sys.argv[1] if len(sys.argv) > 1 else "")
    if handler:
        handler(read_input())
