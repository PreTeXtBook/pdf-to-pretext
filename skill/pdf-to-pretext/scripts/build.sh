#!/bin/bash
# Build a transcription with the pretext/pretext script from the project's clone, then
# check a PDF for lost glyphs.
# Usage: build.sh <main.ptx> <publication.ptx> <format> <output-directory>
#   format: html, latex, pdf, ...   output-directory is created (use a new name if dirty)
# The build log is kept as <output-directory>/build.log.  For a PDF, two checks follow:
# the engine's "Missing character" warnings in the log, and U+FFFD (a glyph the text
# layer could not name) in the PDF.  Either one means a character of the source did not
# reach the page, and the script exits with status 1.  The overfull boxes of the last
# LaTeX pass are then counted, and those wider than 20 points listed, widest first, each
# with the start of its text: look at those on the page.  They do not change the status.
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
    # every LaTeX pass repeats the overfull boxes; only the last pass describes the PDF
    limit=20
    start=$(grep -n '^This is .*TeX, Version' "$log" | tail -1 | cut -d: -f1)
    pass=$(tail -n +"${start:-1}" "$log")
    total=$(printf '%s\n' "$pass" | grep -c '^Overfull \\hbox' || true)
    wide=$(printf '%s\n' "$pass" | awk -v limit="$limit" '
        /^Overfull \\hbox \(/ {
            width = $3; sub(/^\(/, "", width); sub(/pt$/, "", width)
            where = $0; sub(/^.*too wide\) /, "", where)
            if (width + 0 > limit) { getline text; printf "%9.1f pt  %s: %s\n", width, where, substr(text, 1, 70) }
        }' | sort -rn)
    echo "overfull boxes in the last LaTeX pass: $total; wider than $limit pt: $(printf '%s' "$wide" | grep -c . || true)"
    if [ -n "$wide" ]; then
        printf '%s\n' "$wide"
    fi
    if [ "$failed" -ne 0 ]; then
        exit 1
    fi
    echo "glyph check: no missing characters in the log, no replacement characters in the PDF"
fi
