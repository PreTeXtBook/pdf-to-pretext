#!/bin/bash
# Say what this skill needs and whether this machine has it.  setup.sh runs this at its
# end; run setup.sh, not this, on a machine new to the skill.
#
# Usage: check-setup.sh [--quick]
# Status 0 when everything a transcription requires is present, 1 otherwise.  What is
# needed only for some papers (figures) is reported and does not fail.  Unless --quick
# is given it ends with a trial run: the template laid out, validated, and built.
set -u
. "$(dirname "$0")/pretext-location.sh"
missing=0
packages=""
have() { command -v "$1" > /dev/null 2>&1; }
ok() { printf '  ok       %s\n' "$1"; }
bad() { printf '  MISSING  %s\n' "$1"; missing=1; }
note() { printf '  absent   %s\n           %s\n' "$1" "$2"; }
# the name of a system package, for the package manager this machine has
package() {  # arguments: apt name, dnf name, brew name
    if have apt-get; then packages="$packages $1"; elif have dnf; then packages="$packages $2"; else packages="$packages $3"; fi
}

echo "The PDF tools (poppler):"
poppler=1
for tool in pdftotext pdftoppm pdftocairo pdfinfo pdffonts pdfimages pdftohtml; do
    if have "$tool"; then ok "$tool"; else bad "$tool"; poppler=0; fi
done
[ "$poppler" -eq 1 ] || package poppler-utils poppler-utils poppler

echo "PreTeXt (its own script, pretext/pretext):"
if [ -n "$PRETEXT_HOME" ] && [ -f "$PRETEXT_HOME/pretext/pretext" ]; then
    ok "clone at $PRETEXT_HOME, commit $(git -C "$PRETEXT_HOME" rev-parse --short HEAD 2>/dev/null || echo unknown)"
    if "$PRETEXT_PYTHON" "$PRETEXT_HOME/pretext/pretext" -h > /dev/null 2>&1; then
        ok "$PRETEXT_PYTHON runs it"
    else
        bad "a Python that runs it ($PRETEXT_PYTHON does not): run $skill/scripts/setup.sh, which builds one"
    fi
else
    bad "PreTeXt: run $skill/scripts/setup.sh, which gets it"
fi
if have jing; then
    ok "jing (validation)"
else
    note "jing" "validation will go through PreTeXt's validation server instead, which needs the network"
fi
if have xelatex; then
    ok "xelatex (PDF builds)"
else
    bad "xelatex: the PDF build is how a transcription is compared with its original"
    package texlive-xetex texlive-xetex mactex-no-gui
fi

echo "For papers with figures:"
if have mutool; then
    ok "mutool"
else
    note "mutool" "crop-figures.py reads text positions with it"
    package mupdf-tools mupdf mupdf-tools
fi
for module in numpy scipy PIL; do
    if "$PRETEXT_PYTHON" -c "import $module" 2>/dev/null || python3 -c "import $module" 2>/dev/null; then
        ok "Python module $module"
    else
        note "Python module $module" "run $skill/scripts/setup.sh, which installs it"
    fi
done

echo "Network: api.crossref.org and api.datacite.org for looking up DOIs; PreTeXt's HTML"
echo "build downloads some of its static files."

if [ -n "$packages" ]; then
    echo
    echo "Programs for the whole machine cannot be installed from here.  The person whose"
    echo "machine this is can install what is listed above with one command:"
    if have apt-get; then echo "    sudo apt-get install$packages"
    elif have dnf; then echo "    sudo dnf install$packages"
    elif have brew; then echo "    brew install$packages"
    else echo "    (with this system's package manager:$packages)"; fi
fi
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
