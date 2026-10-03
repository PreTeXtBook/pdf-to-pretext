# Results

One row per run.  Scores come from `scripts/compare.py` and the manifest count check;
"side by side" is a human read of sample pages.

The similarities in this table were measured with poppler's text extraction.  Since
2026-10-03 the skill reads PDFs with PyMuPDF, which extracts mathematics with less
noise, so the same comparison of the same two PDFs now gives a higher number: Farmer
0.959 (it was 0.954 the same day under poppler), scvt 0.979 (0.962), Burau 0.968 (0.961).
Compare a new row with these, not with the column below.

| date | document | path (PDF only / PDF+LaTeX) | model | pretext commit | validation | builds | text similarity | items present | side by side | wall time | context tokens | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-09-03 | arXiv 2010.15608 (Farmer) | PDF only | claude-fable-5-1 | 59cd06c1 | clean | html, pdf | 0.949 | 73/73 | pages 1, 2, 6, 7, 8, 12, 16 read; nothing beyond the notes | about 60 min (reconstructed) | about 400,000 (reconstructed) | Table 5.1 prints as Table 5.2 (figure-like blocks share a counter); funding sentence appears once `support` sits inside `author`; AMS-style PDF (`journal name="ams"`) built as `paper-ams.pdf`; second URL of [1] not representable in CSL; run `runs/2026-09-03-farmer-real-roots` |
| 2026-09-03 | corpus/own/scvt (Beezer, submitted version) | PDF only | claude-fable-5-1 | 59cd06c1 | clean | html, pdf, AMS-style pdf | 0.958 | 54/54 | pages 1, 2, 5, 8 read; nothing beyond the notes | 18 min (10 survey, 8 author and build) | about 180,000 | every number coincides; default LaTeX title page hides the author block behind the long `support` (PreTeXt defect, notes.md); `paper-ams.pdf` is the build to read; run `runs/2026-09-03-beezer-scvt` |
| 2026-09-16 | arXiv 2607.05283 (Bharathram, Birman, Brendle) | PDF only | claude-fable-5-1 | 0638f0a6 | clean | html, pdf | 0.963 | 21 blocks, 13 proofs, 33 figures with 13 subfigures and 58 panels, 15 displays, 24 entries: all present | every page of the PDF read | 50 min (16 survey, 34 author, build, compare) | about 290,000 | Main Theorem takes 1.1 and shifts two numbers; every other number coincides; PDF needs a two-line patch to `xsl/pretext-latex-common.xsl` (subfigures with `figures/@distinct`, patch in the run directory); the twenty-term display is broken in two; all 58 figure panels recreated in PreFigure (six by measurement, 52 by the general tracer), 45 + 108 + 39 min in three logged efforts; demonstration directory `runs/2026-09-16-burau-demonstration` (AMS PDF hand-compiled with fontspec `no-math`; EPUB has 15 title-markup errors under EPUBCheck); run `runs/2026-09-16-bharathram-burau-faithful` |
