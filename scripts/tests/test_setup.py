import argparse
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import setup_agents


class SetupTest(unittest.TestCase):
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
