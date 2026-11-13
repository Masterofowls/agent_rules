# Agent rules

User-level setup for VS Code Copilot, Copilot CLI, and Claude Code. Requires Python 3.10+. Run from a trusted checkout; no administrator privileges are needed.

Windows:
```powershell
.\scripts\setup-agents.ps1 --dry-run
.\scripts\setup-agents.ps1
```

Linux:
```sh
sh scripts/setup-agents.sh --dry-run
sh scripts/setup-agents.sh
```

Add `--external-skills` to download the design/web skills listed in `scripts/external-skills.json` (requires Node.js/npx and internet). Review those sources first; this option can update matching installed skills. Bundled skills install offline. Tools used by operational checks are not installed automatically.

The external sources track upstream names, not pinned snapshots; a removed or renamed skill causes an explicit failure. Host-provided plugin skills such as `agent-customization` are not redistributed. This setup targets Copilot and Claude, not arbitrary agent products.

Instructions go to the VS Code user prompts directory, `~/.copilot/instructions`, and converted Claude rules in `~/.claude/rules/agent-rules`. Bundled skills go to `~/.agents/skills` and `~/.claude/skills`. The existing skill router is registered in Claude settings only; this installer does not claim equivalent Copilot hook enforcement.

Existing unrelated files and settings are preserved. Changed files receive content-addressed backups and atomic replacements; identical files are skipped. Linked destinations and parent directories are rejected. Hook registrations owned by this installer are updated when Python changes; unrelated hooks remain intact. Use `--vscode-prompts PATH` for a non-default VS Code profile, or `--home PATH` with an explicit prompts path for an isolated offline install. Reload agents afterward. The legacy `install-claude.py [project]` entry point delegates to this installer for Claude-only setup and supports `--dry-run`; it no longer deletes existing rules.

Use `--rules-only` to update instructions and Claude hooks without touching installed skills, including existing skill-directory links. It cannot be combined with `--external-skills`.

Framework rules require confirmed dependencies, imports, or configuration. Tool-specific lint and format instructions are loaded for the selected tools, not every manifest edit. Instruction frontmatter uses the repository's constrained format: one JSON-quoted `description` and one JSON string or string array `applyTo`, each on a single line. General YAML syntax is not accepted.

The Claude hook tracks successful tool results: visual edits require a successful audit skill invocation after the latest visual change. Recognizable handler-only JSX/TSX edits and test files are not gated as design work; ambiguous changes remain gated. This is a conservative text heuristic for `Write`, `Edit`, and `MultiEdit`, not proof of a completed visual review; shell edits and other tools are outside its enforcement.

Validation:
```text
python -m unittest discover -s scripts/tests -v
ruff check scripts hooks/skill_router.py install-claude.py
ruff format scripts hooks/skill_router.py install-claude.py
ruff format --check scripts hooks/skill_router.py install-claude.py
coverage run --branch --source=scripts --omit="scripts/tests/*" -m unittest discover -s scripts/tests
coverage report --fail-under=80
```

The setup tests use temporary profiles and mocked third-party downloads. They do not certify upstream skill availability or hook execution in every agent version.
