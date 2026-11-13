import argparse
import contextlib
import importlib.util
import io
import json
import os
import socket
import subprocess
import sys
import tempfile
import unittest
import urllib.error
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import checks
import network_probe

spec = importlib.util.spec_from_file_location("launcher", SCRIPTS / "run.py")
launcher = importlib.util.module_from_spec(spec)
sys.modules["launcher"] = launcher
spec.loader.exec_module(launcher)


class ChecksTest(unittest.TestCase):
    def invoke(self, argv: list[str]) -> tuple[int, dict]:
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = checks.main(argv)
        return code, json.loads(out.getvalue() or err.getvalue())

    def test_detection(self):
        for system in ("Windows", "Linux", "Darwin"):
            with (
                self.subTest(system=system),
                patch("checks.platform.system", return_value=system),
                patch("checks.platform.release", return_value="microsoft"),
            ):
                code, result = self.invoke(["detect-os"])
                self.assertEqual(code, 0)
                self.assertEqual(result["os"], system)
                self.assertEqual(result["wsl"], system == "Linux")
        with patch("checks.platform.system", return_value="Other"):
            self.assertEqual(self.invoke(["detect-os"])[0], 2)

    def test_authorization_blocks_remote_commands(self):
        for argv in (
            ["check-url", "--url", "https://example.test"],
            ["check-dns", "--host", "example.test"],
            ["check-tls", "--host", "example.test"],
            ["check-postgres", "--service", "test"],
            ["check-supabase", "--service", "test"],
            ["check-ssh", "--host", "example.test", "--user", "deploy"],
            ["check-ftp", "--url", "ftps://example.test", "--netrc-file", "absent"],
            ["setup-ubuntu", "--apply"],
        ):
            with self.subTest(task=argv[0]), patch("checks.execute") as execute:
                self.assertEqual(self.invoke(argv)[0], 2)
                execute.assert_not_called()

    def test_network_parent_bounds_entire_probe_and_rejects_bad_hosts(self):
        for task in ("check-dns", "check-tls"):
            with patch("checks.execute", return_value='{"verified": true}') as execute:
                code, result = self.invoke(
                    [task, "--host", "example.test", "--timeout", "7", "--authorized"]
                )
                self.assertEqual(code, 0)
                self.assertTrue(result["verified"])
                command, timeout = execute.call_args.args
                self.assertEqual(command[0], sys.executable)
                self.assertIn("network_probe.py", command[1])
                self.assertEqual(timeout, 7)
                self.assertIn("--authorized", command)
            with patch(
                "checks.execute", side_effect=checks.CheckError("probe timed out")
            ):
                self.assertEqual(
                    self.invoke([task, "--host", "example.test", "--authorized"])[0], 1
                )
        for host in (
            "https://example.test",
            "host;command",
            "bad host",
            "-option",
            "host..",
        ):
            with self.subTest(host=host), self.assertRaises(checks.CheckError):
                checks.host_name(host)
        with patch("checks.execute", return_value="not JSON"):
            self.assertEqual(
                self.invoke(["check-dns", "--host", "example.test", "--authorized"])[0],
                1,
            )

    def test_dns_addresses_are_deduplicated_without_exposing_addresses(self):
        args = argparse.Namespace(
            task="check-dns", host="example.test", authorized=True
        )
        records = [
            (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("192.0.2.1", 0)),
            (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("192.0.2.1", 0)),
            (socket.AF_INET6, socket.SOCK_STREAM, 6, "", ("2001:db8::1", 0, 0, 0)),
        ]
        with patch("network_probe.socket.getaddrinfo", return_value=records):
            result = network_probe.probe(args)
        self.assertEqual(result, {"resolved": True, "ipv4_count": 1, "ipv6_count": 1})
        with (
            patch("network_probe.socket.getaddrinfo", return_value=[]),
            self.assertRaises(checks.CheckError),
        ):
            network_probe.probe(args)
        args.authorized = False
        with (
            patch("network_probe.socket.getaddrinfo") as lookup,
            self.assertRaises(checks.CheckError),
        ):
            network_probe.probe(args)
        lookup.assert_not_called()

    def test_dns_child_process_with_localhost_only(self):
        code, result = self.invoke(["check-dns", "--host", "localhost", "--authorized"])
        self.assertEqual(code, 0)
        self.assertTrue(result["resolved"])
        self.assertGreaterEqual(result["ipv4_count"] + result["ipv6_count"], 1)

    def test_tls_verifies_hostname_and_exact_expiry_threshold(self):
        args = argparse.Namespace(
            task="check-tls",
            host="example.test",
            port=443,
            timeout=7,
            min_days=14,
            authorized=True,
        )
        context, connection = MagicMock(), MagicMock()
        context.wrap_socket.return_value.__enter__.return_value.getpeercert.return_value = {
            "notAfter": "expiry"
        }
        for days, passes in ((14, True), (13.999, False), (0, False)):
            with (
                self.subTest(days=days),
                patch("network_probe.ssl.create_default_context", return_value=context),
                patch(
                    "network_probe.socket.create_connection", return_value=connection
                ) as connect,
                patch(
                    "network_probe.ssl.cert_time_to_seconds", return_value=days * 86400
                ),
                patch("network_probe.time.time", return_value=0),
            ):
                if passes:
                    result = network_probe.probe(args)
                    self.assertEqual(result["days_remaining"], 14)
                    self.assertTrue(result["verified"])
                else:
                    with self.assertRaises(checks.CheckError):
                        network_probe.probe(args)
                self.assertEqual(connect.call_args.kwargs["timeout"], 7)
                self.assertEqual(
                    context.wrap_socket.call_args.kwargs["server_hostname"],
                    "example.test",
                )
        context.wrap_socket.return_value.__enter__.return_value.getpeercert.return_value = {}
        with (
            patch("network_probe.ssl.create_default_context", return_value=context),
            patch("network_probe.socket.create_connection", return_value=connection),
            self.assertRaises(checks.CheckError),
        ):
            network_probe.probe(args)

    def test_network_child_reports_failures_without_native_output(self):
        for failure in (
            checks.CheckError("no permission", 2),
            OSError("private-host-details"),
        ):
            with (
                patch(
                    "sys.argv",
                    ["network_probe.py", "check-tls", "--host", "example.test"],
                ),
                patch("network_probe.probe", side_effect=failure),
                contextlib.redirect_stderr(io.StringIO()) as stream,
            ):
                self.assertEqual(
                    network_probe.main(),
                    2 if isinstance(failure, checks.CheckError) else 1,
                )
                self.assertNotIn("private-host-details", stream.getvalue())

    def test_disk_thresholds_include_boundary_and_each_failure(self):
        gib = 1024**3
        for free, code in ((gib, 0), (gib - 1, 1), (2 * gib, 0)):
            with patch(
                "checks.shutil.disk_usage",
                return_value=SimpleNamespace(total=10 * gib, free=free),
            ):
                self.assertEqual(self.invoke(["check-disk"])[0], code)
        with patch(
            "checks.shutil.disk_usage",
            return_value=SimpleNamespace(total=100 * gib, free=2 * gib),
        ):
            self.assertEqual(self.invoke(["check-disk"])[0], 1)
        with patch("checks.shutil.disk_usage", side_effect=OSError):
            self.assertEqual(self.invoke(["check-disk"])[0], 2)

    def test_git_state_handles_renames_newline_paths_and_conflicts_without_writes(self):
        records = (
            "1 .M N... metadata path with\nnewline\0"
            + "2 R. N... metadata renamed\0? old name\0"
            + "? untracked\0u UU metadata conflict\0"
        )
        with patch(
            "checks.execute", side_effect=["true", "feature/test", records]
        ) as execute:
            code, result = self.invoke(["check-git-state"])
            self.assertEqual(code, 0)
            self.assertFalse(result["clean"])
            self.assertEqual(
                {
                    key: result[key]
                    for key in ("staged", "unstaged", "untracked", "conflicted")
                },
                {"staged": 1, "unstaged": 1, "untracked": 1, "conflicted": 1},
            )
            self.assertNotIn("newline", json.dumps(result))
            self.assertIn("--no-optional-locks", execute.call_args.args[0])
        with patch("checks.execute", side_effect=["true", "", ""]):
            code, result = self.invoke(["check-git-state", "--require-clean"])
            self.assertEqual(code, 0)
            self.assertTrue(result["detached"])
        with patch("checks.execute", side_effect=["true", "main", "? file\0"]):
            self.assertEqual(self.invoke(["check-git-state", "--require-clean"])[0], 1)

    def test_url_validation(self):
        for url in (
            "https://user:password@example.test",
            "file:///tmp/test",
            "https://example.test:99999",
            "https://example.test/#fragment",
            "https://example.test/a b",
            "https:///missing",
        ):
            with self.subTest(url=url), self.assertRaises(checks.CheckError):
                checks.target_url(url, ("https",))
        checks.target_url("https://example.test:443/path", ("https",))

    def test_url_head_and_fallback(self):
        response = MagicMock()
        response.__enter__.return_value.status = 204
        opener = MagicMock()
        for fallback in (False, True):
            opener.open.side_effect = (
                [urllib.error.HTTPError("url", 405, "method", {}, None), response]
                if fallback
                else [response]
            )
            with patch("checks.urllib.request.build_opener", return_value=opener):
                code, result = self.invoke(
                    ["check-url", "--url", "https://example.test", "--authorized"]
                )
            self.assertEqual(code, 0)
            self.assertEqual(result["method"], "GET" if fallback else "HEAD")
        self.assertIsNone(
            checks.NoRedirect().redirect_request(
                None, None, 302, "", {}, "https://elsewhere.test"
            )
        )

    def test_url_failures(self):
        import socket
        import ssl

        for failure in (
            urllib.error.HTTPError("url", 302, "redirect", {}, None),
            urllib.error.HTTPError("url", 500, "failure", {}, None),
            urllib.error.URLError(ssl.SSLError()),
            urllib.error.URLError(socket.gaierror()),
            urllib.error.URLError(TimeoutError()),
            urllib.error.URLError(ConnectionError()),
            TimeoutError(),
        ):
            opener = MagicMock()
            opener.open.side_effect = failure
            with (
                self.subTest(failure=type(failure)),
                patch("checks.urllib.request.build_opener", return_value=opener),
            ):
                self.assertEqual(
                    self.invoke(
                        ["check-url", "--url", "https://example.test", "--authorized"]
                    )[0],
                    1,
                )
        response = MagicMock()
        response.__enter__.return_value.status = 304
        opener.open.side_effect = None
        opener.open.return_value = response
        with patch("checks.urllib.request.build_opener", return_value=opener):
            self.assertEqual(
                self.invoke(
                    ["check-url", "--url", "https://example.test", "--authorized"]
                )[0],
                1,
            )

    def test_postgres_read_only_tls_and_no_secret_arguments(self):
        for task in ("check-postgres", "check-supabase"):
            with patch("checks.execute", return_value="1") as execute:
                self.assertEqual(
                    self.invoke([task, "--service", "test", "--authorized"])[0], 0
                )
                command, timeout, env = execute.call_args.args
                self.assertIn("SELECT 1", command)
                self.assertEqual(env["PGSSLMODE"], "verify-full")
                self.assertIn("read_only=on", env["PGOPTIONS"])
                self.assertEqual(env["PGSERVICE"], "test")
                self.assertEqual(timeout, 15)
        for service in ("postgres://secret", "bad name"):
            self.assertEqual(
                self.invoke(["check-postgres", "--service", service, "--authorized"])[
                    0
                ],
                2,
            )
        with patch("checks.execute", return_value="unexpected"):
            self.assertEqual(
                self.invoke(["check-postgres", "--service", "test", "--authorized"])[0],
                1,
            )

    def test_ssh_argument_safety(self):
        with patch("checks.execute") as execute:
            self.assertEqual(
                self.invoke(
                    [
                        "check-ssh",
                        "--host",
                        "example.test",
                        "--user",
                        "deploy",
                        "--authorized",
                    ]
                )[0],
                0,
            )
            command = execute.call_args.args[0]
            self.assertIn("StrictHostKeyChecking=yes", command)
            self.assertIn("ForwardAgent=no", command)
            self.assertEqual(command[-1], "true")
        for field, value in (("--host", "x;touch"), ("--user", "bad user")):
            argv = [
                "check-ssh",
                "--host",
                "example.test",
                "--user",
                "deploy",
                "--authorized",
            ]
            argv[argv.index(field) + 1] = value
            self.assertEqual(self.invoke(argv)[0], 2)

    def test_ftp_requires_private_file_and_tls(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "private file"
            argv = [
                "check-ftp",
                "--url",
                "ftps://example.test/path/",
                "--netrc-file",
                str(path),
                "--authorized",
            ]
            self.assertEqual(self.invoke(argv)[0], 2)
            path.write_text("", encoding="utf-8")
            path.chmod(0o600)
            with patch("checks.execute") as execute:
                self.assertEqual(self.invoke(argv)[0], 0)
                command = execute.call_args.args[0]
                self.assertIn("--ssl-reqd", command)
                self.assertIn("--list-only", command)
                self.assertIn(str(path), command)

    def test_git_scope_and_redaction(self):
        for scope, count in (("all", 3), ("history", 2), ("files", 2)):
            with patch("checks.execute") as execute:
                self.assertEqual(
                    self.invoke(["check-git-leaks", "--scope", scope])[0], 0
                )
                self.assertEqual(execute.call_count, count)
                self.assertIn("--redact", execute.call_args.args[0])
        with patch("checks.execute", side_effect=checks.CheckError("scan failed")):
            self.assertEqual(self.invoke(["check-git-leaks"])[0], 1)

    def test_tools(self):
        self.assertEqual(self.invoke(["check-tools", "--tools", "python"])[0], 0)
        with (
            patch("checks.shutil.which", return_value="/tool"),
            patch("checks.execute", return_value="version"),
        ):
            self.assertEqual(
                self.invoke(["check-tools", "--tools", "node", "npm", "git"])[0], 0
            )
        with patch("checks.shutil.which", return_value=None):
            self.assertEqual(self.invoke(["check-tools", "--tools", "node"])[0], 2)
        self.assertEqual(self.invoke(["check-tools", "--tools", "unknown"])[0], 2)

    def test_docker_requires_daemon(self):
        with patch("checks.execute", return_value="version") as execute:
            self.assertEqual(self.invoke(["check-docker"])[0], 0)
            self.assertEqual(execute.call_count, 2)
        with patch(
            "checks.execute", side_effect=["version", checks.CheckError("down")]
        ):
            self.assertEqual(self.invoke(["check-docker"])[0], 1)

    def test_ubuntu_preview_never_mutates(self):
        with patch("checks.execute") as execute:
            code, result = self.invoke(["setup-ubuntu"])
            self.assertEqual(code, 0)
            self.assertTrue(result["preview"])
            execute.assert_not_called()

    def test_ubuntu_apply_guards(self):
        argv = ["setup-ubuntu", "--apply", "--authorized"]
        with patch("checks.platform.system", return_value="Windows"):
            self.assertEqual(self.invoke(argv)[0], 2)
        with (
            patch("checks.platform.system", return_value="Linux"),
            patch("checks.Path.read_text", return_value="ID=debian\n"),
        ):
            self.assertEqual(self.invoke(argv)[0], 2)
        with (
            patch("checks.platform.system", return_value="Linux"),
            patch("checks.Path.read_text", return_value="ID=ubuntu\n"),
            patch("checks.os.geteuid", return_value=1000, create=True),
        ):
            self.assertEqual(self.invoke(argv)[0], 2)
        with (
            patch("checks.platform.system", return_value="Linux"),
            patch("checks.Path.read_text", return_value='ID="ubuntu"\n'),
            patch("checks.os.geteuid", return_value=0, create=True),
            patch("checks.execute") as execute,
        ):
            self.assertEqual(self.invoke(argv)[0], 0)
            self.assertEqual(execute.call_count, 2)
        with (
            patch("checks.platform.system", return_value="Linux"),
            patch("checks.Path.read_text", side_effect=OSError),
        ):
            self.assertEqual(self.invoke(argv)[0], 2)

    def test_execution_failures_do_not_leak_output(self):
        with patch("checks.shutil.which", return_value=None):
            with self.assertRaises(checks.CheckError) as caught:
                checks.execute(["missing"], 5)
            self.assertEqual(caught.exception.code, 2)
        with patch("checks.shutil.which", return_value="/tool"):
            for failure in (subprocess.TimeoutExpired("tool", 5), OSError()):
                with (
                    patch("checks.subprocess.run", side_effect=failure),
                    self.assertRaises(checks.CheckError),
                ):
                    checks.execute(["tool"], 5)
            with patch(
                "checks.subprocess.run",
                return_value=subprocess.CompletedProcess(
                    ["tool"], 1, "private-output", "private-output"
                ),
            ):
                with self.assertRaises(checks.CheckError) as caught:
                    checks.execute(["tool"], 5)
                self.assertNotIn("private-output", str(caught.exception))
            with patch(
                "checks.subprocess.run",
                return_value=subprocess.CompletedProcess(["tool"], 0, " ok \n", ""),
            ):
                self.assertEqual(checks.execute(["tool"], 5), "ok")
            with patch(
                "checks.subprocess.run",
                return_value=subprocess.CompletedProcess(
                    ["tool"],
                    2,
                    "",
                    '{"error":"Explicit target authorization required"}',
                ),
            ):
                with self.assertRaises(checks.CheckError) as caught:
                    checks.execute(["tool"], 5, redacted_error=True)
                self.assertEqual(caught.exception.code, 2)
                self.assertEqual(
                    str(caught.exception), "Explicit target authorization required"
                )

    def test_numeric_argument_limits(self):
        for func in (checks.bounded_integer, checks.ssh_port):
            for value in ("zero", "0", "999999"):
                with self.assertRaises(Exception) as caught:
                    func(value)
                self.assertEqual(type(caught.exception).__name__, "ArgumentTypeError")
            self.assertEqual(func("10"), 10)
        for value in ("-1", "nan", "inf", "invalid"):
            with self.assertRaises(argparse.ArgumentTypeError):
                checks.nonnegative_number(value)
        self.assertEqual(checks.nonnegative_number("0"), 0)
        with self.assertRaises(argparse.ArgumentTypeError):
            checks.percentage("100.1")

    def test_launcher_platforms_and_missing_shell(self):
        for system in ("Windows", "Linux", "Darwin"):
            with (
                patch("launcher.platform.system", return_value=system),
                patch("launcher.shutil.which", return_value="/shell"),
                patch("launcher.subprocess.call", return_value=7) as call,
            ):
                self.assertEqual(launcher.main(), 7)
                self.assertEqual(
                    call.call_args.kwargs["env"]["OPS_CHECKS_PYTHON"], sys.executable
                )
        with contextlib.redirect_stderr(io.StringIO()):
            with patch("launcher.platform.system", return_value="Other"):
                self.assertEqual(launcher.main(), 2)
            with patch("launcher.shutil.which", return_value=None):
                self.assertEqual(launcher.main(), 2)
            with (
                patch("launcher.shutil.which", return_value="/shell"),
                patch("launcher.subprocess.call", side_effect=OSError),
            ):
                self.assertEqual(launcher.main(), 2)

    def test_task_pairs_and_powershell_entrypoint(self):
        for path in SCRIPTS.glob("*.ps1"):
            self.assertTrue(path.with_suffix(".sh").is_file())
        if os.name == "nt":
            result = subprocess.run(
                ["pwsh", "-NoProfile", "-File", str(SCRIPTS / "detect-os.ps1")],
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["os"], "Windows")
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "run.py"),
                    "check-url",
                    "--url",
                    "https://example.test",
                ],
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )
            self.assertEqual(result.returncode, 2)


if __name__ == "__main__":
    unittest.main()
