#!/bin/bash
# Start a transcription: lay out the project, copy the original in, render its pages,
# extract its text, and begin the notes.
#
# Usage: new-transcription.sh <paper.pdf> <project-directory> <model-id>
#   The directory must not exist yet, or be empty.  The model id is what the session
#   knows about itself; it goes in the notes' header.
#
# The layout is the PreTeXt-CLI's (source/, publication/, assets/, generated-assets/,
# output/, project.ptx), so that an author who uses the CLI can carry on from the result.
# The skill itself builds and validates with PreTeXt's own script only.  Its working
# papers are in transcription/.  See references/project-layout.md.
set -eu
. "$(dirname "$0")/pretext-location.sh"
paper=$1
project=$2
model=$3
if [ ! -f "$paper" ]; then
    echo "no such file: $paper" >&2
    exit 2
fi
if [ -e "$project" ] && [ -n "$(ls -A "$project" 2>/dev/null)" ]; then
    echo "$project exists and is not empty; name a new directory" >&2
    exit 2
fi
mkdir -p "$project"
cp -R "$skill/assets/." "$project/"
mv "$project/gitignore" "$project/.gitignore"
mkdir -p "$project/assets" "$project/generated-assets"
work=$project/transcription
cp "$paper" "$work/original.pdf"
"$skill/scripts/render-pages.sh" "$work/original.pdf" "$work/pages" 150
"$skill/scripts/extract-text.sh" "$work/original.pdf" "$work/original.txt"
{
    echo "# Notes"
    echo
    "$skill/scripts/run-header.sh" "$model"
    echo
    echo "## Effort"
    echo
    echo "| pass | started | finished | notes |"
    echo "|---|---|---|---|"
    echo
    echo "## Pass 1"
    echo
} > "$work/notes.md"
echo
echo "project: $project"
pdfinfo "$work/original.pdf" | grep -E '^(Title|Author|Creator|Producer|Pages|Page size):' || true
echo "fonts:   $(pdffonts "$work/original.pdf" 2>/dev/null | tail -n +3 | wc -l)"
echo "images:  $(pdfimages -list "$work/original.pdf" 2>/dev/null | tail -n +3 | wc -l) (embedded pictures; vector drawings are not counted)"
pages=$(pdfinfo "$work/original.pdf" | awk '/^Pages:/ {print $2}')
words=$(wc -w < "$work/original.txt")
echo "text:    $words words on $pages page(s)"
if [ "$words" -lt $((pages * 50)) ]; then
    echo "WARNING: fewer than 50 words a page.  This looks like a scan with no text layer,"
    echo "         which this skill cannot transcribe."
fi
echo "page images: $(ls "$work/pages" | head -1) ... $(ls "$work/pages" | tail -1)"
