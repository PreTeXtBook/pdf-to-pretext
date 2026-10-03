date: 2026-09-03
model: claude-fable-5-1
claude code: 2.1.259 (Claude Code)
pretext commit: 59cd06c1 (2026-09-03)

# Run notes — corpus/own/scvt (Beezer, Sylow subgraphs), PDF-only path

## Inputs and policy for this run

- Read: `corpus/own/scvt/paper.pdf` (the submitted version, pdfTeX, 2004-12-30, 10 pages),
  its 150-dpi renderings in `pages/`, and `paper.txt` (`pdftotext -layout`).
- Not opened: `corpus/own/scvt/source/` (`scvt_expo_submit.tex`, `scvt_eversion_final.tex`,
  and the figure file `scvt9.pdf`), and `published.pdf` (Elsevier, Expo. Math. 24 (2006)
  185–194), which is for a later diff and a later run.  No HTML rendering exists.
- Rob's standing rulings apply: nothing from outside the PDF (no arXiv-style metadata),
  typos preserved verbatim, composite figures split unless stacked.

## Effort log

Wall-clock times are from the shell clock; "context tokens" is the decrease of the
session's token counter across the pass (tokens added to the conversation: page images,
tool output, and my own writing).  Billed tokens are larger, since the whole conversation
is re-sent, mostly from cache, on every step.

| pass | started | finished | wall time | context tokens | notes |
|---|---|---|---|---|---|
| 1 (survey) | 16:40 | 16:50 | 10 min | about 100,000 | 10 pages read at 150 dpi, 18 crops at 300 dpi (9 mis-aimed), 26 Crossref queries, manifest written |
| 2 + 3 (author, build, compare) | 16:56 | 17:04 | 8 min | about 80,000 | 8 source files, 1 crop, 2 validations, 2 HTML, 2 PDF and 1 AMS-style build, 4 pages read side by side |

## Pass 1 — survey (2026-09-03)

- The PDF's page numbers are off by one from the printed ones (unnumbered title page);
  the first round of 300-dpi crops used printed numbers and landed on the wrong pages.
  Worth a sentence in the skill: say which numbering `pdftoppm -f` uses.
- Crossref found DOIs for 20 of 23 entries; the two Australasian Journal of Combinatorics
  papers and the personal communication have none.  Six lookups failed on the first
  pass (empty responses) and succeeded on retry — retry before concluding "no DOI".
- The article schema has no place for an acknowledgement: it becomes a `paragraphs`
  at the end of the last section, which is also where LaTeX put it.
- Nothing unreadable.  The empty-set glyph is a judgement call (`\varnothing`).

## Pass 2 and 3 — authoring, build, compare (2026-09-03)

- Layout as in the Farmer run: `main.ptx` with `xi:include` of `sections/*.ptx`,
  `publication.ptx`, `publication-ams.ptx`, `external/` with the one figure (SVG and PDF).
- Validation: schema clean on the first run.  Validation-plus warned about Unicode
  en dashes in `page` (`<ndash/>` is not allowed there); the ranges now use a hyphen,
  the CSL convention.  Clean after.
- Builds: HTML and PDF without warnings; every `xref` resolves; every number
  coincides with the original (Definition 2.1 … Theorem 5.2, Lemma 3.2, Figure 1).
  Item count 54 of 54 (the manifest header had said 12 numbered blocks; it is 11 plus
  the remark, and the count check caught the slip).  `compare.py` 0.958 (4,072 words
  against 4,069); every reported missing run is moved text (the thanks, the author
  block, the caption) or the text layer's garbage for tilde-M.
- **PreTeXt finding, title page of the default LaTeX article.**  `author/support` is
  emitted as a `\\`-separated row inside `\author{…}` (`xsl/pretext-latex-common.xsl`,
  template `author` mode `article-info`).  A 37-word statement makes the author tabular
  wider than the page, LaTeX abandons the centering, and the name, affiliation, and
  email rows are pushed off the right edge: the built title page shows the title, one
  clipped line of the thanks, and the date.  The Farmer sentence was short enough to
  fit, which is why this did not show there.  The classic conversion
  (`pretext-latex-classic.xsl`, `author` mode `article-frontmatter`) wraps it in
  `\thanks{}` instead, and the AMS texstyle does too.  Second finding, same file: the
  two identical `bibinfo/support` templates apply `*` children, and `support` is mixed
  text, so an article-level support statement renders nothing — the cause of the
  "funding sentence absent" departure in the Farmer run before it moved into `author`.
  Both are Rob's to file; the source keeps `author/support`, which is the right place.
- `paper-ams.pdf` (AMS texstyle, 8 pages) has the date, keywords, and the full thanks
  as first-page footnotes, and is the build to read.
- The published version (`published.pdf`) and the source were not opened.  The diff
  of the submitted and revised texts is the next run's business.

## For the skill

- Say that PDF page numbers and printed page numbers can differ; check before cropping.
- Say that `page` ranges take a hyphen.
- The count check is worth doing against the manifest's own tables, not its header.

## Rob's reading of the AMS-style PDF (2026-09-03, evening)

Three reports, three causes.

1. **"Aut( )" with no Gamma, start of Section 2.**  The source had `\mathbf{Aut(\Gamma)}`
   to match the original's bold "Aut(Γ)"; under the AMS build's fonts `\mathbf{\Gamma}`
   has no glyph and printed as a blank (the plain build and MathJax showed it).  Now
   `\mathbf{Aut}(\Gamma)`: "Aut" bold, Γ regular.  Manifest updated.
2. **"Theorem 3.1 ([17, 22). ]If …", and Lemma 3.2 likewise.**  A PreTeXt defect in
   `xsl/pretext-latex-classic.xsl`, which the AMS texstyle imports: the theorem-like
   `env-title` template (and the proof-title branch, and the aside/assemblage one) writes
   the title into the amsthm optional argument as `[…]` without braces, so a `]` inside
   the title — every citation has one — ends the argument early.  The default conversion
   passes titles as braced tcolorbox arguments and is unaffected.  Fix: `[{…}]` in those
   three places; the diff is `pretext-latex-classic-optional-argument.patch` in this run
   directory (made against a copy; the clone is untouched).  `paper-ams-patched.pdf` is
   the generated LaTeX with that patch applied by hand and compiled with xelatex, as the
   proof that it works: "Theorem 3.1 ([17, 22]). If …".
3. **"References are not live links."**  In the prose they are: the AMS PDF has 53 link
   annotations and all 53 resolve to named destinations, 23 of them `biblio-*`
   (checked with PyPDF2).  The citations that are not links are the ones inside theorem
   headings, because PreTeXt's `title-xref` mode renders an `xref` in a title as plain
   text (titles also feed running heads and tables of contents).  Behaviour, not a bug;
   worth knowing when a paper cites sources in theorem headings, as this one does.

Seen on the same page: the unnumbered Remark of the original prints as "Remark 3.3" in
every PreTeXt output — blocks are always numbered, and the remark class shares the
theorem counter.  No later item in Section 3 is displaced.  Numbering is a permitted
difference; recorded here and in the manifest's expected-agreement line.

Posted as PreTeXtBook/pretext issue #3207 on 2026-09-03 (the markup proposal plus the
unbraced-optional-argument bug, with the diff).

## Why the missing Gamma was not seen (post-mortem, 2026-09-03)

What happened: `\mathbf{Aut(\Gamma)}` lost its Γ in **both** PDF builds, plain and
AMS, not only the AMS one.  Under xelatex with fontspec, `\mathbf` takes an uppercase
Greek letter from the text font's Unicode slot, and Latin Modern Demi has none; the
engine wrote "Missing character: There is no ^^@ (U+0000) in font
[lmromandemi10-regular]" to its log, and the PDF's text layer got U+FFFD where the Γ
should be.  The Farmer builds have no such warning and no U+FFFD.

Four reasons it got past me, in order of weight:

1. **I never looked at the page.**  Pass 3 read built pages 1, 2, 5, and 8 of 9 against
   the original; the defect is on page 3.  The AMS output was checked on page 1 only,
   then handed over as the file to read.  A single lost glyph cannot be found by
   sampling; the skill's "three sample pages" rule invites exactly this.
2. **The engine's own warning was in a log I had, and I did not grep for it.**  Both
   build logs carried "Missing character" twice.  My log check looked only for
   PreTeXt's `PTX:WARNING` and `PTX:ERROR` lines.
3. **`compare.py` is blind to mathematics by design**, and I let its 0.958 stand in for
   "content complete".  It compares words; "Aut(Γ)" and "Aut( )" have the same words.
4. **I introduced the risk myself**, copying a typographic detail (the bold Γ) that the
   fidelity principle does not require, with a construct whose rendering depends on a
   font feature, and did not verify it in the built output.

Three checks that would each have caught it, tried against every build of both papers:

- `grep -c 'Missing character'` on the build log: 2 in each defective build, 0 elsewhere.
- U+FFFD in `pdftotext` of the built PDF: 1 in each defective build, 0 elsewhere.
- A symbol inventory (`symbol-inventory.py`, kept here): counts of every non-ASCII
  character in the two text layers; the defective build reports
  "Γ  GREEK CAPITAL LETTER GAMMA  79  78  <-- MISSING", and after the fix that line is
  gone.  The rest of its output is encoding noise (combining accents against
  precomposed letters, ∑ and ∏ extracted differently from Type 1 fonts) that
  normalization can remove.

Proposed for the skill: run the first two after every PDF build and treat any hit as a
failure; add the inventory to pass 3; read every page of every delivered output when
the paper is short, and every page with mathematics when it is not; and in pass 2 list
font-feature constructs (bold or script Greek, unusual alphabets) as render risks to be
verified per output, or replaced by the robust form with the typographic difference
recorded.

The two `support` defects were posted as PreTeXtBook/pretext issue #3208 on 2026-09-04.

## Figure 1 as a PreFigure diagram (2026-09-04)

- The drawing, read from the cropped SVG: nine circles, sixteen straight segments, two
  cubic curves for the edges between opposite corners (bowed left of the center so they
  miss the center vertex), and one degenerate zero-length path.  Matched against the
  computed Paley graph on GF(9) (x² + 2x + 2 = 0, squares {1, 2, x+1, 2x+2}): identical
  when x^k sits at the k-th corner clockwise from the top, as the text says.
- Corrected 2026-09-23.  The first reading said "counterclockwise", and the diagram was
  drawn upside down, because the parse ignored the `transform` on the cropped SVG's paths
  (`matrix(0.4,0,0,-0.4,…)`, which already flips y) and flipped y a second time.  The
  paper was right.  For the skill: apply an SVG's transforms before reading geometry from
  path data, and check a recreated figure against the original on one concrete fact,
  such as which vertices the top vertex joins.
- Markup: `network` with `node/@p` positions on a regular octagon of radius 1 (the
  original's corners are hand-placed and slightly uneven), `node-size="8"`,
  `edge-thickness="2"`, no labels; the two bowed edges as `path` + `quadratic-bezier`
  with control points (−0.28, ±0.28), given `@at` ids in the network's naming scheme so
  the annotations can name them.  Annotations: one sentence for the graph, one per
  vertex naming its neighbors, one per curved edge.
- Generation: `pretext -c prefigure -f svg` and `-f pdf` into `generated/prefigure/`;
  HTML embeds the diagcess version for keyboard exploration, LaTeX takes the PDF.
  Validation clean.  `-f tactile` fails in `pretext.py` (`individual_prefigure_conversion`
  moves `output/<name>.pdf` into `output/tactile/`, which prefig 0.7.4 does not create)
  — a PreTeXt-side bug for Rob.
- Weights were tuned once against the original: nodes of radius 8 pixels on a 174-pixel
  octagon radius (the original's ratio), edges 2.

## Demonstration directory (2026-09-04)

`runs/2026-09-04-scvt-demonstration/`: the published version (DOI link), the preprint,
the source (with `generated/prefigure/`), three PDFs, HTML, EPUB, Jupyter, braille,
behind `index.html` with Rob's permission line.  The two LaTeX PDFs are hand-patched
generated LaTeX, compiled with xelatex: the AMS one with the braces of issue #3207, the
usual one with the funding note moved into `\thanks` as issue #3208 proposes; the
pipeline outputs are not fit to show until the two issues are fixed.  The XSL-FO PDF
needs neither patch: its title page wraps the note and its headings read
"Theorem 3.1. [17, 22].", and veraPDF passes it as PDF/UA-1.  epubcheck's 36 CSS
errors and the braille conversion's equation-reference errors are as for Farmer.

Rebuilt 2026-09-23 with the corrected figure, from the clone at `93b7f665`, then again
after a pull, from `156cd7f7`; the two builds differ only in timestamps and Jupyter cell
ids, and the demonstration holds the second.  Issues #3207 and #3208 are fixed there, so both LaTeX PDFs are now the pipeline's own, unpatched and
glyph-clean ("Theorem 3.1 ([17, 22])." in the AMS one, the funding note in `\thanks` in
the usual one).  The XSL-FO PDF again passes veraPDF as PDF/UA-1, and the EPUB is clean
under epubcheck 5.3.0.  The braille file came out byte-identical, since it carries only
the figure's description.  The September 4 HTML, whose JavaScript bundles have other
names, was moved aside to `runs/2026-09-04-scvt-demonstration-html-superseded/` rather
than deleted.

## Effort, the rest of 2026-09-04 (approximate, from the clock)

| work | wall time | context tokens |
|---|---|---|
| PreFigure figure, with the edge-by-edge check of the drawing and two rounds of annotations | about 50 min | about 120,000 |
| demonstration directory, hand-patched PDFs, servers | about 30 min | about 60,000 |
