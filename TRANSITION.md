# Transition — state of the project for the next session

Updated 2026-10-03: an experiment, one paper transcribed from the PDF alone and again from
its LaTeX, with corrections and additions to the skill that came of it (the section after
"What exists").  Before that, 2026-09-26: every output of the third document rebuilt on the
clone at `20d10545` for Rob to publicize (below).  Three documents transcribed from their PDFs
alone (Farmer, arXiv 2010.15608; Beezer, the Sylow subgraphs preprint; Bharathram, Birman,
Brendle, arXiv 2607.05283), each built into every PreTeXt output and packaged as a
demonstration directory; the third has all 58 figure panels as PreFigure diagrams, with
tactile PDFs.  `runs/` is gitignored, so the runs live only on this machine.

A local server was serving the third demonstration at `http://127.0.0.1:8020/` from
`runs/2026-09-16-burau-demonstration/` (`python3 -m http.server 8020 --bind 127.0.0.1` run in
that directory); it does not survive a restart, and the explorable diagrams need a server,
not a `file:` URL.

## What exists

- `CLAUDE.md` — the rules and every decision Rob made on 2026-09-03; read it first.
- `skill/pdf-to-pretext/` — `SKILL.md` (three-pass procedure), six reference files
  (`article-elements`, `block-classes` generated from the clone's `entities.ent`,
  `csl-bibliography`, `numbering`, `identifiers`, `macros`), and scripts
  (`fetch-arxiv.sh`, `render-pages.sh`, `extract-text.sh`, `build.sh`, `validate.sh`,
  `compare.py`, `run-header.sh`, `block-classes.py`, `lookup-dois.py`, and the figure
  scripts under Open items).  All scripts smoke-tested.
- `pretext/` — a clone of PreTeXtBook/pretext at `bf795ab1` (master, 2026-10-02), not
  committed; `git -C pretext pull --ff-only` before every new task (CLAUDE.md).  Building
  and validating the minimal example through `~/.claude/pretext-venv` from this clone works.
- `templates/main.ptx`, `templates/publication.ptx` — starting points.
- `corpus/arxiv/2010.15608/` — the first document, fetched: `paper.pdf` (18 pages, dvips +
  Ghostscript, text layer present, 8,203 words), `pages/` (150 dpi PNG renderings),
  `paper.txt` (layout text), `source/` (the e-print: `whenpolyrealzeros1g.tex`, six EPS
  figures), `metadata-oai.xml`.  See `corpus/MANIFEST.md` for title, author, license.
- `evaluation/RESULTS.md` (one row, the PDF-only run), `notes/decisions-2026-09-03.md`,
  `notes/2026-10-03-pdf-only-versus-latex.md` (the experiment's report, next section).
- `favors/` — one-off conversions done as favors, not runs (new 2026-10-01).
  `favors/2026-10-01-mols-table/`: a ten-page table of MOLS bounds (n below 10,000)
  converted to a Python list.  Only `report.md` remains.  The source `MOLS_table.pdf` and
  the result `mols_table.py`, which the report describes, were never tracked, because Rob
  judges we have no rights to the data, and were deleted at his word on 2026-10-03.

## The experiment of 2026-10-03: one paper from the PDF alone, then from its LaTeX

Rob's test of the process on arXiv 2610.02127v1 (Niles-Weed, Sadovsky, Shkrob, 12 pages, no
figures).  Not an open license and the authors are not known to him, so by his instruction
there is no corpus entry and no results row, and nothing of the paper is in the repository.
The report is: `notes/2026-10-03-pdf-only-versus-latex.md`.  The rest is on this machine
only, in `runs/2026-10-03-vector-balancing-pdf-only/`, `-latex/`, and `-experiment/` (the
diffs, the comparison script, the effort scripts).  Never commit the two effort scripts:
they hold the session's transcript file name, which is a session identifier.

- **Result.**  The PDF-only transcription has no error of words or of mathematics against
  the one made from the source by script: same structure, same words, 301 of 302 paired
  formulas equivalent after eight spelling equivalences.  About 14 minutes for the
  PDF-only run and 8 for the LaTeX one, which reused the first run's identifiers and DOIs.
- **Rob's rulings.**  The skill gets no section for transcribing from LaTeX ("let's NOT do
  this"); the report's section "For a LaTeX path, later" holds what it would have said and
  the questions left open (a printed date that is `\today`, the case of the bibliography,
  the authors' labels as identifiers, normalizing the authors' spelling).  Read it before
  any PDF+LaTeX run of the corpus papers.
- **Changes to the skill, all with his approval.**  `templates/main.ptx` has the
  `titlepage` the schema requires (the template failed validation without it).
  `references/article-elements.md`: an article has no `acknowledgement`; an unnumbered
  Acknowledgements section is a titled `paragraphs` closing the last section.  `SKILL.md`: fonts (`pdftohtml -xml`)
  and code points settle look-alikes; an upright remark ends only by vertical space, a
  judgment for the manifest.  `scripts/lookup-dois.py` asks Crossref and then DataCite
  (arXiv, Dagstuhl); `references/csl-bibliography.md` says so.  `build.sh` lists the
  overfull boxes of the last LaTeX pass wider than 20 points.  `compare.py` prints a second
  similarity, for the text before the reference list.

## Demonstration directories (2026-09-04)

EPUBCheck 5.3.0 is at `/home/rob/epubcheck/` (installed 2026-09-04, delete the directory
to remove); the system 4.2.6 gives 36 false CSS errors on every PreTeXt EPUB.  Under
5.3.0 the Farmer EPUB has 40 errors, one per numbered display, from MathJax's
`data-mjx-viewBox` attribute; the scvt EPUB is clean.  Filed as PreTeXtBook/pretext issue #3209 (2026-09-04).

`runs/2026-09-04-scvt-demonstration/`: Rob's paper in every output, with the DOI link to
the published version and his permission line.  Rebuilt 2026-09-23 from the clone at
`156cd7f7`, where #3207 and #3208 are fixed, so every PDF is now the pipeline's own,
unpatched.  Details in the scvt run notes.

`runs/2026-09-04-farmer-demonstration/`: the Farmer paper in every PreTeXt output behind
`index.html` (source zip, usual PDF, AMS PDF, PDF/UA-1 XSL-FO PDF, HTML, EPUB, Jupyter,
braille).  Meant for pretextbook.org; David Farmer has given permission for the
distribution (Rob, 2026-09-04), and the page says so.  Findings from the builds are in the Farmer run notes.
The clone's `script/mjsre/` now has its node packages installed (needed for EPUB,
braille, and XSL-FO).

## State of the third run (2026-09-16): corpus/arxiv/2607.05283, PDF only, complete

`runs/2026-09-16-bharathram-burau-faithful/` — Bharathram, Birman, Brendle, "The Burau
representation is faithful for n = 4" (arXiv 2607.05283v2, 28 pages, CC BY 4.0, so the first
redistributable document).  `manifest.md`, `notes.md` (effort log per pass, findings for the
skill), `errata.md` (what looks wrong in the arXiv version, none of it changed), `main.ptx`
+ `sections/*.ptx`, `publication.ptx`, `publication-ams.ptx`, `external/` (58 panels, SVG
and PDF each), `figure-spec.json` + `figure-boxes.json` (the crop script's input and
output), `paper.pdf` (the usual build) and `paper-ams-patched.pdf`.  Validation clean;
HTML without warnings; PDF 30 pages, glyph check clean; every page read side by side;
`compare.py` 0.963; every item present.  Rob's rulings: the Main Theorem is numbered
(1.1, shifting Corollary 1.1 and Proposition 1.2 by one); `creator` + `origins` for
attributions; figures `distinct="yes"`; titles stored without their final period because
PreTeXt supplies it (a general rule now, in `SKILL.md`); the twenty-term display broken in
two.  `corpus/MANIFEST.md` has the entry; `evaluation/RESULTS.md` the row.

Every figure panel, all 58, is a PreFigure diagram (2026-09-18, Rob's request, in two
efforts logged separately in the run notes): Figures 1.1, 2.1, and 3.1 measured and traced
by hand-written scripts, the other 52 panels vectorized by the general tracer
`skill/pdf-to-pretext/scripts/trace-figure.py` (curves by color, arrowheads, dots, dashes,
fills, bands, labels from the text layer) and a generator; `prefigure-work/` in the run
directory has both pipelines, the traces, the PreFigure sources, and the comparison sheets.
The small losses of the first pass (arrowheads, dotted tails, a dotted leader, a kink, two
marked points) were fixed on 2026-09-19; the run notes list what each needed.  Tactile PDFs of all 58 diagrams exist (2026-09-19): `generated/prefigure/tactile/`,
the demonstration's `tactile/index.html`, and `runs/2026-09-16-burau-tactile/` with its zip
for embossing.  Two tool defects met on the way, both recorded in the run notes and not
filed: PreFigure's tactile mode needs integer `thickness` (an `int()` in `diagram.py`), and
the script's `-c prefigure -f tactile` fails because only `-f all` creates `output/tactile/`
(filed as PreTeXtBook/pretext issue #3221 on 2026-09-19; fixed by PR #3224, in the clone since
2026-09-23; `-f tactile` works alone, used on 2026-09-26).  Building this paper needs `pretext -c prefigure -f svg` and `-f pdf` into
`generated/prefigure/` before the HTML and PDF builds, and `-f tactile` for the tactile set
(done 2026-09-26 on `20d10545`; the previous set is in `generated-superseded-2026-09-26/`).

`runs/2026-09-16-burau-demonstration/`: the paper in every output behind `index.html`
with the CC BY 4.0 attribution and the list of changes (source zip, usual PDF, AMS PDF,
XSL-FO PDF passing veraPDF as PDF/UA-1, HTML, EPUB, Jupyter, braille).  Rebuilt from
scratch on 2026-09-26 on the clone at `20d10545`, for Rob to publicize; the previous contents
are in `runs/2026-09-16-burau-demonstration-superseded-2026-09-19/`.  What changed, from
upstream fixes: the EPUB has 2 EPUBCheck errors instead of 17 (only issue #3209 left) and a
cover image of the title page; the XSL-FO PDF has typographic apostrophes; diagram labels
are in New Computer Modern (MathJax 4).  Details in the run notes, last section.  Two
changes to `index.html` at Rob's request: a second list item linking arXiv's experimental
HTML (`https://arxiv.org/html/2607.05283`, not opened, per the rule), and the typos
sentence softened to "we made no corrections of apparent errors or typos".  Ready to
upload; click the arXiv HTML link once before publicizing, since it is unchecked.

**PreTeXt defects from this run.**  (1) Filed as PreTeXtBook/pretext #3218 (2026-09-16),
fixed upstream in PR #3220 (merged 2026-09-17) and closed: the clone is pulled to
`93b7f665`, the PDF builds without any patch, and the patch file in the run directory is a
record only.  For the AMS PDF, hand-edit the generated LaTeX in one place (fontspec
`no-math`, defect (2)).  (2) Not filed: the AMS texstyle under xelatex fails
on a subscript inside `\mathrm` in the abstract because fontspec redeclares the `\mathrm`
alphabet and amsart sets the abstract before its script size exists; `\usepackage[no-math]
{fontspec}` cures it (the AMS PDF in the demonstration was compiled by hand that way).
(3) Mathematics in the article title reached the EPUB's `dc:title` and cover page as
MathJax SVG markup, giving 15 EPUBCheck errors; fixed upstream (PR #3240), gone on
2026-09-26.

**Skill.**  `scripts/crop-figures.py` is new (page-region crops from text positions and
ink, a JSON spec of panels per figure, contact sheets); `SKILL.md` has a paragraph of
this run's lessons under Pitfalls.  The full rewrite of `SKILL.md` from the three runs'
notes is still to do.

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
Both are fixed and closed (#3207 on 2026-09-15, #3208 on 2026-09-16), and the clone at
`156cd7f7` builds this paper's LaTeX PDFs with no patch.
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

1. Any new document: the prompt at the end of this file.  For 2607.05283 the PDF+LaTeX run
   (`source/Burau4-final.tex`) and the diff against the PDF-only run are next; its PDF
   builds on the current clone with no patch (#3218 is fixed upstream), and the AMS PDF
   needs the one fontspec edit in the generated LaTeX.  The skill is still the first draft
   plus the glyph checks, a Pitfalls paragraph, and the additions of 2026-10-03; the runs'
   notes (`notes.md`, sections
   "For the skill") hold what it should say differently.  Tactile PDFs of the 58 diagrams
   were sent for embossing (`runs/2026-09-16-burau-tactile.zip`); if the embosser wants
   heavier lines, raise the `thickness` values in the sections and rerun `-c prefigure -f all`.
2. PreTeXt issues filed from this work: #3207 (citations in theorem headings, and the
   unbraced optional argument in the classic conversion; fixed and closed), #3208
   (`support` in the LaTeX article; fixed and closed), #3209 (MathJax's `data-mjx-viewBox`
   in EPUB; open), #3218 (subfigures with distinct figure numbering; fixed and closed),
   #3221 (`-c prefigure -f tactile` and the missing `output/tactile/` directory; fixed by
   PR #3224, in the clone since 2026-09-23), #3249 (225 macOS AppleDouble files `._*` in
   the HTML's `_static/`, from the Runestone Services archive; filed 2026-09-26; left out of
   the Burau demonstration by hand, still in the scvt and Farmer ones).  The hand patches for #3207
   and #3208 are no longer needed (checked on the scvt paper, 2026-09-23).  The fix for
   #3207 added an `origins` element (PR #3217) as the home for a block's citations; the
   scvt source still puts them in `title`, and the skill should learn `origins`.  Not
   filed: the AMS texstyle under xelatex fails on a subscript inside `\mathrm` in an abstract (fontspec `no-math` cures it, still needed at `20d10545`); the braille conversion's errors for
   references to numbered equations; PreFigure's tactile mode needs integer `thickness`
   (an `int()` in `core/diagram.py`, for David Austin).
3. For scvt: the PDF+LaTeX run (`source/scvt_expo_submit.tex` matches `paper.pdf`) and the
   diff against the PDF-only run; then a run from `published.pdf` (no key) and a diff of the
   submitted and revised texts.
4. For Farmer: the PDF+LaTeX run, same comparison.
5. Rewrite `SKILL.md` from the runs' notes.
6. One small fix outside `runs/` still awaits Rob's approval: CLAUDE.md names `scripts/`
   where the scripts are `skill/pdf-to-pretext/scripts/`.
7. Rob's request, 2026-09-26: the `index.html` of the scvt and Farmer demonstrations
   should say what the Burau one now says, "The words and the mathematics are the
   authors' own; we made no corrections of apparent errors or typos."  ("author's" for the
   single-author papers.)  Neither page has a sentence about typos now, so it is an
   addition, after the paragraph that describes the transcription.

## Open items

- `compare.py` measures prose only; a display-mathematics comparison against a LaTeX key
  (normalized) is still to be written.  A first one exists for one paper,
  `runs/2026-10-03-vector-balancing-experiment/compare-sources.py`: two of its eight
  equivalences name that paper's macros and operators and would have to be made general.
- The skill says to read every delivered output, and gives no way to read the HTML with
  its mathematics rendered; in the experiment of 2026-10-03 the HTML was checked from its
  files only.  Raised with Rob, not decided.
- Figures: `scripts/crop-figures.py` crops panels from the page (boxes from text positions
  and ink, a JSON spec per figure, contact sheets); `scripts/trace-curve.py` and
  `scripts/trace-figure.py` vectorize drawings for PreFigure.  The generator that turns a
  trace into a PreFigure diagram lives in the Burau run's `prefigure-work/all-panels/`, not
  yet in the skill.
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
