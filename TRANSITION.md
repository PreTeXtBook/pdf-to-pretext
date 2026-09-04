# Transition — state of the project for the next session

Updated 2026-09-04, end of the second session.  Two documents transcribed from their PDFs alone
(Farmer, arXiv 2010.15608; Beezer, the Sylow subgraphs preprint), both built into every
PreTeXt output and packaged as demonstration directories.  Rob is letting the project rest.
`runs/` is gitignored, so the runs live only on this machine.

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

## Demonstration directories (2026-09-04)

EPUBCheck 5.3.0 is at `/home/rob/epubcheck/` (installed 2026-09-04, delete the directory
to remove); the system 4.2.6 gives 36 false CSS errors on every PreTeXt EPUB.  Under
5.3.0 the Farmer EPUB has 40 errors, one per numbered display, from MathJax's
`data-mjx-viewBox` attribute; the scvt EPUB is clean.  Filed as PreTeXtBook/pretext issue #3209 (2026-09-04).

`runs/2026-09-04-scvt-demonstration/`: Rob's paper in every output, with the DOI link to
the published version and his permission line; the two LaTeX PDFs are hand-patched
(issues #3207 and #3208) and the XSL-FO PDF needs no patch.  Details in the scvt run notes.

`runs/2026-09-04-farmer-demonstration/`: the Farmer paper in every PreTeXt output behind
`index.html` (source zip, usual PDF, AMS PDF, PDF/UA-1 XSL-FO PDF, HTML, EPUB, Jupyter,
braille).  Meant for pretextbook.org; David Farmer has given permission for the
distribution (Rob, 2026-09-04), and the page says so.  Findings from the builds are in the Farmer run notes.
The clone's `script/mjsre/` now has its node packages installed (needed for EPUB,
braille, and XSL-FO).

## State of the second run (2026-09-03): corpus/own/scvt

`runs/2026-09-03-beezer-scvt/` — Rob's paper "Sylow Subgraphs in Self-Complementary Vertex
Transitive Graphs", the submitted version, PDF only.  `manifest.md`, `notes.md` (with an
effort log per pass), `main.ptx` + `sections/*.ptx`, `publication.ptx`,
`publication-ams.ptx`, `paper-ams.pdf`, `external/` (one figure).  Validation clean; HTML
and PDF build without warnings; 54 of 54 items; every number coincides; `compare.py`
0.958.  Two PreTeXt defects found and recorded in `notes.md`, both in
`xsl/pretext-latex-common.xsl`: `author/support` becomes an unbreakable `\author` row (a
long statement pushes the author block off the page), and `bibinfo/support` renders
nothing.  A third, in `xsl/pretext-latex-classic.xsl` (used by the AMS texstyle): titles go
into the amsthm optional argument unbraced, so a citation in a theorem title breaks the
heading; the two-line fix is `runs/2026-09-03-beezer-scvt/pretext-latex-classic-optional-argument.patch`,
and `paper-ams-patched.pdf` there shows the result.  Filed with the markup proposal as
PreTeXtBook/pretext issue #3207 (2026-09-03); the `support` defects as issue #3208 (2026-09-04).
A missed glyph (a bold Γ that xelatex could not set) led to three skill changes, committed
2026-09-03: `build.sh` fails a PDF build on "Missing character" or U+FFFD, `compare.py`
reports symbols whose count drops in the build, and pass 3 reads every page of a short paper.  `corpus/MANIFEST.md` has the document's entry (uncommitted).

## State of the first run (2026-09-03)

`runs/2026-09-03-farmer-real-roots/` — `manifest.md` (pass 1), `notes.md` (header, policy,
pass-2 findings, raw material for the skill rewrite), `main.ptx` + `sections/*.ptx` +
`publication.ptx`, `publication-ams.ptx` (adds `common/journal/@name="ams"`, the PreTeXt
texstyle for AMS journals), `paper-ams.pdf` (the AMS-style build, amsart, 17 pages),
`external/` (five cropped panels, SVG and PDF each).  Validation clean,
HTML and PDF build without warnings, every `xref` resolves, 73 of 73 manifest items present,
`compare.py` similarity 0.949 (the missing runs are running heads, figure lettering, and
moved text).  Row recorded in `evaluation/RESULTS.md`.  Rob's rulings during the run:
nothing taken from the arXiv record (no date, no MSC codes); Figure 5.1 one composite
image; typos preserved, never corrected.  Builds are under `/tmp/pdf-to-pretext/`
(`farmer-html-2`, `farmer-pdf-2`).

## Next steps, in order

1. Any new document: the prompt at the end of this file.  The skill is still the first
   draft plus the glyph checks; the runs' notes (`notes.md`, sections "For the skill")
   hold what it should say differently.
2. The three PreTeXt issues filed from this work: #3207 (citations in theorem headings, and
   the unbraced optional argument in the classic conversion), #3208 (`support` in the
   LaTeX article), #3209 (MathJax's `data-mjx-viewBox` in EPUB).  Until #3207 and #3208
   are fixed, the LaTeX PDFs of a paper with citations in headings or a long funding note
   need the hand patches described in the scvt run notes.  Not filed: `-c prefigure -f
   tactile` fails in `pretext.py` on a missing `output/tactile/` directory with prefig 0.7.4;
   the braille conversion's errors for references to numbered equations.
3. For scvt: the PDF+LaTeX run (`source/scvt_expo_submit.tex` matches `paper.pdf`) and the
   diff against the PDF-only run; then a run from `published.pdf` (no key) and a diff of the
   submitted and revised texts.
4. For Farmer: the PDF+LaTeX run, same comparison.
5. Rewrite `SKILL.md` from the runs' notes.
6. One small fix outside `runs/` still awaits Rob's approval: CLAUDE.md names `scripts/`
   where the scripts are `skill/pdf-to-pretext/scripts/`.

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

For a paper that is a local PDF (with or without LaTeX source):

```
Read CLAUDE.md and TRANSITION.md, then skill/pdf-to-pretext/SKILL.md.  Run
`git -C pretext pull` first.  The new document is the PDF at <path>; its LaTeX source, if
any, is at <path>.  Put it in corpus/<own or wild>/<short-name>/ with the usual layout
(paper.pdf, pages/, paper.txt, source/ unopened), add its entry to corpus/MANIFEST.md, and
tell me the license situation before anything else.  Then pass 1 from the PDF alone: create
the run directory, write its notes header with the model you are, start the effort log, and
survey the whole paper into a manifest as SKILL.md describes.  Do not open the LaTeX source
and never consult an HTML rendering.  Ask before creating anything outside runs/ other
than the corpus directory.
```

For an arXiv paper, replace the second and third sentences with:

```
The new document is arXiv <identifier>; fetch it with skill/pdf-to-pretext/scripts/fetch-arxiv.sh,
add its entry to corpus/MANIFEST.md, and tell me the license situation before anything else.
```

Then, when pass 1 is done: "your decisions were good, on to pass 2" (or the corrections
first).  Pass 2 runs through the pass-3 checks and ends with a results row.
