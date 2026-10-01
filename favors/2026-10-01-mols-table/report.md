# MOLS table: PDF to a Python list

2026-10-01.  Converted by Claude (`claude-opus-5-5`, Claude Code 2.1.286) for Rob Beezer.
A one-off conversion, not a transcription run.

## The request

> Here is the file I want converted. You can relabel infinity to -1. I need to be able
> to read it in python so I was thinking just having it a list (10 000 entries long).

## Files in this directory

| File | What it is |
|---|---|
| `MOLS_table.pdf` | The source as supplied: ten pages, numbered 176–185, running heads "Mutually Orthogonal Latin Squares (MOLS)  III.3" and "III.3.6  MOLS of Side n ≤ 10,000". |
| `mols_table.py` | The result: one list, `MOLS`, of 10,000 integers. |
| `report.md` | This report. |

## The result

`MOLS[n]` is the table entry for side `n`, for 0 ≤ n < 10000.  The table prints ∞ for
n = 0 and n = 1; those two entries are `-1`.  No other entry is negative.

```python
from mols_table import MOLS

len(MOLS)     # 10000
MOLS[10]      # 2
MOLS[9973]    # 9972
```

In the file, each line of the list is one row of the printed table (twenty entries), and
a comment at the end of the line gives the side of the row's first entry.

## How it was checked

1. **Two extractions agree.**  The numbers were taken from the text of the PDF twice:
   once row by row, and once by placing every number in its column from its position on
   the page.  The two agree on all 10,000 entries.  Every row has exactly twenty entries
   and all 500 row labels (0, 20, …, 9980) are present.
2. **The mathematics holds.**  All 1,280 prime powers below 10,000 have the entry n − 1,
   and no other n does.  No entry exceeds n − 1, and none falls below the MacNeish bound
   (the smallest prime-power factor of n, less one).
3. **Read against the page images.**  33 rows (660 entries) were read from rendered pages
   and compared with the list: rows 0–220 on page 176, rows 5400–5600 on page 181, and
   rows 9800–9980 on page 185.  No differences.

The remaining 9,340 entries were not read from the images; they rest on checks 1 and 2.

## What the list does not carry

- The printed table sets some entries in italic, and the entries of three or more digits
  in small type.  A plain list drops both.  The ten pages supplied include no legend, so
  what the italics mean is not known from this source.
- The docstring in `mols_table.py` describes the entries as lower bounds on N(n), the
  maximum number of mutually orthogonal Latin squares of side n.  That description is the
  converter's; the ten pages carry only running heads, no caption.

## Effort

About two minutes of machine time, 14 tool calls, roughly 75,000 tokens, one session, no
subagents.  Tools: `pdftotext` (layout and word-position modes) for the numbers,
`pdftocairo` for the page images, Python for the comparisons.
