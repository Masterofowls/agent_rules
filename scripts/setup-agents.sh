#!/bin/sh
set -eu
root=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
python=${AGENT_SETUP_PYTHON:-python3}
if ! command -v "$python" >/dev/null 2>&1; then
    printf '%s\n' 'Python 3.10+ is required' >&2
    exit 2
fi
exec "$python" "$root/setup_agents.py" "$@"
