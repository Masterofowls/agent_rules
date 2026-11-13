#!/bin/sh
exec sh "$(dirname -- "$0")/run.sh" check-disk "$@"
