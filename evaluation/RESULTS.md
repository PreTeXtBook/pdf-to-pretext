# Results

One row per run.  Scores come from `scripts/compare.py` and the manifest count check;
"side by side" is a human read of sample pages.

| date | document | path (PDF only / PDF+LaTeX) | model | pretext commit | validation | builds | text similarity | items present | side by side | wall time | context tokens | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-09-03 | arXiv 2010.15608 (Farmer) | PDF only | claude-fable-5-1 | 59cd06c1 | clean | html, pdf | 0.949 | 73/73 | pages 1, 2, 6, 7, 8, 12, 16 read; nothing beyond the notes | about 60 min (reconstructed) | about 400,000 (reconstructed) | Table 5.1 prints as Table 5.2 (figure-like blocks share a counter); funding sentence appears once `support` sits inside `author`; AMS-style PDF (`journal name="ams"`) built as `paper-ams.pdf`; second URL of [1] not representable in CSL; run `runs/2026-09-03-farmer-real-roots` |
| 2026-09-03 | corpus/own/scvt (Beezer, submitted version) | PDF only | claude-fable-5-1 | 59cd06c1 | clean | html, pdf, AMS-style pdf | 0.958 | 54/54 | pages 1, 2, 5, 8 read; nothing beyond the notes | 18 min (10 survey, 8 author and build) | about 180,000 | every number coincides; default LaTeX title page hides the author block behind the long `support` (PreTeXt defect, notes.md); `paper-ams.pdf` is the build to read; run `runs/2026-09-03-beezer-scvt` |
