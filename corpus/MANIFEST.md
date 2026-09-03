# Corpus manifest

One entry per document: origin, license (decides redistribution), why it is here.
PDFs and sources are not committed; `skill/pdf-to-pretext/scripts/fetch-arxiv.sh` fetches them.

## corpus/arxiv/2010.15608

- Fetched 2026-09-03: `paper.pdf` (18 pages, LaTeX via dvips + Ghostscript, text layer
  present), e-print source (`source/whenpolyrealzeros1g.tex`, six EPS figures,
  `thebibliography` written by hand, no .bib).
- Class `amsart`; theorem-like environments numbered within sections on one shared counter
  (theorem, corollary, conjecture, principle, question, lemma, proposition, definition);
  `notation` and `remark` unnumbered.  Ten macro definitions, one redefinition.
- Title: "When are the roots of a polynomial real and distinct? A graphical view".
  Author: David W. Farmer (American Institute of Mathematics).  math.CA, math.NT;
  MSC 30C15, 11M26.  Version 1, 2020-10-29; no journal reference, no DOI.
- License: arXiv non-exclusive distribution 1.0 (`metadata-oai.xml`) — NOT redistributable
  by us.  The PDF and source stay out of the repository; a transcription is not to be
  published without the author's permission.
- Role: first document.  Both paths — PDF alone (scored), then PDF+LaTeX.

## corpus/own

Rob's own papers (rights held, LaTeX source, an original PDF and a rebuilt one each).  None yet.

## corpus/round-trip

PreTeXt-authored articles built to PDF and transcribed back; exact keys.  None yet.

## corpus/wild

PDF-only documents, not redistributable, never committed.  None yet.
