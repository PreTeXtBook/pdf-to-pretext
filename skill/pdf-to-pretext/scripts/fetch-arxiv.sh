#!/bin/bash
# Fetch one arXiv paper into corpus/arxiv/<identifier>: metadata (with license),
# the PDF, and the e-print source, unpacked.
# Usage: fetch-arxiv.sh <identifier>          e.g. 2010.15608
set -eu
identifier=$1
project=$(cd "$(dirname "$0")/../../.." && pwd)
target=$project/corpus/arxiv/$identifier
agent='pdf-to-pretext corpus fetch'
mkdir -p "$target/source"
cd "$target"
curl -s -L -A "$agent" -o metadata-oai.xml \
    "https://export.arxiv.org/oai2?verb=GetRecord&identifier=oai:arXiv.org:$identifier&metadataPrefix=arXiv"
curl -s -L -A "$agent" -o paper.pdf "https://arxiv.org/pdf/$identifier"
curl -s -L -A "$agent" -o eprint.bin "https://arxiv.org/e-print/$identifier"
cd source
cp ../eprint.bin eprint.gz
gunzip -f eprint.gz
if tar -tf eprint > /dev/null 2>&1; then
    tar -xf eprint
else
    mv eprint main.tex
fi
cd ..
echo "license: $(grep -o '<license>[^<]*</license>' metadata-oai.xml | sed 's/<[^>]*>//g')"
echo "pages:   $(pdfinfo paper.pdf | awk '/^Pages/ {print $2}')"
echo "source:  $(ls source | tr '\n' ' ')"
