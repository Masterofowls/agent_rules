#!/bin/sh
set -eu
root=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
python=${OPS_CHECKS_PYTHON:-python3}
if ! command -v "$python" >/dev/null 2>&1; then
    printf '%s\n' 'Python 3.10+ is required' >&2
    exit 2
fi
exec "$python" "$root/checks.py" "$@"
