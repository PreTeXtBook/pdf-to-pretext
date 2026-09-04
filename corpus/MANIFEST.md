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

Rob's own papers (rights held, LaTeX source, an original PDF and a rebuilt one each).

### corpus/own/scvt

- Added 2026-09-03 from `/home/rob/papers/scvt/`: `paper.pdf` is the submitted version
  (`scvt_expo_submit.pdf`, pdfTeX, dated December 30, 2004, 10 pages, letter, text layer
  present, 4,775 words); `published.pdf` is the version of record, Expositiones
  Mathematicae 24 (2006) 185–194, doi:10.1016/j.exmath.2005.09.003 (Elsevier, Distiller,
  10 pages, received 12 January 2005, revised 11 August 2005; carries Elsevier's copyright
  line); `source/` holds `scvt_expo_submit.tex` (matches `paper.pdf`),
  `scvt_eversion_final.tex` (probably the revised manuscript; unconfirmed), and the one
  figure as a separate Mayura Draw vector file, `scvt9.pdf`.
- Title: "Sylow Subgraphs in Self-Complementary Vertex Transitive Graphs".  Author:
  Robert A. Beezer (University of Puget Sound).  Published version adds MSC 2000 primary
  05C25, secondary 05C75, 20D20, and keywords.
- Rights: the author's.  The PDFs and sources are not committed (`.gitignore`), by the
  general rule; a transcription of the submitted text may be published at Rob's discretion.
  The Elsevier typesetting is not to be redistributed.
- Role: second document.  PDF-only run from `paper.pdf` first (scored against the matching
  source), then PDF+LaTeX; later, a run from `published.pdf` (no key) and a diff of the two
  texts.  Figure 1 is a candidate for a PreFigure recreation.

## corpus/round-trip

PreTeXt-authored articles built to PDF and transcribed back; exact keys.  None yet.

## corpus/wild

PDF-only documents, not redistributable, never committed.  None yet.
