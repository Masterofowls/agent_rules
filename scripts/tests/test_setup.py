import argparse
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import setup_agents


class SetupTest(unittest.TestCase):
    def test_atomic_failure_preserves_original_and_cleans_owned_temporary_file(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "rule.md"
            target.write_bytes(b"original")
            with (
                patch("builtins.print"),
                patch("setup_agents.os.replace", side_effect=OSError("replace failed")),
                self.assertRaises(OSError),
            ):
                setup_agents.put(target, b"changed", False)
            self.assertEqual(target.read_bytes(), b"original")
            self.assertFalse(list(target.parent.glob("*.tmp")))
            self.assertEqual(
                next(target.parent.glob("*.agent-rules-backup-*")).read_bytes(),
                b"original",
            )

    def test_linked_parent_is_rejected_before_any_installation(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            linked = home / ".claude" / "rules"
            args = argparse.Namespace(
                home=str(home),
                vscode_prompts=str(home / "prompts"),
                dry_run=False,
                external_skills=False,
            )
            with (
                patch.object(Path, "is_symlink", lambda path: path == linked),
                self.assertRaises(ValueError),
            ):
                setup_agents.install(args)
            self.assertFalse((home / ".copilot").exists())
            self.assertFalse((home / "prompts").exists())

    def test_rules_only_preserves_linked_skill_directories(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            args = argparse.Namespace(
                home=str(home),
                vscode_prompts=str(home / "prompts"),
                dry_run=False,
                external_skills=False,
                rules_only=True,
            )
            linked = home / ".claude" / "skills" / "practice-topic"
            with (
                patch.object(Path, "is_symlink", lambda path: path == linked),
                patch("builtins.print"),
            ):
                setup_agents.install(args)
            self.assertTrue(
                (home / ".copilot" / "instructions" / "react.instructions.md").is_file()
            )
            self.assertTrue((home / ".claude" / "hooks" / "skill_router.py").is_file())
            self.assertFalse((home / ".claude" / "skills").exists())
            self.assertFalse((home / ".agents").exists())

    def test_invalid_frontmatter_reports_explicit_errors(self):
        for metadata in (
            'description: "Valid"',
            'applyTo: "**"',
            'description: ""\napplyTo: "**"',
            'description: "Valid"\napplyTo: []',
            'description: "Valid"\napplyTo: [123]',
            'description: "Valid"\napplyTo: "**"\napplyTo: "*.py"',
            'description: Unquoted YAML\napplyTo: "**"',
            'description: "Valid"\napplyTo:\n  - "*.py"',
        ):
            with self.subTest(metadata=metadata), self.assertRaises(ValueError):
                setup_agents.convert(f"---\n{metadata}\n---\nBody\n", False)

    def test_reinstall_replaces_owned_hooks_when_python_changes(self):
        with tempfile.TemporaryDirectory(prefix="agent profile ") as directory:
            home = Path(directory)
            settings = home / ".claude" / "settings.json"
            with patch("builtins.print"):
                setup_agents.register_hooks(home, False)
            data = json.loads(settings.read_text())
            for event, _, _ in setup_agents.EVENTS:
                data["hooks"][event][0]["hooks"][0]["command"] = data["hooks"][event][
                    0
                ]["hooks"][0]["command"].replace(
                    str(Path(sys.executable).resolve()), "old-python"
                )
            data["hooks"]["Stop"][0]["hooks"].append(
                {"type": "command", "command": "other-hook"}
            )
            settings.write_text(json.dumps(data))
            with patch("builtins.print"):
                setup_agents.register_hooks(home, False)
            result = json.loads(settings.read_text())
            self.assertEqual(
                result["hooks"]["Stop"][0]["hooks"],
                [{"type": "command", "command": "other-hook"}],
            )
            for event, _, action in setup_agents.EVENTS:
                commands = [
                    item["command"]
                    for group in result["hooks"][event]
                    for item in group["hooks"]
                ]
                self.assertEqual(
                    sum(command.endswith(" " + action) for command in commands), 1
                )
                self.assertFalse(any("old-python" in command for command in commands))
            first = settings.read_bytes()
            with patch("builtins.print"):
                setup_agents.register_hooks(home, False)
            self.assertEqual(first, settings.read_bytes())

    def test_owned_hook_matches_legacy_home_reference_and_shell_quoting(self):
        with tempfile.TemporaryDirectory(prefix="agent profile ") as directory:
            home = Path(directory)
            script = home / ".claude" / "hooks" / "skill_router.py"
            for system in ("Windows", "Linux"):
                with (
                    self.subTest(system=system),
                    patch("setup_agents.platform.system", return_value=system),
                ):
                    command = f'python "{script}" stop'
                    self.assertTrue(
                        setup_agents.owned_hook(command, script, home, "stop")
                    )
                    self.assertTrue(
                        setup_agents.owned_hook(
                            'python "$HOME/.claude/hooks/skill_router.py" stop',
                            script,
                            home,
                            "stop",
                        )
                    )
                    self.assertFalse(
                        setup_agents.owned_hook(
                            'python "other-script.py" stop', script, home, "stop"
                        )
                    )
                    self.assertFalse(
                        setup_agents.owned_hook(
                            'python "unterminated', script, home, "stop"
                        )
                    )

    def test_legacy_entry_point_preserves_project_rules_and_installs_claude_only(self):
        spec = importlib.util.spec_from_file_location(
            "legacy_setup", setup_agents.ROOT / "install-claude.py"
        )
        legacy = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(legacy)
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            rules = home / ".claude" / "rules" / "agent-rules"
            rules.mkdir(parents=True)
            unrelated = rules / "custom.md"
            unrelated.write_text("keep")
            changed = rules / "react.md"
            changed.write_text("old rule")
            with (
                patch("sys.argv", ["install-claude.py", str(home)]),
                patch("builtins.print"),
            ):
                self.assertEqual(legacy.main(), 0)
            self.assertEqual(unrelated.read_text(), "keep")
            self.assertEqual(
                next(rules.glob("react.md.agent-rules-backup-*")).read_text(),
                "old rule",
            )
            self.assertFalse((home / ".copilot").exists())
            self.assertFalse((home / ".agents").exists())
            self.assertTrue(
                (home / ".claude" / "skills" / "teach-topic" / "SKILL.md").exists()
            )

    def test_offline_install_preserves_settings_and_is_repeatable(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            settings = home / ".claude" / "settings.json"
            settings.parent.mkdir()
            settings.write_text(
                json.dumps(
                    {
                        "theme": "dark",
                        "hooks": {
                            "Stop": [
                                {
                                    "hooks": [
                                        {"type": "command", "command": "other-hook"}
                                    ]
                                }
                            ]
                        },
                    }
                )
            )
            args = argparse.Namespace(
                home=str(home),
                vscode_prompts=str(home / "prompts"),
                dry_run=False,
                external_skills=False,
            )
            with patch("builtins.print"):
                setup_agents.install(args)
            first = settings.read_bytes()
            self.assertEqual(json.loads(first)["theme"], "dark")
            self.assertEqual(len(json.loads(first)["hooks"]["Stop"]), 2)
            with patch("builtins.print"):
                setup_agents.install(args)
            self.assertEqual(first, settings.read_bytes())
            self.assertTrue((home / ".agents/skills/ops-checks/SKILL.md").is_file())
            self.assertTrue((home / ".claude/skills/teach-topic/SKILL.md").is_file())
            rules = list((home / ".copilot/instructions").glob("*.instructions.md"))
            self.assertGreater(len(rules), 60)
            self.assertIn(
                "**/*.{js,jsx,ts,tsx,css}",
                (home / "prompts/react.instructions.md").read_text(),
            )

    def test_dry_run_does_not_create_destination(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory) / "not-created"
            args = argparse.Namespace(
                home=str(home),
                vscode_prompts=str(home / "prompts"),
                dry_run=True,
                external_skills=False,
            )
            with patch("builtins.print"):
                setup_agents.install(args)
            self.assertFalse(home.exists())

    def test_backup_and_symlink_safety(self):
        with tempfile.TemporaryDirectory() as directory:
            file = Path(directory) / "rules"
            file.write_bytes(b"original")
            with patch("builtins.print"):
                setup_agents.put(file, b"new", False)
            self.assertEqual(file.read_bytes(), b"new")
            backups = list(file.parent.glob("rules.agent-rules-backup-*"))
            self.assertEqual(backups[0].read_bytes(), b"original")
            with (
                patch.object(Path, "is_symlink", return_value=True),
                self.assertRaises(ValueError),
            ):
                setup_agents.put(file, b"changed", False)

    def test_invalid_settings_do_not_install_rules(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            settings = home / ".claude/settings.json"
            settings.parent.mkdir()
            settings.write_text("invalid")
            args = argparse.Namespace(
                home=str(home),
                vscode_prompts=str(home / "prompts"),
                dry_run=False,
                external_skills=False,
            )
            with self.assertRaises(ValueError):
                setup_agents.install(args)
            self.assertFalse((home / ".copilot").exists())

    def test_custom_home_paths_ignore_real_profile_environment(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            for system, relative in (
                ("Windows", "AppData/Roaming/Code/User/prompts"),
                ("Linux", ".config/Code/User/prompts"),
                ("Darwin", "Library/Application Support/Code/User/prompts"),
            ):
                with patch("setup_agents.platform.system", return_value=system):
                    self.assertEqual(
                        setup_agents.vscode_directory(home), home / relative
                    )

    def test_external_install_commands_without_network(self):
        with tempfile.TemporaryDirectory() as directory:
            args = argparse.Namespace(
                home=directory,
                vscode_prompts=str(Path(directory) / "prompts"),
                dry_run=False,
                external_skills=True,
            )
            with (
                patch("builtins.print"),
                patch("setup_agents.shutil.which", return_value="/npx"),
                patch("setup_agents.subprocess.run") as run,
            ):
                setup_agents.install(args)
            packages = json.loads(
                (setup_agents.ROOT / "scripts/external-skills.json").read_text()
            )
            self.assertEqual(run.call_count, len(packages))
            self.assertTrue(all(call.kwargs["check"] for call in run.call_args_list))
            args.dry_run = True
            with patch("builtins.print"), patch("setup_agents.subprocess.run") as run:
                setup_agents.install(args)
            run.assert_not_called()

    def test_conversion_and_main_errors(self):
        with self.assertRaises(ValueError):
            setup_agents.convert("missing metadata", False)
        with (
            patch("sys.argv", ["setup_agents.py", "--dry-run"]),
            patch("setup_agents.install") as install,
        ):
            self.assertEqual(setup_agents.main(), 0)
            self.assertEqual(install.call_args.args[0].home, str(Path.home()))
        with (
            patch("sys.argv", ["setup_agents.py"]),
            patch("setup_agents.install", side_effect=OSError("failed")),
            patch("builtins.print"),
        ):
            self.assertEqual(setup_agents.main(), 1)

    def test_malformed_hooks_and_missing_npx_preflight(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            settings = home / ".claude/settings.json"
            settings.parent.mkdir()
            args = argparse.Namespace(
                home=directory,
                vscode_prompts=None,
                dry_run=False,
                external_skills=False,
            )
            for value in (
                [],
                {"hooks": []},
                {"hooks": {"Stop": [None]}},
                {"hooks": {"Stop": [{"hooks": [None]}]}},
            ):
                settings.write_text(json.dumps(value))
                with self.assertRaises((ValueError, TypeError)):
                    setup_agents.install(args)
                self.assertFalse((home / ".copilot").exists())
            settings.write_text("{}")
            args.external_skills = True
            with (
                patch("setup_agents.shutil.which", return_value=None),
                self.assertRaises(ValueError),
            ):
                setup_agents.install(args)
            self.assertFalse((home / ".copilot").exists())


if __name__ == "__main__":
    unittest.main()
