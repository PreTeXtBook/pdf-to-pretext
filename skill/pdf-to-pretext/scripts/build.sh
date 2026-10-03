#!/bin/bash
# Build a transcription with PreTeXt's own script (pretext/pretext in a clone of
# PreTeXtBook/pretext), then check a PDF for lost glyphs and overfull boxes.
#
# Usage: build.sh <project-directory> <format> [<output-directory>]
#   format: html, pdf, latex, epub, ...
#   The output goes to <project-directory>/output/web for html, output/print for pdf,
#   output/<format> otherwise, unless an output directory is named.  The directory is
#   created; the script does not empty it, so name a new one for a build from nothing.
# For a source not laid out as a project:
#        build.sh <main.ptx> <publication.ptx> <format> <output-directory>
#
# The build log is kept as build.log in the output directory.  PreTeXt reports some
# faults of the source only there, and exits with status 0: a cross-reference with no
# target is one.  So every line of the log that PreTeXt marks as an error or a warning is
# printed, and an error gives status 1.  PreTeXt's working directories (for a PDF, the
# LaTeX source and its log) are kept beside the output, in <output-directory>-work.
#
# For a PDF, two more checks
# follow: the engine's "Missing character" warnings in the log, and U+FFFD (a glyph the
# text layer could not name) in the PDF.  Either one means a character of the source did
# not reach the page, and the script exits with status 1.  The overfull boxes of the last
# LaTeX pass are then counted, and those wider than 20 points listed, widest first, each
# with the start of its text: look at those on the page.  They do not change the status.
set -eu
. "$(dirname "$0")/pretext-location.sh"
require_pretext
if [ -d "$1" ]; then
    project_files "$1"
    format=$2
    case "$format" in
        html) default=web ;;
        pdf) default=print ;;
        *) default=$format ;;
    esac
    out=${3:-$1/output/$default}
else
    main=$1
    publication=$2
    format=$3
    out=$4
fi
mkdir -p "$out"
out=$(cd "$out" && pwd)
work=$out-work
mkdir -p "$work"
log=$out/build.log
# -vv puts the LaTeX engine's messages in the log, which the checks below read; it also
# makes PreTeXt keep its working directories, so they are sent beside the output
TMPDIR=$work pretext_script -vv -c doc -f "$format" -p "$publication" -d "$out" "$main" 2>&1 | tee "$log"
status=${PIPESTATUS[0]}
if [ "$status" -ne 0 ]; then
    echo "build failed with status $status; log: $log"
    exit "$status"
fi
reported=$(grep -E 'PTX:(ERROR|WARNING|BUG)' "$log" | sed -E 's/^PTX:(ERROR|WARNING|BUG) *: \* //' | sort -u || true)
if [ -n "$reported" ]; then
    echo "PreTeXt reported:"
    printf '%s\n' "$reported" | cut -c1-400
fi
if grep -q -E 'PTX:(ERROR|BUG)' "$log"; then
    echo "BUILD NOT ACCEPTED: PreTeXt reported an error; log: $log"
    exit 1
fi
if [ "$format" = "pdf" ]; then
    failed=0
    missing=$(grep -c 'Missing character' "$log" || true)
    if [ "$missing" -gt 0 ]; then
        echo "GLYPH CHECK FAILED: $missing 'Missing character' line(s) in $log:"
        grep 'Missing character' "$log" | sort | uniq -c
        failed=1
    fi
    for pdf in "$out"/*.pdf; do
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
echo "built: $out"
