# Results

One row per run.  Scores come from `scripts/compare.py` and the manifest count check;
"side by side" is a human read of sample pages.

| date | document | path (PDF only / PDF+LaTeX) | model | pretext commit | validation | builds | text similarity | items present | side by side | notes |
|---|---|---|---|---|---|---|---|---|---|---|
| 2026-09-03 | arXiv 2010.15608 (Farmer) | PDF only | claude-fable-5-1 | 59cd06c1 | clean | html, pdf | 0.949 | 73/73 | pages 1, 2, 6, 7, 8, 12, 16 read; nothing beyond the notes | Table 5.1 prints as Table 5.2 (figure-like blocks share a counter); funding sentence absent from the PDF (`support` not rendered by the LaTeX article); second URL of [1] not representable in CSL; run `runs/2026-09-03-farmer-real-roots` |
