# Transition — state of the project for the next session

Updated 2026-09-03, end of the first transcription session (PDF-only run of 2010.15608 complete
through pass 3; nothing committed under `runs/`, which is gitignored).

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
- `evaluation/RESULTS.md` (one row, the PDF-only run), `notes/decisions-2026-09-03.md`.

## State of the first run (2026-09-03)

`runs/2026-09-03-farmer-real-roots/` — `manifest.md` (pass 1), `notes.md` (header, policy,
pass-2 findings, raw material for the skill rewrite), `main.ptx` + `sections/*.ptx` +
`publication.ptx`, `external/` (five cropped panels, SVG and PDF each).  Validation clean,
HTML and PDF build without warnings, every `xref` resolves, 73 of 73 manifest items present,
`compare.py` similarity 0.949 (the missing runs are running heads, figure lettering, and
moved text).  Row recorded in `evaluation/RESULTS.md`.  Rob's rulings during the run:
nothing taken from the arXiv record (no date, no MSC codes); Figure 5.1 one composite
image; typos preserved, never corrected.  Builds are under `/tmp/pdf-to-pretext/`
(`farmer-html-2`, `farmer-pdf-2`).

## Next steps, in order

1. Rob reads the built PDF (`/tmp/pdf-to-pretext/farmer-pdf-2/main.pdf`, or rebuild with
   `skill/pdf-to-pretext/scripts/build.sh`) against the original and rules on the three
   known departures: Table 5.1 printed as 5.2, the funding sentence absent from the PDF,
   the second URL of reference [1] dropped.
2. One small fix outside `runs/` awaits Rob's approval: CLAUDE.md names `scripts/` where
   the scripts are `skill/pdf-to-pretext/scripts/`.  (The templates and
   `references/numbering.md` were corrected and committed on 2026-09-03.)
3. The second run on 2010.15608 with the LaTeX source as the primary text; compare with the
   PDF-only run (words, mathematics, and the macro decisions the source makes visible).
4. Rewrite `SKILL.md` from the two runs' notes (`notes.md`, section "For the skill").
5. Rob's own papers into `corpus/own/`; a PreTeXt-authored article into `corpus/round-trip/`.

## Open items

- `compare.py` measures prose only; a display-mathematics comparison against a LaTeX key
  (normalized) is still to be written.
- Figures: cropping with `pdftocairo` works (`-x -y -W -H` plus `-paperw -paperh`, both
  SVG and PDF, `image/@source` without extension); the commands are in the run notes, not
  yet a script.
- A PreTeXt to-do was recorded in the `~/mathbook/claude` memory to-do list (2026-09-03):
  a CSL `biblio` that needs more than one URL.
- Rob's idea, recorded: surface the original numbers (now XML comments) to readers as
  metadata — a PreTeXt enhancement, later.

## Prompt for a fresh session in this directory

```
Read CLAUDE.md and TRANSITION.md, then skill/pdf-to-pretext/SKILL.md.  The PDF-only run of
corpus/arxiv/2010.15608 is complete in runs/2026-09-03-farmer-real-roots; read its notes.md.
Start the second run of the same paper with the LaTeX source in corpus/arxiv/2010.15608/source/
as the primary text and the PDF as the visual check; never consult an HTML rendering.  Create
a new run directory, write its notes header with the model you are, and survey into a
manifest as SKILL.md describes.  Ask before creating anything outside runs/.
```
