#!/bin/bash
# The checks that need no model.  Run before proposing a change, and after PreTeXt moves.
#
# Usage: tests/run.sh
#
#   1. skill/pdf-to-pretext/scripts/check-setup.sh: the tools are present, and the skill's
#      template lays out, validates, and builds to HTML and PDF.
#   2. Every round-trip case in corpus/round-trip: its pictures compile, its source
#      validates with no message, it builds to HTML and to PDF with the glyph check, and
#      the two comparison scripts find it identical to itself.
#   3. Every worked example in examples/ validates and builds.
#   4. crop-figures.py puts the 58 figure panels of arXiv 2607.05283 where they were, if
#      that paper has been fetched into corpus/arxiv/2607.05283 (it is not in the
#      repository; the specification and the boxes, in tests/crop-figures, are).
#
# The PDF each case builds (corpus/round-trip/<case>/output/print/main.pdf) is the input
# for scoring the skill itself, which takes a model and is done by hand: CONTRIBUTING.md.
# Status 0 when every check passes.
set -u
root=$(cd "$(dirname "$0")/.." && pwd)
scripts=$root/skill/pdf-to-pretext/scripts
failures=0
fail() { echo "  FAILED   $1"; failures=$((failures + 1)); }

echo "== setup, and the template"
if ! "$scripts/check-setup.sh"; then
    fail "check-setup.sh"
    echo "Nothing else can be checked until that passes."
    exit 1
fi

for case in "$root"/corpus/round-trip/*/; do
    case=${case%/}
    name=$(basename "$case")
    [ -f "$case/source/main.ptx" ] || continue
    echo "== $name"
    log=$case/output/checks
    mkdir -p "$log"
    if [ -d "$case/figures" ]; then
        work=$(mktemp -d)
        mkdir -p "$case/assets"
        for picture in "$case"/figures/*.tex; do
            stem=$(basename "$picture" .tex)
            if pdflatex -interaction=batchmode -output-directory "$work" "$picture" > /dev/null 2>&1 \
                && cp "$work/$stem.pdf" "$case/assets/$stem.pdf" \
                && pdftocairo -svg "$case/assets/$stem.pdf" "$case/assets/$stem.svg"; then
                :
            else
                fail "picture $stem did not compile (log in $work)"
            fi
        done
        echo "  ok       pictures: $(ls "$case"/figures/*.tex | wc -l)"
    fi
    if "$scripts/validate.sh" "$case" > "$log/validate.txt" 2>&1; then
        echo "  ok       validates with no message"
    else
        fail "validation: $log/validate.txt"
        continue
    fi
    if "$scripts/build.sh" "$case" html > "$log/html.txt" 2>&1 && ! grep -q 'PTX:WARNING\|PTX:ERROR' "$log/html.txt"; then
        echo "  ok       builds to HTML with no warning"
    else
        fail "HTML build: $log/html.txt"
    fi
    if "$scripts/build.sh" "$case" pdf > "$log/pdf.txt" 2>&1; then
        echo "  ok       builds to PDF, $(pdfinfo "$case/output/print/main.pdf" | awk '/^Pages/ {print $2}') page(s), glyph check clean; $(grep '^overfull boxes' "$log/pdf.txt")"
    else
        fail "PDF build: $log/pdf.txt"
        continue
    fi
    python3 "$root/tests/compare-transcriptions.py" "$case/source/main.ptx" "$case/source/main.ptx" > "$log/self.txt" 2>&1
    if grep -q '^STRUCTURE .*identical' "$log/self.txt" && grep -q '^WORDS .*identical' "$log/self.txt" \
        && grep -q 'still different: 0; in one document only: 0' "$log/self.txt"; then
        echo "  ok       compare-transcriptions.py: identical to itself ($(grep -o '^FORMULAS *[0-9]*' "$log/self.txt" | awk '{print $2}') formulas)"
    else
        fail "compare-transcriptions.py against itself: $log/self.txt"
    fi
    if python3 "$scripts/compare.py" "$case/output/print/main.pdf" "$case/output/print/main.pdf" 2> /dev/null | grep -q '^similarity: 1.000'; then
        echo "  ok       compare.py: similarity 1.000 with itself"
    else
        fail "compare.py against itself"
    fi
done

for example in "$root"/examples/*/; do
    example=${example%/}
    [ -f "$example/source/main.ptx" ] || continue
    echo "== example $(basename "$example")"
    log=$example/output/checks
    mkdir -p "$log"
    if "$scripts/validate.sh" "$example" > "$log/validate.txt" 2>&1 \
        && "$scripts/build.sh" "$example" html > "$log/html.txt" 2>&1 \
        && "$scripts/build.sh" "$example" pdf > "$log/pdf.txt" 2>&1; then
        echo "  ok       validates, builds to HTML and to PDF ($(pdfinfo "$example/output/print/main.pdf" | awk '/^Pages/ {print $2}') pages), glyph check clean"
    else
        fail "example: $log"
    fi
done

echo "== crop-figures.py on the 58 panels of arXiv 2607.05283"
paper=$root/corpus/arxiv/2607.05283/paper.pdf
if [ -f "$paper" ]; then
    work=$(mktemp -d)
    cp "$root/tests/crop-figures/2607.05283-figure-spec.json" "$work/figure-spec.json"
    if python3 "$scripts/crop-figures.py" "$paper" "$work/figure-spec.json" "$work/assets" > "$work/crop.log" 2>&1 \
        && python3 -c 'import json, sys; sys.exit(0 if json.load(open(sys.argv[1])) == json.load(open(sys.argv[2])) else 1)' \
            "$work/crop-work/figure-boxes.json" "$root/tests/crop-figures/2607.05283-figure-boxes.json"; then
        echo "  ok       every box where it was"
    else
        fail "crop-figures.py: boxes moved, or the script failed ($work)"
    fi
else
    echo "  skipped  the paper is not here; fetch it (it is CC BY 4.0) with"
    echo "           skill/pdf-to-pretext/scripts/fetch-arxiv.sh 2607.05283 corpus/arxiv/2607.05283"
fi

echo
if [ "$failures" -eq 0 ]; then
    echo "All checks passed."
else
    echo "$failures check(s) FAILED."
    exit 1
fi
