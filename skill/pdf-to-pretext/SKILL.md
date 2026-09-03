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
6. Bibliography entries with identifiers and CSL types (`references/csl-bibliography.md`).
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
- Every block preceded by its original-number comment; every reference an `xref`; every
  citation an `xref` to a `biblio`.
- Element names verified against the schema (`references/article-elements.md`).
- Validate after every division (`scripts/validate.sh`); fix before moving on.

## Pass 3 — the whole document

1. Every `xref` resolves; every manifest item is present (count them).
2. `scripts/validate.sh` clean; `scripts/build.sh` to HTML and to PDF succeed.
3. `scripts/compare.py <original.pdf> <built.pdf>`: record the similarity and read every
   run it reports missing.
4. Read three sample pages side by side with the original, one of them dense with
   mathematics; fix what you find; repeat until a pass finds nothing.
5. Record the run in `evaluation/RESULTS.md`; finish `notes.md` with what was hard and
   what this skill should say differently next time.

## Pitfalls

Two-column layouts interleave in extraction; footnotes float; ligatures (`fi`, `fl`)
come out as single characters; end-of-line hyphens split words; `--` and quotation marks
need their PreTeXt elements; a "Notation" or "Remark" environment is often unnumbered;
a named theorem keeps its name as a `title`; "Proof of Theorem 3" is a titled `proof`;
lettered main theorems ("Theorem A") cannot be lettered by PreTeXt — keep the letter in
the title and the comment.
