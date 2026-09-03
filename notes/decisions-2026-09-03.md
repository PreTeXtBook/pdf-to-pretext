# Decisions, 2026-09-03 (Rob, in conversation)

- Input policy: a mix of PDF-only and PDF+LaTeX documents.
- Fidelity: preserve content verbatim; fully PreTeXt-native; numbering may differ;
  cross-references are `xref`s.  Principle recorded in CLAUDE.md.
- Identifiers: semantic (author-memorable), never mechanical; original numbers as XML
  comments before each element.  Idea for later: surface those original numbers to a
  reader as metadata (a PreTeXt enhancement, not part of this project yet).
- Corpus: publicly available documents or with permission; local repository now, public later.
- Audience: Claude Code first; builds with the `pretext/pretext` script from a dedicated
  clone kept current with `git pull`; CLI-compatible source later.
- Finish line: valid PreTeXt, no glaring omissions or garbled text, at most minor hand
  editing for a faithful replica.
- Macros: semantic only, MathJax-compatible, give up easily.  References: CSL-style.
  Figures: split composites into `sidebyside`; PreFigure as a bonus.  Tables: Claude does them.
- Every run records the model version.
- First document: arXiv 2010.15608; never read its HTML rendering.
