# Numbering (publication file `numbering` element, from `schema/publication-schema.rnc`)

Children, each optional: `divisions` (`@level`, `@chapter-start`, `@part-structure`),
`blocks` (`@level`, required), `projects`, `figures`, `exercises`, `openproblems`
(each `@level`, `@distinct`), `equations` (`@level`, required), `footnotes` (`@level`).
Levels count structural divisions: in an article, `0` numbers globally, `1` within sections,
`2` within subsections.

`divisions/@level` is how deep the numbered divisions go: `1` for sections only, `2`
for sections and subsections.

Reading a paper's scheme from its pages (the LaTeX that usually lies behind each is in
parentheses, for when the source is at hand):

- Theorem 2.1, Lemma 2.2, Remark 2.3 in one run, starting again in each section: blocks
  on one counter within sections, PreTeXt's own habit, `<blocks level="1"/>`
  (`\newtheorem{theorem}{Theorem}[section]` with siblings sharing its counter).  One run
  through the whole paper, Theorem 1 to Remark 11: `<blocks level="0"/>`.
- Equations (2.1), (2.2): `<equations level="1"/>` (`\numberwithin{equation}{section}`).
  Equations (1), (2) through the paper: `level="0"`.
- Figures and tables are usually numbered through the whole paper, each on its own
  counter.  PreTeXt's `figures` covers figures, tables, and listings on one shared
  counter; `@distinct="yes"` keeps that counter separate from the theorem-like blocks
  (without it, figures and theorems share one).  A paper's separately numbered tables
  will not agree (Table 5.1 becomes Table 5.2 after Figure 5.1): record the mismatch;
  PreTeXt wins.
- Theorem 1, Lemma 1, Theorem 2: a counter for each kind (`\newtheorem{lemma}{Lemma}`).
  This cannot be reproduced: PreTeXt shares one counter across a level.  Record the
  mismatch in the manifest; the fidelity principle says PreTeXt wins.

Every element keeps its original number as an XML comment immediately before it,
`<!-- Original: Lemma 3.2 -->`, whatever PreTeXt ends up printing.
