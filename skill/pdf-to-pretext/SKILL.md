---
name: pdf-to-pretext
description: Transcribe a research article in mathematics from a PDF (and its LaTeX source when available) into valid, fully PreTeXt-native source. Use when asked to convert, transcribe, or transcode a paper or PDF into PreTeXt.
---

# PDF to PreTeXt

Produce PreTeXt source that reads as a faithful replica of a research article: every
word and every formula as the author wrote them, in PreTeXt's own structure.

**Fidelity principle.** Fully PreTeXt-native. A difference from the original is acceptable
when it changes neither content nor meaning: numbering, the wording of a reference
("Section 5.2" becomes an `xref`), placement of floats, typography. Words, mathematics,
and structure are never such differences.

## Before starting

- Installed: poppler tools (`pdftotext`, `pdftoppm`, `pdftocairo`), Python 3, and a PreTeXt
  checkout with its script (`pretext/pretext`) runnable through a venv. `scripts/build.sh`
  and `scripts/validate.sh` know where they are; adjust the paths there if needed.
- Inputs: the PDF, always; the LaTeX source when it exists, as the primary text. Never an
  HTML rendering of the paper.
- Make a run directory `runs/<date>-<short-name>/` and start `notes.md` with the output of
  `scripts/run-header.sh <model-id>`.

## Pass 1 — survey the whole document, write the manifest

Render the pages (`scripts/render-pages.sh`) and extract the text (`scripts/extract-text.sh`).
Read every page. Write `manifest.md` with:

1. Front matter: title, authors with affiliations and emails, date, keywords and MSC codes,
   abstract, acknowledgements, funding.
2. Divisions, in order, with proposed identifiers (`references/identifiers.md`).
3. Every numbered item — theorem-like blocks, definitions, remarks, equations, figures,
   tables — with its original number, its page, its class (`references/block-classes.md`),
   and its identifier. Unnumbered environments too, marked as such.
4. The numbering scheme, and the `numbering` element that mimics it (`references/numbering.md`).
5. Macros, each marked keep or expand, with the reason (`references/macros.md`).
6. Bibliography entries with identifiers and CSL types (`references/csl-bibliography.md`),
   and their DOIs (`scripts/lookup-dois.py`: Crossref first, then DataCite, which holds
   what Crossref lacks, arXiv preprints and the Dagstuhl proceedings among them).
7. Figures: which are composite and how they split; tables and their shapes.
8. Anything unreadable, with page numbers.

Most of PreTeXt is global — identifiers, numbering, macros, the bibliography — and the
manifest is what keeps section-by-section work consistent. Do not start pass 2 until it
is complete.

## Pass 2 — author, section by section

Start from `templates/main.ptx` and `templates/publication.ptx`. For each division, with
the page images open:

- Prose from the text layer, hyphenation and ligatures repaired, running heads and page
  numbers removed; never paraphrase.
- Mathematics from the page image (or the LaTeX source). Never guess: an unclear formula
  becomes `<!-- UNREADABLE: page N, ... -->` and a line in `notes.md`.
- Look-alikes are settled by the PDF, not by eye.  `pdftohtml -xml -i -f N -l N -stdout paper.pdf`
  names the font of every run of text on page N: text italic or math italic (is the "n"
  of "n-dimensional" mathematics?), a bold digit or a plain one.  The text layer's code
  points tell three typed periods (`...`) from `\dots` (". . ."), and a star (U+22C6)
  from an asterisk (U+2217).
- Every block preceded by its original-number comment; every reference an `xref`; every
  citation an `xref` to a `biblio`.
- Element names verified against the schema (`references/article-elements.md`).
- A construct whose rendering depends on a font feature (a bold or script Greek letter,
  an unusual alphabet, a wide accent) is a render risk: list each one in the manifest and
  verify it in every built output, or use the robust form and record the typographic
  difference.  A bold Greek capital via `\mathbf` silently vanishes under xelatex.
- Validate after every division (`scripts/validate.sh`); fix before moving on.

## Pass 3 — the whole document

1. Every `xref` resolves; every manifest item is present (count them).
2. `scripts/validate.sh` clean; `scripts/build.sh` to HTML and to PDF succeed, including
   the glyph check that follows a PDF build: no "Missing character" in the build log, no
   U+FFFD in the PDF's text layer.  Either one is a character of the source that did not
   reach the page, and a failure.
3. `scripts/compare.py <original.pdf> <built.pdf>`: record the similarity, read every run
   it reports absent (moved text counts as absent), and account for every symbol it
   reports with a lower count in the build.
4. Read every page of every delivered output side by side with the original when the
   paper is short (under about twenty pages); for a longer paper, every page with a
   display or a figure and a sample of the rest.  A single lost glyph cannot be found by
   sampling.  Fix what you find; repeat until a pass finds nothing.
5. Record the run in `evaluation/RESULTS.md`; finish `notes.md` with what was hard and
   what this skill should say differently next time.

## Pitfalls

PreTeXt supplies the period after a title, on `paragraphs`, `li`, and theorem-like blocks
alike, so a title copied with its final period prints two: store titles without the
period, but keep a question mark or any other final punctuation the author wrote.  A
display wider than the text block spills into the margin in the original but is clipped
at the page edge by the LaTeX conversion: break it into `mrow`s (a typographic change)
rather than lose terms.  Figures that are pictures with labels typeset over them are
cropped from the page with `scripts/crop-figures.py` (boxes from text positions and ink,
a spec of panels per figure, contact sheets to check); composites are cut into panels,
lettered only where the original letters them, with panel widths from the pictures'
natural sizes.  A hand-drawn arc can be recreated in PreFigure by tracing it from a 600-dpi render with
`scripts/trace-curve.py` and feeding the points to a `spline` with chord-length `t-values`;
crossings with gaps are one spline drawn piecewise by `domain`, with the crossing points as
knots.  A whole colored line drawing is vectorized by `scripts/trace-figure.py` (curves by
color, arrowheads, dots, dashes, fills, bands) and turned into a PreFigure diagram of
`polygon`s with labels from the text layer; tune its palette per paper and read a
comparison sheet after every change.  Count items from the assembled XML, not from the manifest's own header.
After a PDF build, read the `Overfull` lines above about twenty points as well as the
glyph check.

Two-column layouts interleave in extraction; footnotes float; ligatures (`fi`, `fl`)
come out as single characters; end-of-line hyphens split words; `--` and quotation marks
need their PreTeXt elements; a "Notation" or "Remark" environment is often unnumbered;
a remark set upright ends only where the vertical space says so: decide from the spacing
and the sense, and record the decision in the manifest as a judgment;
an article has no `acknowledgement` element, so an unnumbered Acknowledgements section is
a titled `paragraphs` closing the last section;
a named theorem keeps its name as a `title`; "Proof of Theorem 3" is a titled `proof`;
lettered main theorems ("Theorem A") cannot be lettered by PreTeXt — keep the letter in
the title and the comment; a lost glyph leaves only two traces, the engine's "Missing
character" warning in the build log and a U+FFFD in the text layer, and the prose
comparison cannot see it.
