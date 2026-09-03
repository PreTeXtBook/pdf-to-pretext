#!/bin/bash
# Validate a transcription (RELAX NG plus validation-plus) with the project's clone.
# Usage: validate.sh <main.ptx> <publication.ptx> <output-directory>
# Writes <name>-validation.txt in the output directory; line numbers refer to the
# assembled file written beside it.
set -eu
project=$(cd "$(dirname "$0")/../../.." && pwd)
mkdir -p "$3"
/home/rob/.claude/pretext-venv/bin/python3 "$project/pretext/pretext/pretext" -V full \
    -p "$2" -d "$3" "$1"
echo "report: $(ls "$3"/*-validation.txt)"
