#!/bin/bash
# Say what this skill needs and whether this machine has it.
# Usage: check-setup.sh
# Status 0 when everything a transcription requires is present, 1 otherwise.  What is
# needed only for some papers (figures) or some outputs is reported and does not fail.
set -u
. "$(dirname "$0")/pretext-location.sh"
missing=0
have() { command -v "$1" > /dev/null 2>&1; }
ok() { printf '  ok       %s\n' "$1"; }
bad() { printf '  MISSING  %s\n           %s\n' "$1" "$2"; missing=1; }
note() { printf '  absent   %s\n           %s\n' "$1" "$2"; }

echo "The PDF tools (poppler):"
for tool in pdftotext pdftoppm pdftocairo pdfinfo pdffonts pdfimages pdftohtml; do
    if have "$tool"; then ok "$tool"; else bad "$tool" "install poppler (poppler-utils on Debian and Ubuntu, poppler with Homebrew)"; fi
done

echo "PreTeXt (its own script; the PreTeXt-CLI is not used):"
if [ -n "$PRETEXT_HOME" ] && [ -f "$PRETEXT_HOME/pretext/pretext" ]; then
    ok "clone at $PRETEXT_HOME, commit $(git -C "$PRETEXT_HOME" rev-parse --short HEAD 2>/dev/null || echo unknown)"
    if "$PRETEXT_PYTHON" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)' 2>/dev/null; then
        ok "$PRETEXT_PYTHON is Python 3.10 or newer"
    else
        bad "Python 3.10 or newer as $PRETEXT_PYTHON" "set PRETEXT_PYTHON in $skill/config.local"
    fi
    if "$PRETEXT_PYTHON" "$PRETEXT_HOME/pretext/pretext" -h > /dev/null 2>&1; then
        ok "the script runs"
    else
        bad "the script's Python packages" "make a virtual environment, run: pip install -r $PRETEXT_HOME/pretext/requirements.txt  and name its python3 as PRETEXT_PYTHON in $skill/config.local"
    fi
else
    bad "a clone of PreTeXtBook/pretext" "git clone https://github.com/PreTeXtBook/pretext  then write two lines in $skill/config.local:
             PRETEXT_HOME=/where/the/clone/is
             PRETEXT_PYTHON=/a/python3/with/the/clone's/pretext/requirements.txt/installed"
fi
if have jing; then ok "jing (validation)"; else bad "jing" "the RELAX NG validator (package jing on Debian and Ubuntu, jing-trang with Homebrew)"; fi
if have xelatex; then ok "xelatex (PDF builds)"; else bad "xelatex" "a TeX distribution with xelatex; the PDF build is how a transcription is compared with the original"; fi

echo "For papers with figures:"
if have mutool; then ok "mutool"; else note "mutool" "MuPDF's tools (mupdf-tools); crop-figures.py reads text positions with it"; fi
for module in numpy scipy PIL; do
    if python3 -c "import $module" 2>/dev/null; then ok "python3 module $module"; else note "python3 module $module" "pip install numpy scipy pillow; the figure scripts use them"; fi
done

echo "Network: api.crossref.org and api.datacite.org for looking up DOIs; PreTeXt's HTML"
echo "build downloads some of its static files."

if [ "$missing" -ne 0 ]; then
    echo "Not ready: see MISSING above."
    exit 1
fi
if [ "${1:-}" = "--quick" ]; then
    echo "Ready (the trial run was skipped)."
    exit 0
fi
echo "Trial run: the template is laid out, validated, and built to HTML and to PDF."
trial=$(mktemp -d)
printf '%%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj 2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj 3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 200 200]>>endobj\ntrailer<</Root 1 0 R>>\n' > "$trial/blank.pdf"
if "$skill/scripts/new-transcription.sh" "$trial/blank.pdf" "$trial/project" trial > "$trial/new.log" 2>&1 \
    && "$skill/scripts/validate.sh" "$trial/project" > "$trial/validate.log" 2>&1 \
    && "$skill/scripts/build.sh" "$trial/project" html > "$trial/html.log" 2>&1 \
    && "$skill/scripts/build.sh" "$trial/project" pdf > "$trial/pdf.log" 2>&1; then
    echo "  ok       laid out, validated clean, built: $trial/project/output"
    echo "Ready."
else
    echo "  FAILED   the logs are in $trial (new.log, validate.log, html.log, pdf.log)"
    exit 1
fi
