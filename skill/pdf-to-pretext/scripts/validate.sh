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
# refer to.  The messages are printed.  Status 0 when all three examinations have no
# message, 1 otherwise.
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
pretext_script -V full -p "$publication" -d "$out" "$main" > "$out/validate.log" 2>&1 || {
    cat "$out/validate.log"
    echo "the validation itself failed; log: $out/validate.log"
    exit 2
}
report=$(ls "$out"/*-validation.txt)
sed -n '/^Messages: RELAX-NG/,$p' "$report" | grep -v '^$'
echo "report: $report"
if [ "$(grep -c '^(no messages' "$report")" -eq 3 ]; then
    echo "validation: clean"
else
    echo "validation: MESSAGES ABOVE"
    exit 1
fi
