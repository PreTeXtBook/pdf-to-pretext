# Pitfalls

Each entry is a mistake made once in a real transcription.  Read them all before pass 2.
New entries go under the heading they fit, one entry to a paragraph.

## The text layer

- **Hyphens and ligatures.**  End-of-line hyphens split words, and ligatures (`fi`, `fl`)
  come out as single characters.  Repair both.
- **Accents.**  Older LaTeX sets an accent as a glyph of its own beside its letter.  The
  extraction joins the two, but check every accented name against the page image.
- **A glyph with no character.**  A symbol the PDF's fonts give no Unicode for extracts
  as a control character or as nothing readable.  That is the original's doing and tells
  you to read the symbol from the image; in a PDF you built, `scripts/build.sh` checks
  for the kind that means a glyph was lost.
- **Columns and floats.**  A two-column layout interleaves in extraction; footnotes and
  floated captions land away from where they are read.
- **Wide accents and stacked scripts.**  A wide tilde over a subscripted letter, or a
  superscript over a subscript, extracts as scattered characters.  Read these from the
  page image.
- **Page numbers.**  The PDF's page numbers and the printed ones can differ.  Check before
  cropping or citing a page.
- **The stamp.**  An arXiv stamp in the margin is in the text layer and is not part of
  the document.

## Structure

- **Unnumbered environments.**  A "Notation" or "Remark" environment is often unnumbered.
- **Where an upright remark ends.**  A remark set in upright type ends only where the
  vertical space says so.  Decide from the spacing and the sense, and record the decision
  in the manifest as a judgment.
- **Named theorems.**  A named theorem keeps its name as a `title`.  An attribution in the
  heading, "(Hadamard)", is a `creator`; a citation there goes in `origins`.
- **Lettered theorems.**  PreTeXt cannot letter a theorem ("Theorem A").  Keep the letter
  in the `title` and in the comment that records the original number.
- **Proofs away from their theorem.**  "Proof of Theorem 3", with other text between it
  and the theorem, is a `proof` with `@ref` naming the theorem.  PreTeXt prints
  "Proof. (Theorem 3)", an acceptable difference.
- **Acknowledgements.**  An article has no `acknowledgement` element and no unnumbered
  division.  An unnumbered Acknowledgements section is a titled `paragraphs` closing the
  last section.
- **Run-in headings.**  A bold run-in heading begins a `paragraphs` that runs to the next
  heading.

- **The comment before a section.**  A section is a file of its own, and a comment before
  the root element of an included file is lost in assembly.  Its `<!-- Original: ... -->`
  goes in `main.ptx`, before the `xi:include`.

## References

- **A reference with no target passes validation.**  PreTeXt's validation says "no
  messages" for an `xref` that names nothing, and PreTeXt's builds exit as if all were
  well, with one line in the log.  `scripts/validate.sh` lists such references and
  `scripts/build.sh` refuses the build; do not run PreTeXt's script some other way and
  take its silence for success.

## Titles

- **The final period.**  PreTeXt supplies the period after a title, on `paragraphs`, `li`,
  and theorem-like blocks alike, so a title copied with its final period prints two.
  Store titles without the period; keep a question mark or any other final punctuation
  the author wrote.

## Text

- **Dashes and quotation marks** need their PreTeXt elements (`ndash`, `mdash`, `q`, `sq`).
- **A title cited in prose** is an `articletitle` or a `pubtitle`.

## Mathematics

- **The three characters XML keeps for itself.**  In mathematics write `\amp`, `\lt`,
  `\gt` for `&`, `<`, `>`.  A bare `&` or `<` is not well-formed XML, and these three
  are what PreTeXt defines for the purpose.

- **A display wider than the text block** spills into the margin in the original but is
  clipped at the page edge by the LaTeX conversion, losing terms; HTML scrolls instead.
  Break it into `mrow`s (a typographic change) rather than lose terms.
- **A lost glyph leaves only two traces**: the engine's "Missing character" warning in the
  build log, and a glyph with no character in the PDF's text layer.  The comparison of words cannot see it.
  `scripts/build.sh` checks both after a PDF build.
- **Font-dependent constructs.**  A bold Greek capital written with `\mathbf` vanishes
  under xelatex.  Do not copy a typographic detail the fidelity principle does not
  require with a construct you have not seen render.
- **The removed elements.**  `me`, `men`, and `mdn` no longer exist.  Display mathematics
  is `md`, with `@number` for a single numbered line and `mrow`s for several.

## Front matter

- **A long affiliation** set on one line can be wider than PreTeXt's title block; put it
  on several `line`s inside `institution`.
- **Where the addresses are.**  A document may print its authors' addresses at the end.
  They still belong in `bibinfo`; note the change of place in the manifest.

## Checking

- **Count from the assembled source**, not from the manifest's own tallies: the tallies
  are what you are checking.
- **A moved run counts as absent** in `scripts/compare.py` (a footnote, a floated caption,
  an address block).  Read the runs it lists; do not trust the number alone.
- **Symbols reported with a lower count** are often an artifact of the built PDF's text
  layer (a norm bar extracted as a letter, a not-equal sign as two characters).  Each one
  still has to be found on the page before it is dismissed.
- **Overfull boxes.**  After a PDF build, look on the page at each overfull box that
  `scripts/build.sh` lists.  A DOI in the bibliography cannot be broken by PreTeXt's
  rendering and will be among them.
- **Sampling pages is not checking.**  A single lost glyph was missed once because only
  four pages of nine were read.
