---
name: pdf-to-pretext
description: Transcribe a mathematics research article from a PDF into valid, fully PreTeXt-native source, with every word and every formula as the author wrote them, then validate it, build it to HTML and PDF, and compare the result with the original. Use this whenever someone wants to convert, transcribe, port, or move a paper, preprint, arXiv article, or journal PDF into PreTeXt, including when they only say "turn this PDF into PreTeXt" or ask for an accessible or HTML version of a paper they have only as a PDF.
---

# PDF to PreTeXt

Produce PreTeXt source that reads as a faithful replica of a research article: every word
and every formula as the author wrote them, in PreTeXt's own structure, so that PreTeXt
can make from it HTML, PDF, EPUB, braille, and whatever it learns to make later.

## The fidelity principle

Fully PreTeXt-native. A difference from the original is acceptable when it changes neither
content nor meaning: numbering, the wording of a reference ("Section 5.2" becomes an
`xref`, and PreTeXt supplies "Section"), placement of floats, typography. Words,
mathematics, and structure are never such differences.

Three rules follow from it.

- **Do not correct the author.** A typo, a missing period, a formula that looks wrong, an
  inconsistent bibliography entry: transcribe it as printed. The reader who compares your
  work with the original must find the same text, and the "obvious" correction is
  sometimes the mistake. Say what looks wrong in the manifest instead, where the person
  you work for can decide what to tell the author.
- **Do not guess.** A formula you cannot read becomes `<!-- UNREADABLE: page N, ... -->`
  and a line in the notes. Symbols that look alike are settled by evidence from the PDF
  (pass 2), never by what the mathematics ought to say.
- **Only what the document prints.** No date, subject codes, keywords, or better title
  taken from an arXiv record, a journal's page, or memory. The one addition is a DOI for a
  bibliography entry, looked up and checked (pass 1).

## Before starting

1. **Rights.** A transcription is a derivative work of the original. Find the document's
   license (its first page, its arXiv record, the journal) and tell the person you are
   working for what it allows, before anything else. Without an open license or the
   author's permission a transcription may be made but not distributed; that is their
   decision, and they need the facts to make it.
2. **Setup.** Run `scripts/setup.sh` yourself, without asking: the first time the skill
   is used on a machine, and again before each new transcription. It gets PreTeXt and
   builds a Python environment for it, both in the skill's own data directory, updates
   them when they are already there, and ends with a trial build. The person should not
   have to do any of this. The one thing it cannot do is install a program for the whole
   machine, and the only such program it needs is a TeX distribution; when that is
   missing it prints the single command that installs it, and that command is what you
   pass on to the person.
   PreTeXt changes from week to week, which is why the script is run each time; the
   notes' header records the commit that was used.
3. **Inputs.** The PDF, always, and it must have a text layer: a scan without one is
   outside this skill. The LaTeX source when it exists, as the primary text. Never an
   HTML rendering of the paper (arXiv's, a journal's): that is another party's
   conversion, with its own errors. `scripts/pdftool.py` does everything the skill asks
   of a PDF (text, the position of every line, the font of every run, page images, zooms,
   pictures, crops); run it with no arguments for the list.
4. **The project.** `scripts/new-transcription.sh <paper.pdf> <directory> <model-id>`
   lays out the project, copies the original in, renders its pages at 150 dpi, extracts
   its text, and begins the notes. `references/project-layout.md` says what goes where:
   PreTeXt source in `source/`, the publication file in `publication/`, figures in
   `assets/`, builds in `output/`, your working papers in `transcription/`.

In this file, a path that begins `scripts/` or `references/` is in the skill's own
directory; every other path is in the project.

PreTeXt is run only through its own script, by `scripts/validate.sh` and
`scripts/build.sh`. When the script fails, correct the source if the source is at fault,
and otherwise record the defect (see "Finishing"); do not make the output some other way.
An output made by another tool is no evidence that the source is valid PreTeXt.

## Pass 1: survey the whole document, write the manifest

Read every page image with the extracted text beside it. Fill in
`transcription/manifest.md`, whose headings are already there:

1. Front matter: title, authors with affiliations and emails, and where the document
   prints them; date, keywords, and subject codes if printed; abstract; acknowledgements;
   funding.
2. Divisions, in order, with identifiers (`references/identifiers.md`).
3. Every numbered item (theorem-like blocks, definitions, remarks, equations, figures,
   tables) with its original number, its page, its class (`references/block-classes.md`),
   and its identifier. Unnumbered environments too, marked as such.
4. The numbering scheme, and the `numbering` element that mimics it
   (`references/numbering.md`).
5. Macros and notation (`references/macros.md`).
6. Bibliography entries with identifiers and CSL types (`references/csl-bibliography.md`),
   and their DOIs: `scripts/lookup-dois.py` asks Crossref and then DataCite.
7. Figures and tables. Read `references/figures.md` before describing the figures: how a
   figure is stored in the PDF decides how it is cropped and split. The list of figures
   and panels made here is what the cropping script reads at the start of pass 2.
8. Render risks: anything whose appearance depends on a font feature (a bold or script
   Greek letter, an unusual alphabet, a wide accent).
9. Anything unreadable, with page numbers.
10. What looks wrong in the original, kept as printed.
11. Judgments: decisions the page did not settle, each with its reason.
12. Advice for the authors, added as the passes find it: a construct that is theirs to
    change and that no renderer sets well (a formula too long to stay inline, a list item
    whose only content is a list, a package command that fails inside an environment).
    About structure, never style; short; never applied to the transcription.

Most of PreTeXt is global (identifiers, numbering, macros, the bibliography), and the
manifest is what keeps work done one section at a time consistent. Finish it before
writing any section.

## Pass 2: author, section by section

Read `references/pitfalls.md` first; it is short, and each entry is a mistake already made
once. Then, one file per section in `source/sections/`, with the page images open:

- Prose from the text layer, hyphenation and ligatures repaired, running heads and page
  numbers removed. Never paraphrase.
- Mathematics from the page image (or the LaTeX source). Where a formula is dense, render
  that part of the page again at 300 dpi before trusting a subscript:
  `scripts/pdftool.py zoom transcription/original.pdf N LEFT TOP WIDTH HEIGHT transcription/zoom/NAME.png`,
  the box in the pixels of the 150-dpi page image, where you read it off.
- Symbols that look alike are settled by the PDF, not by eye.
  `scripts/pdftool.py fonts transcription/original.pdf N` prints every line of page N with
  the font of each run of text: text italic or math italic (is the "n" of "n-dimensional"
  mathematics?), a bold digit or a plain one. The text layer's code points tell three
  typed periods (`...`) from `\dots` (". . ."), and a star (U+22C6) from an asterisk
  (U+2217).
- Every block is preceded by a comment with its original number
  (`<!-- Original: Theorem 2.3 -->`); every reference is an `xref`; every citation is an
  `xref` to a `biblio`.
- Verify each element name against the schema (`schema/pretext.rnc` in the PreTeXt clone)
  before using it; `references/article-elements.md` is a map of the ones an article needs.
- A construct listed as a render risk is verified in every built output, or replaced by
  the robust form with the typographic difference recorded. A bold Greek capital written
  with `\mathbf` silently vanishes under xelatex.
- Validate after every section (`scripts/validate.sh <project>`), and correct what it
  reports before going on. Errors are cheap to find one section at a time and expensive
  to untangle at the end. Validation itself does not test whether a reference has a
  target; the script lists the references that have none. One that points into a section
  not yet written stays on that list until the section exists.

## Pass 3: the whole document

1. Every `xref` resolves, and every manifest item is present.
   `scripts/count-items.py <project>` counts the elements of the assembled source that
   validation leaves in `output/validation/`, and lists every reference with no target
   and every bibliography entry never cited. Compare its counts with the manifest's
   tables, not with the manifest's own tallies.
2. `scripts/validate.sh <project>` is clean. `scripts/build.sh <project> html` and
   `scripts/build.sh <project> pdf` succeed, including the glyph check that follows a PDF
   build: no "Missing character" in the build log, no glyph without a character in the
   PDF's text layer. Either one is a character of the source that did not reach the page,
   and a failure.
   The script then lists the overfull boxes of the last LaTeX pass wider than twenty
   points: find each on the page. A build is also refused when PreTeXt's log reports an
   error, which is where a reference with no target shows; PreTeXt itself still exits as
   if all were well.
3. `scripts/compare.py transcription/original.pdf output/print/main.pdf`: record both
   similarities (the whole text, and the text before the reference list, where PreTeXt's
   own ordering of a bibliography entry does not count against the transcription), read
   every run it reports absent (moved text counts as absent), and account for every
   symbol it reports with a lower count in the build.
4. Read every page of the built PDF side by side with the original when the paper is
   short (under about twenty pages); for a longer paper, every page with a display or a
   figure and a sample of the rest. `scripts/pdftool.py render output/print/main.pdf
   transcription/built-pages` makes the page images of the build, as
   `transcription/pages` holds the original's. A single lost glyph cannot be found by
   sampling. Correct what you find, and repeat until a reading finds nothing.
5. The HTML is typeset in the reader's browser, and this skill does not ask for one, so
   it is checked from its files. `scripts/html-outline.py <project>/output/web` lists
   every page's headings, numbers, captions, equation tags, cross-references, footnotes,
   and images, and the title page's authors and abstract. They must agree with the PDF
   you have just read, and no image may be missing.

## Finishing

Do not stop with a list of small known defects for a later pass. Correct what you found
and can correct. What you cannot correct, or what needs a decision from the person you
work for, goes in the notes with the reason.

Finish `transcription/notes.md`: what was done in each pass, the counts from the
assembled source, the comparison's leftovers with each one accounted for, the differences
from the original that remain, and the effort (clock time for each pass).

**Advice for the authors.** A transcription is the one time a paper is set by five
renderers its authors never use, and a few things that are the authors' to change would
set better in every one of them. The manifest's last section collects them; at the end,
hand that section to the person you work for, with its opening sentence, for them to pass
on or not. It is advice, not correction: nothing in it was applied.

**Notes for upstream.** Whenever you had to work something out that this skill should
have told you, or the skill told you something wrong, or PreTeXt itself misbehaved, add an
entry to `transcription/upstream-notes.md` in the form given there. That file is how one
transcription improves the next person's: the skill does not learn unless somebody
carries the lesson back. Three cautions. Sort each entry as the file asks (a gap in the
skill, a defect in PreTeXt, or a peculiarity of this one document), because they go to
different places and the third goes nowhere. The test for a gap in the skill is whether
the same thing would trip the transcription of a different paper by different authors:
one publisher's styling or one author's habit is the document's own, and a rule made
from it would mislead on the next ten papers. When in doubt, it is the document's. Never
quote the document in an entry; show
the construct with a few lines of your own, since the document is not yours to publish.
And at the end, when there are entries of the first two kinds, offer to draft an issue
from those entries only: show the draft, and leave the filing to the person you work for.

## Reference files

| file | read it |
|---|---|
| `references/project-layout.md` | when laying out the project or adding a file to it |
| `references/pitfalls.md` | before pass 2, whole |
| `references/article-elements.md` | when choosing an element |
| `references/block-classes.md` | when classing a theorem, remark, example, and the like |
| `references/identifiers.md` | in pass 1, when naming things |
| `references/numbering.md` | in pass 1, for the publication file |
| `references/macros.md` | in pass 1, for `docinfo/macros`, and when the paper loads a LaTeX package for its notation |
| `references/csl-bibliography.md` | for the bibliography and its DOIs |
| `references/figures.md` | when the paper has figures |
