import contextlib
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location(
    "skill_router", Path(__file__).resolve().parents[2] / "hooks" / "skill_router.py"
)
router = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(router)


class RoutingTest(unittest.TestCase):
    @contextlib.contextmanager
    def transcript(self, events):
        with tempfile.TemporaryDirectory() as directory:
            entries = []
            for index, (name, args, success) in enumerate(events):
                call_id = str(index)
                entries.extend(
                    [
                        {
                            "message": {
                                "content": [
                                    {
                                        "type": "tool_use",
                                        "id": call_id,
                                        "name": name,
                                        "input": args,
                                    }
                                ]
                            }
                        },
                        {
                            "message": {
                                "content": [
                                    {
                                        "type": "tool_result",
                                        "tool_use_id": call_id,
                                        "is_error": not success,
                                    }
                                ]
                            }
                        },
                    ]
                )
            path = Path(directory) / "transcript.jsonl"
            path.write_text(
                "\n".join(json.dumps(entry) for entry in entries), encoding="utf-8"
            )
            yield str(path)

    def output(self, handler, data):
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream):
            handler(data)
        return json.loads(stream.getvalue()) if stream.getvalue() else None

    def test_one_primary_skill_allows_ui_edit(self):
        for skill in router.DESIGN_SKILLS:
            if skill == "no-ai-design-slop":
                continue
            with (
                self.subTest(skill=skill),
                patch.object(router, "installed", return_value=True),
                patch.object(router, "loaded_skills", return_value={skill}),
            ):
                self.assertIsNone(
                    self.output(
                        router.on_pre_edit, {"tool_input": {"file_path": "Page.tsx"}}
                    )
                )

    def test_no_primary_skill_requests_one_not_all(self):
        with (
            patch.object(router, "installed", return_value=True),
            patch.object(router, "loaded_skills", return_value={"no-ai-design-slop"}),
        ):
            result = self.output(
                router.on_pre_edit, {"tool_input": {"file_path": "Page.tsx"}}
            )["hookSpecificOutput"]
            self.assertEqual(result["permissionDecision"], "deny")
            self.assertIn("one suitable", result["permissionDecisionReason"])

    def test_missing_skills_and_non_ui_edits_do_not_block(self):
        with patch.object(router, "installed", return_value=False):
            self.assertIsNone(
                self.output(
                    router.on_pre_edit, {"tool_input": {"file_path": "Page.tsx"}}
                )
            )
        self.assertIsNone(
            self.output(router.on_pre_edit, {"tool_input": {"file_path": "server.py"}})
        )

    def test_prompt_defers_audit_and_discourages_bulk_loading(self):
        with patch.object(router, "installed", return_value=True):
            result = self.output(router.on_prompt, {"prompt": "design a page"})
        text = result["hookSpecificOutput"]["additionalContext"]
        self.assertIn("smallest set", text)
        self.assertIn("Defer the audit", text)
        self.assertNotIn("load all design skills", text)

    def test_final_visual_audit_remains_required(self):
        with (
            patch.object(router, "installed", return_value=True),
            patch.object(router, "pending_visual_audit", return_value=True),
        ):
            self.assertEqual(self.output(router.on_stop, {})["decision"], "block")
            self.assertIsNone(self.output(router.on_stop, {"stop_hook_active": True}))

    def test_audit_must_succeed_after_latest_successful_visual_edit(self):
        edit = (
            "Edit",
            {"file_path": "Page.tsx", "new_string": "<button>Save</button>"},
            True,
        )
        audit = ("Skill", {"skill": "plugin:audit-ai-design-slop"}, True)
        for events, blocked in (
            ([audit, edit], True),
            ([edit, audit], False),
            ([edit, audit, edit], True),
            ([edit, (*audit[:2], False)], True),
            ([(edit[0], edit[1], False)], False),
        ):
            with (
                self.subTest(events=events),
                self.transcript(events) as path,
                patch.object(router, "installed", return_value=True),
            ):
                self.assertEqual(
                    self.output(router.on_stop, {"transcript_path": path}) is not None,
                    blocked,
                )

    def test_failed_skill_invocation_does_not_unlock_visual_edits(self):
        with (
            self.transcript([("Skill", {"skill": "frontend-design"}, False)]) as path,
            patch.object(router, "installed", return_value=True),
        ):
            result = self.output(
                router.on_pre_edit,
                {
                    "transcript_path": path,
                    "tool_input": {"file_path": "Page.tsx", "new_string": "<main />"},
                },
            )
            self.assertEqual(result["hookSpecificOutput"]["permissionDecision"], "deny")

    def test_audit_started_before_edit_finished_does_not_clear_requirement(self):
        blocks = [
            {
                "type": "tool_use",
                "id": "edit",
                "name": "Edit",
                "input": {"file_path": "Page.css", "new_string": "color: red;"},
            },
            {
                "type": "tool_use",
                "id": "audit",
                "name": "Skill",
                "input": {"skill": "audit-ai-design-slop"},
            },
            {"type": "tool_result", "tool_use_id": "edit"},
            {"type": "tool_result", "tool_use_id": "audit"},
        ]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "transcript.jsonl"
            path.write_text(
                "\n".join(
                    json.dumps({"message": {"content": [block]}}) for block in blocks
                ),
                encoding="utf-8",
            )
            self.assertTrue(router.pending_visual_audit(str(path)))

    def test_handler_only_and_test_edits_need_no_design_skill(self):
        with patch.object(router, "installed", return_value=True):
            for args in (
                {
                    "file_path": "Page.tsx",
                    "old_string": "await save();",
                    "new_string": "await save(value);",
                },
                {"file_path": "Page.test.tsx", "new_string": "render(<Page />);"},
                {
                    "file_path": "Page.tsx",
                    "edits": [{"new_string": "await save(value);"}],
                },
            ):
                with self.subTest(args=args):
                    self.assertIsNone(
                        self.output(router.on_pre_edit, {"tool_input": args})
                    )

    def test_plain_jsx_text_changes_remain_gated(self):
        with (
            patch.object(router, "installed", return_value=True),
            patch.object(router, "loaded_skills", return_value=set()),
        ):
            result = self.output(
                router.on_pre_edit,
                {
                    "tool_input": {
                        "file_path": "Page.tsx",
                        "old_string": "Save",
                        "new_string": "Delete",
                    },
                },
            )
            self.assertEqual(result["hookSpecificOutput"]["permissionDecision"], "deny")


if __name__ == "__main__":
    unittest.main()
