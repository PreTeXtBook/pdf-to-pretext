# Numbering (publication file `numbering` element, from `schema/publication-schema.rnc`)

Children, each optional: `divisions` (`@level`, `@chapter-start`, `@part-structure`),
`blocks` (`@level`, required), `projects`, `figures`, `exercises`, `openproblems`
(each `@level`, `@distinct`), `equations` (`@level`, required), `footnotes` (`@level`).
Levels count structural divisions: in an article, `0` numbers globally, `1` within sections,
`2` within subsections.

Reading a LaTeX paper's scheme:

- `\newtheorem{theorem}{Theorem}[section]` and siblings sharing its counter: blocks
  numbered within sections on one counter — `<blocks level="1"/>`, PreTeXt's own habit.
- `\numberwithin{equation}{section}`: `<equations level="1"/>`; absent: `level="0"`.
- Figures and tables: LaTeX numbers them globally unless told otherwise, on separate
  counters.  PreTeXt's `figures` covers figures, tables, and listings on one shared
  counter; `@distinct="yes"` keeps that counter separate from the theorem-like blocks
  (without it, figures and theorems share one).  A paper's separately numbered tables
  will not agree (Table 5.1 becomes Table 5.2 after Figure 5.1): record the mismatch;
  PreTeXt wins.
- Separate counters per environment (`\newtheorem{lemma}{Lemma}`) cannot be reproduced:
  PreTeXt shares one counter across a level.  Record the mismatch in the manifest; the
  fidelity principle says PreTeXt wins.

Every element keeps its original number as an XML comment immediately before it,
`<!-- Original: Lemma 3.2 -->`, whatever PreTeXt ends up printing.
