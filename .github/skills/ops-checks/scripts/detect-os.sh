#!/bin/sh
exec sh "$(dirname -- "$0")/run.sh" detect-os "$@"
