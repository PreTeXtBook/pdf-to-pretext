#!/bin/bash
# Extract the text layer of a PDF, layout preserved, for the words of the paper.
# Usage: extract-text.sh <paper.pdf> <output.txt>
set -eu
pdftotext -layout "$1" "$2"
wc -w "$2"
