"""OS-aware launcher for the paired operational checks."""

import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parent
    system = platform.system()
    if system == "Windows":
        shell = shutil.which("pwsh") or shutil.which("powershell")
        args = ["-NoProfile", "-File", str(root / "run.ps1")]
    elif system in ("Linux", "Darwin"):
        shell = shutil.which("sh")
        args = [str(root / "run.sh")]
    else:
        print("Unsupported operating system", file=sys.stderr)
        return 2
    if not shell:
        print("Required shell unavailable", file=sys.stderr)
        return 2
    env = os.environ.copy()
    env["OPS_CHECKS_PYTHON"] = sys.executable
    try:
        return subprocess.call([shell, *args, *sys.argv[1:]], env=env)
    except OSError:
        print("Could not launch checks", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
