# Experiment — one paper transcribed twice, from the PDF alone and from the LaTeX

Rob's request, 2026-10-03.  Paper: arXiv 2610.02127v1, Niles-Weed, Sadovsky, Shkrob, "An
optimal constant for vector balancing with permutations", 12 pages, no figures or tables.
Model claude-opus-5-5, Claude Code 2.1.288, PreTeXt clone at `bf795ab1` (pulled first).

Not an open license, and the authors are not known to Rob.  The transcriptions, the diffs,
and the scripts are under `runs/`, which is gitignored: they exist on Rob's machine only.
No corpus entry, no results row.  This report is the one part kept in the repository
(`notes/2026-10-03-pdf-only-versus-latex.md`); a copy is in the experiment directory.

| | |
|---|---|
| A, PDF only | `runs/2026-10-03-vector-balancing-pdf-only/` |
| B, with the LaTeX | `runs/2026-10-03-vector-balancing-latex/` |
| comparison, effort | `runs/2026-10-03-vector-balancing-experiment/` |

File names below with no directory are in the third of these.

A was finished, built, read, and checksummed (`pdf-only-checksums-before-latex.txt`,
12:58:33) before anything was requested from arxiv.org; the e-print was fetched at 12:58.
B's words and mathematics were not retyped: two scripts written for this paper take them
from the `.tex` and the `.bib`, so that B is a key independent of my reading of the PDF.
B uses A's identifiers so the two can be compared.

## Result

Both validate with no messages, build to HTML with no warnings and to a ten-page PDF with
a clean glyph check, and number every block (1-11) and equation ((1)-(9)) as the original.

**A has no error of words or of mathematics.**  Against B:

| | A | B | |
|---|---|---|---|
| structural elements | 221 | 220 | identical, but for the `date` |
| running text, tokens | 2347 | 2349 | identical words; three places differ in markup only (below) |
| bibliography, 21 entries | | | identical to the character |
| formulas | 302 | 303 | 302 paired |
| ... identical as written | | | 145 |
| ... identical as TeX tokens | | | 223 |
| ... equivalent | | | 301 |

The 301 comes from eight equivalences, each one a different spelling of the same
typeset mathematics, applied in turn (`comparison/summary.txt` has the counts):
`\eps` and `\R` expanded (22 pairs); `\le` for `\leq`, `\lVert` for `\|`, `\ast` for `*`,
`\tfrac` for `\frac` (38); `\ldots`, `\cdots`, `\dots` (3); `\text{vb}`, `\mathrm{vb}`,
`\operatorname{vb}` (4); `~`, `\ `, `\quad` (11); `\left`, `\right` (24); braces around one
token (25); `x^*_i` for `x_i^*` (1).  The normalizer was tested on pairs it must keep
apart (`\frac{1}{n-1}` and `\frac{1}{n}-1`, `p^*` and `p^\star`, `1_S` and `\mathbf{1}_S`).

What is left, all of it markup that prints the same:

1. "the constant is at least 2": text in A, `<m>2</m>` in B (the source has `$2$`).
2. "(0 < k < n)": the parentheses are inside the `m` in A, outside in B.
3. `<date>October 2, 2026</date>` in A, none in B: the source has no `\date`, so the
   printed date is `\today`.
4. Ten `nbsp` in B before citations and equation references, none in A.
5. `docinfo/macros`: empty in A, `\R` and `\eps` in B.

## The three diffs

- `source-trees.diff` — `diff -ru` of the files as written: 864 lines; 180 of A's 880 lines
  removed, 178 added.  Nearly every line with mathematics differs, in spelling.
- `comparison/as-written.diff` — both put one sentence or display to a line, comments
  dropped: 257 changed lines.  The readable one.
- `comparison/normalized.diff` — the same after the eight equivalences: 16 lines, items 1
  to 3 above.

## What the PDF-only reading got right that could have gone wrong

Each was a judgment in A's manifest, and the source confirmed every one: `1/p^\star`
beside `p^*` in one display; the literal `...` in Lemma 5; the plain `1_S` beside the bold
`\mathbf{1}`; an apparent inconsistency between two statements of the paper, kept as
printed; where Remark 8 ends (spacing was the only sign); every paragraph break;
"Acknowledgements" as a titled `paragraphs` closing Section 3 (the source has
`\subsection*`); the `n` of "n-dimensional" as text; and the DOI attached to [14], which
the `.bib`'s arXiv number confirms.

## What only the LaTeX shows

The date is `\today`; the authors' macros and labels; nonbreaking spaces; three spellings
of "vb"; one word of a title that the `.bib` capitalizes and amsplain prints in lower case.
None changes a printed character except the date.

## What the LaTeX path got wrong at first

`k_2<\dots<k_m`: amsmath centers `\dots` by looking at the next character, and PreTeXt's
`\lt` hides the `<` from it, so the first B build set those dots on the baseline.  A, read
from the page, had `\cdots` and was right.  Found by `compare.py` (3 middle dots against
6), fixed in the converter.  Also `{n\choose 2}` draws an amsmath warning; now `\binom`.

## Is A's LaTeX better, or its structure?

Rob's question on reading the above.  More uniform, yes; more semantic, only slightly;
the structure is the same.

**The LaTeX.**  A is tidier because one writer chose one spelling for each thing, where
the source shows several hands.

- "vb" is written three ways in the source (`\operatorname{vb}` twice, `\text{vb}`,
  `\mathrm{vb}`) and "conv" is `\text{conv}`.  A has `\operatorname` throughout, the right
  one: `\text` takes the surrounding font and would turn italic inside a theorem.
- A norm is written four ways in the source: `\|` (5), `\left\|` (10), `\lVert` (5),
  `\left\lVert` (10).  A has `\|` inline and `\left\|` in displays.
- The source has `{n\choose 2}` twice beside `\binom` once, `$$` (15) beside `\[` (20),
  twelve `~` inside mathematics to adjust spacing, braces such as `v_{1}`, sentence
  punctuation inside `$...$` in three places, and one `\eqref` inside `$...$`.

But A is not the more semantic of the two.

- `\lVert ... \rVert` is a paired delimiter and A's inline `\|` is not.  `\dots` is
  amsmath's form that reads its context; A's `\cdots` was only the more robust one under
  PreTeXt.
- The parentheses of "(0 < k < n)" outside the mathematics, and the "2" inside it, are
  the better markup, and they are the authors'.
- Neither has a macro that carries meaning.  The authors define `\one` for the all-ones
  vector and never use it, writing `\mathbf{1}` 36 times; A writes `\mathbf{1}` too,
  because the rule for a PDF-only run is no invented macros.

Much of A's tidiness is a side effect: a `~` or a redundant brace cannot be seen on the
page, so it cannot be copied.  And it is a matter of policy, not of input: B kept the
authors' spelling on purpose and could normalize as easily, as it already does for
`\choose`.  Whether it should is for Rob to decide.

**The structure.**  The same 220 structural elements in both.  That is weaker evidence
than it sounds, since B reused A's choice of elements and its identifiers.  What it does
show is that every block boundary and every paragraph break read off the page matched the
source.  In one place the page was the better guide: the source has a blank line before a
display (line 242 of the `.tex`), which a literal conversion would turn into a paragraph
that starts with the display.

This is one short, clean paper, and the judge is the transcriber.

## For a LaTeX path, later

Rob, 2026-10-03, on a proposal to give the skill a section for transcribing from LaTeX:
"let's NOT do this"; this report is where to pick the matter up.  What that section would
have said:

- `\dots` before `<` or `>` must be written `\cdots`.  PreTeXt needs `\lt` and `\gt`, and
  amsmath centers `\dots` only when it can see the relation character.  After `<`, `>`,
  and `&` are replaced, look again at every command that reads what follows it.
- The mechanical rules this paper needed.  `~` in text is `nbsp`, except after "Theorem",
  "Lemma", "Section", where the `xref` takes its place; `Theorem~\ref{...}` is a bare
  `xref`; a period or comma that ends `$...$` moves outside the `m`; an `\eqref` inside
  `$...$` comes out of the mathematics; `{n\choose 2}` is `\binom{n}{2}`;
  `\texorpdfstring{A}{B}` is `A`; a blank line before a display does not start a
  paragraph; of 86 macros in the preamble the body used 3, and one used once is expanded.
- With no `.bbl` in the e-print, the capitals of the printed bibliography are the style's
  (amsplain lowers every unprotected word after the first), so the list is rebuilt by
  that rule or taken from the PDF; the `.bib` adds entry types and a few DOIs.
- Scoring the PDF-only path against the source: finish and checksum the PDF-only run
  before fetching the source; generate the second transcription from the `.tex` by
  script, with the first run's identifiers; compare formulas after the equivalences of
  `compare-sources.py`.  Two of that script's rules are written for this paper (the
  macros `\eps` and `\R`, the names "vb" and "conv"); made general, it would be the
  comparison of display mathematics that `TRANSITION.md` lists as still to be written.

Left open, since without that section nothing forces an answer:

- whether a printed date that is `\today` is kept;
- whether the bibliography follows the printed case or the `.bib`;
- whether the authors' labels become the identifiers;
- whether a transcription from LaTeX keeps the authors' spelling or normalizes it.

One open point is not about LaTeX.  The skill says to read every delivered output and gives
no way to read HTML with its mathematics rendered.  Here both HTML builds were checked
from their files (headings, block numbers, equation tags) and not in a browser.

## Effort

From the session's transcript (`effort-report.py`).  "New context" is what each turn added
to the conversation; output tokens include reasoning.

| phase | wall time | model turns | tool calls | images read | output tokens | new context tokens |
|---|---|---|---|---|---|---|
| PDF only, pass 1: survey, DOIs, manifest | 7 min 53 s | 22 | 44 | 20 | 44,717 | 173,707 |
| PDF only, passes 2 and 3: author, validate, build, read, compare | 6 min 22 s | 21 | 30 | 11 | 41,712 | 75,053 |
| LaTeX: fetch, convert by script, validate, build, read | 7 min 51 s | 14 | 23 | 8 | 46,699 | 93,092 |
| the diff: comparison script, normalizer, three diffs | 1 min 15 s | 4 | 3 | 0 | 7,370 | 23,474 |
| records: manifests, notes, report | 3 min 15 s | 8 | 9 | 0 | 20,078 | 27,569 |
| total | 26 min 36 s | 69 | 109 | 39 | 160,576 | 392,895 |

Read these with two cautions.  B did not start from nothing: it took its identifiers,
numbering, publication file, and fourteen of its DOIs from A, so 8 minutes is the cost of
a LaTeX run that follows a PDF-only run, not of one alone.  And the paper is short and
clean: pdfTeX output with a good text layer, no figures, no tables, no two-column pages.

By count, A: 12 pages read at 150 dpi and 8 regions at 300 dpi, 27 lookups for DOIs, 5
source files written by hand in one pass, 2 validations, 2 HTML and 2 PDF builds, 10 built
pages read.  B: 2 scripts (495 lines), 2 validations, 2 HTML and 2 PDF builds, 8 built
pages read.  The diff: 1 script (320 lines).

The table stops at 13:10, before the report was made a PDF and before what follows.

## Afterwards, the same day

At Rob's word, and committed: this report in `notes/`, with two remarks on the paper's
text made general; the article template given the `titlepage` the schema requires, and the
skill's reference file corrected on acknowledgements; three additions to `SKILL.md` for
the PDF-only path (fonts and code points for look-alikes, where an upright remark ends,
DOIs at DataCite) with a script, `lookup-dois.py`, which on this paper's 21 entries finds
what the lookups by hand found (14 at Crossref, 5 at DataCite only, 2 with no DOI);
`build.sh` lists the wide overfull boxes of the last LaTeX pass; `compare.py` gives a
second similarity for the text before the reference list (0.937 for A, where the whole
text gives 0.918).
