#!/usr/bin/env sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
if [ "$#" -gt 1 ]; then
    echo "Usage: ./demo.sh ['JSON payload']" >&2
    exit 2
fi
if [ "$#" -eq 1 ]; then
    printf '%s\n' "$1" | "$ROOT/cli.sh" "$ROOT/examples/schema.json"
else
    "$ROOT/cli.sh" "$ROOT/examples/schema.json" < "$ROOT/examples/payload.json"
fi
