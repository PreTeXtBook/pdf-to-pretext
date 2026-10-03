#!/bin/bash
# Extract the text layer of a PDF, set out as on the page, for the words of the paper.
# Usage: extract-text.sh <paper.pdf> <output.txt>
set -eu
. "$(dirname "$0")/pretext-location.sh"
"$PRETEXT_PYTHON" "$skill/scripts/pdftool.py" text "$1" --layout > "$2"
wc -w "$2"
