#!/bin/bash
# Build a transcription with the pretext/pretext script from the project's clone.
# Usage: build.sh <main.ptx> <publication.ptx> <format> <output-directory>
#   format: html, latex, pdf, ...   output-directory is created (use a new name if dirty)
set -eu
project=$(cd "$(dirname "$0")/../../.." && pwd)
mkdir -p "$4"
/home/rob/.claude/pretext-venv/bin/python3 "$project/pretext/pretext/pretext" -vv -c doc \
    -f "$3" -p "$2" -d "$4" "$1"
