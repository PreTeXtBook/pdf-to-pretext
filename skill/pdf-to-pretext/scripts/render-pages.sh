#!/bin/bash
# Render every page of a PDF to PNG for reading; 150 dpi is enough for mathematics.
# Usage: render-pages.sh <paper.pdf> <output-directory> [dpi]
set -eu
pdf=$1
outdir=$2
dpi=${3:-150}
mkdir -p "$outdir"
pdftoppm -r "$dpi" -png "$pdf" "$outdir/page"
ls "$outdir" | wc -l | xargs echo "pages rendered:"
