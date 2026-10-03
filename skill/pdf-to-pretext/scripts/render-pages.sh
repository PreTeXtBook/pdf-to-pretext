#!/bin/bash
# Render every page of a PDF to PNG for reading; 150 dpi is enough for mathematics.
# Usage: render-pages.sh <paper.pdf> <output-directory> [dpi]
# The files are page-01.png, page-02.png, ... (three digits from 100 pages on).
set -eu
. "$(dirname "$0")/pretext-location.sh"
"$PRETEXT_PYTHON" "$skill/scripts/pdftool.py" render "$1" "$2" "${3:-150}"
