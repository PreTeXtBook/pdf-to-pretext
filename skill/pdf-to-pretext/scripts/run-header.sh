#!/bin/bash
# Print the header every run's notes.md begins with.  The model id is what the
# session knows about itself; pass it as the argument.
# Usage: run-header.sh <model-id>
set -eu
project=$(cd "$(dirname "$0")/../../.." && pwd)
echo "date: $(date +%Y-%m-%d)"
echo "model: $1"
echo "claude code: $(claude --version 2>/dev/null || echo unknown)"
echo "pretext commit: $(git -C "$project/pretext" rev-parse --short HEAD) ($(git -C "$project/pretext" log -1 --format=%cd --date=short))"
