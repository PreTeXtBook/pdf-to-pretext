#!/bin/bash
# Build a transcription with the pretext/pretext script from the project's clone, then
# check a PDF for lost glyphs.
# Usage: build.sh <main.ptx> <publication.ptx> <format> <output-directory>
#   format: html, latex, pdf, ...   output-directory is created (use a new name if dirty)
# The build log is kept as <output-directory>/build.log.  For a PDF, two checks follow:
# the engine's "Missing character" warnings in the log, and U+FFFD (a glyph the text
# layer could not name) in the PDF.  Either one means a character of the source did not
# reach the page, and the script exits with status 1.
set -eu
project=$(cd "$(dirname "$0")/../../.." && pwd)
mkdir -p "$4"
log=$4/build.log
/home/rob/.claude/pretext-venv/bin/python3 "$project/pretext/pretext/pretext" -vv -c doc \
    -f "$3" -p "$2" -d "$4" "$1" 2>&1 | tee "$log"
status=${PIPESTATUS[0]}
if [ "$status" -ne 0 ]; then
    echo "build failed with status $status; log: $log"
    exit "$status"
fi
if [ "$3" = "pdf" ]; then
    failed=0
    missing=$(grep -c 'Missing character' "$log" || true)
    if [ "$missing" -gt 0 ]; then
        echo "GLYPH CHECK FAILED: $missing 'Missing character' line(s) in $log:"
        grep 'Missing character' "$log" | sort | uniq -c
        failed=1
    fi
    for pdf in "$4"/*.pdf; do
        [ -f "$pdf" ] || continue
        bad=$(pdftotext "$pdf" - | grep -o $'\xef\xbf\xbd' | wc -l)
        if [ "$bad" -gt 0 ]; then
            echo "GLYPH CHECK FAILED: $bad replacement character(s) U+FFFD in the text layer of $pdf"
            failed=1
        fi
    done
    if [ "$failed" -ne 0 ]; then
        exit 1
    fi
    echo "glyph check: no missing characters in the log, no replacement characters in the PDF"
fi
