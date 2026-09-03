# Transition — state of the project for the next session

Updated 2026-09-03 (set up from the PreTeXt main-checkout session; nothing transcribed yet).

## What exists

- `CLAUDE.md` — the rules and every decision Rob made on 2026-09-03; read it first.
- `skill/pdf-to-pretext/` — `SKILL.md` (three-pass procedure), six reference files
  (`article-elements`, `block-classes` generated from the clone's `entities.ent`,
  `csl-bibliography`, `numbering`, `identifiers`, `macros`), and scripts
  (`fetch-arxiv.sh`, `render-pages.sh`, `extract-text.sh`, `build.sh`, `validate.sh`,
  `compare.py`, `run-header.sh`, `block-classes.py`).  All scripts smoke-tested.
- `pretext/` — a clone of PreTeXtBook/pretext at `59cd06c1` (master, 2026-09-03), not
  committed; `git -C pretext pull` at the start of each session.  Building and validating
  the minimal example through `~/.claude/pretext-venv` from this clone works.
- `templates/main.ptx`, `templates/publication.ptx` — starting points.
- `corpus/arxiv/2010.15608/` — the first document, fetched: `paper.pdf` (18 pages, dvips +
  Ghostscript, text layer present, 8,203 words), `pages/` (150 dpi PNG renderings),
  `paper.txt` (layout text), `source/` (the e-print: `whenpolyrealzeros1g.tex`, six EPS
  figures), `metadata-oai.xml`.  See `corpus/MANIFEST.md` for title, author, license.
- `evaluation/RESULTS.md` (empty table), `notes/decisions-2026-09-03.md`.

## Next steps, in order

1. Pass 1 on 2010.15608 **from the PDF alone** — do not open `source/` — writing
   `runs/2026-09-DD-farmer-real-roots/manifest.md` per `SKILL.md`.  Record the model id
   with `scripts/run-header.sh`.
2. Pass 2 and pass 3 the same way; score the run in `evaluation/RESULTS.md`.
3. A second run using the LaTeX source as the primary text; compare the two.
4. Rewrite `SKILL.md` from what the runs taught; the run notes are the raw material.
5. Rob's own papers into `corpus/own/` (original PDF plus a rebuilt one each) when he
   supplies them; a PreTeXt-authored article into `corpus/round-trip/`.

## Open items

- `compare.py` measures prose only; a display-mathematics comparison against a LaTeX key
  (normalized) is still to be written.
- Figures: the paper's six EPS figures exist in the source, but the PDF-only path must
  crop them from pages with `pdftocairo`; no script for that yet.
- Rob's idea, recorded: surface the original numbers (now XML comments) to readers as
  metadata — a PreTeXt enhancement, later.

## Prompt for a fresh session in this directory

```
Read CLAUDE.md and TRANSITION.md, then skill/pdf-to-pretext/SKILL.md.  We are starting
pass 1 on corpus/arxiv/2010.15608 from the PDF alone: do not open the LaTeX source in
corpus/arxiv/2010.15608/source/, and never consult an HTML rendering of the paper.  Create
the run directory, write its notes header with the model you are, and survey the whole
paper into a manifest as SKILL.md describes.  Ask before creating anything outside runs/.
```
