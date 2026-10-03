#!/bin/bash
# Fetch one arXiv paper: its record (with the license), the PDF, and the e-print source.
# Usage: fetch-arxiv.sh <identifier> <directory>        e.g. 2010.15608 papers/2010.15608
# Writes into the directory: metadata-oai.xml, paper.pdf, eprint.bin, source/ (unpacked).
# The license line it prints decides what may be done with a transcription: say it to
# the person you are working for before anything else.  The record is read for the
# license only; nothing else in it belongs in a transcription.
set -eu
identifier=$1
target=$2
agent='pdf-to-pretext fetch'
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
