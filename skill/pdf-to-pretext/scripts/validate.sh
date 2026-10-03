#!/bin/bash
# Validate a transcription with PreTeXt's own script: the RELAX NG schema, the survey of
# experimental constructs, and the validation-plus stylesheet.
#
# Usage: validate.sh <project-directory> [<output-directory>]
#   The report goes to <project-directory>/output/validation unless a directory is named.
# For a source not laid out as a project:
#        validate.sh <main.ptx> <publication.ptx> <output-directory>
#
# Writes <name>-validation.txt, and beside it the assembled source its line numbers
# refer to.  Status 0 when all three examinations have no message; otherwise the
# messages are printed and the status is 1.
#
# Validation does not look at whether a cross-reference has a target.  The references
# that have none are listed after it, by count-items.py; they do not change the status,
# since a reference to a section not yet written is expected while authoring.
set -eu
. "$(dirname "$0")/pretext-location.sh"
require_pretext
if [ -d "$1" ]; then
    project_files "$1"
    out=${2:-$1/output/validation}
else
    main=$1
    publication=$2
    out=$3
fi
mkdir -p "$out"
# without a local jing, PreTeXt's validation server does the same examination
method=""
command -v jing > /dev/null 2>&1 || method="-M server"
pretext_script -V full $method -p "$publication" -d "$out" "$main" > "$out/validate.log" 2>&1 || {
    cat "$out/validate.log"
    echo "the validation itself failed; log: $out/validate.log"
    exit 2
}
report=$(ls "$out"/*-validation.txt)
status=0
if [ "$(grep -c '^(no messages' "$report")" -eq 3 ]; then
    echo "validation: clean   (report: $report)"
else
    sed -n '/^Messages: RELAX-NG/,$p' "$report" | grep -v '^$'
    echo "validation: MESSAGES ABOVE   (report: $report)"
    status=1
fi
python3 "$skill/scripts/count-items.py" --references "${report%-validation.txt}-assembled.xml" || true
exit "$status"
