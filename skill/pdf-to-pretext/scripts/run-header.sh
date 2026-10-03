#!/bin/bash
# Print the header every transcription's notes.md begins with.  The model id is what the
# session knows about itself; pass it as the argument.
# Usage: run-header.sh <model-id>
set -eu
. "$(dirname "$0")/pretext-location.sh"
require_pretext
echo "date: $(date +%Y-%m-%d)"
echo "model: $1"
echo "claude code: $(claude --version 2>/dev/null || echo unknown)"
echo "pretext commit: $(git -C "$PRETEXT_HOME" rev-parse --short HEAD) ($(git -C "$PRETEXT_HOME" log -1 --format=%cd --date=short))"
