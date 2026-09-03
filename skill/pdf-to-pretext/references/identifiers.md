# Identifiers

- Semantic, author-memorable, full words: `theorem-real-zeros-derivative`,
  `lemma-degree-bound`, `equation-fourier-product`, `section-entire-functions`,
  `figure-nonreal-roots-one`, `biblio-polya-collected`.
- Prefix with the element kind, then two to four words from the statement or title.
- Fixed in the manifest during pass 1, before any section is written, so every `xref`
  written in pass 2 already has its target.
- The original number lives in a comment immediately before the element:
  `<!-- Original: Theorem 2.3 -->`; for a display equation `<!-- Original: (2.4) -->`;
  for a division `<!-- Original: Section 4.1 -->`; for an unnumbered environment
  `<!-- Original: unnumbered Remark, page 7 -->`.
- Idea recorded 2026-09-03: make those original numbers available to a reader as
  metadata — a PreTeXt enhancement for later, not part of the Skill.
