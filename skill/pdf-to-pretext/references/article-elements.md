# PreTeXt elements for a research article

This list is a map, not the authority.  The authority is `schema/pretext.rnc` in the
PreTeXt clone: verify each name there before using it (`grep -n 'element NAME ' pretext.rnc`).
PreTeXt changes; this list was last checked on 2026-10-03 against commit `bf795ab1`.

- Root: `pretext` (`@xml:lang="en-US"`), `docinfo` (`macros`), `article` (`title`).
- Front matter, in this order: `frontmatter/bibinfo` with `author` (`personname`,
  `institution`, `email`; an `institution` printed on several lines holds `line`s),
  `date`, `keywords` (`@authority="msc"`, `@variant` for the year, `keyword`s), `support`;
  `frontmatter/titlepage` holding an empty `titlepage-items` (required);
  `frontmatter/abstract` with `p`s.
- Divisions: `section`, `subsection`, `subsubsection`, each with `@xml:id` and `title`;
  an `introduction`/`conclusion` inside a sectioned division when the paper has text
  before its first subsection.
- Blocks: see `block-classes.md`.  Theorem-like: `statement` then `proof`s (a `proof` may
  carry a `title`, or `@ref` when detached from its theorem).  `definition`,
  `remark`-class, `axiom`-class, `example`-class, `openproblem`-class as mapped there.
  In a block's heading, `creator` is an attribution ("Hadamard") and `origins` holds the
  `xref`s to where it comes from.  A `paragraphs` (a titled run of text) may hold
  theorem-like blocks, proofs, and figures.
- Mathematics: `m` inline; `md` display — a single line with `@number="yes"` when the
  original numbers it, or `mrow` children (each with `@number`) for aligned lines;
  `intertext` between rows.  Reference a numbered line by its `@xml:id`.
- Cross-references: `xref` with `@ref` (or `@first`/`@last` for a range), `@text` to choose
  the style, `@detail` for a pinpoint.
- Figures: `figure` (`caption`) around `image` (`@source`, `@width`) with `description`
  or `shortdescription`; several graphics side by side: `sidebyside` with one panel each
  (two panels or more), inside one `figure` when they share a caption; `sbsgroup` for
  rows of them.  See `figures.md`.
- Tables: `table` (`title`) around `tabular` (`row`/`cell`, `col` widths, `@halign`).
- Text: `p`, `em`, `term` (a defined term), `q` and `sq` (double and single quotation
  marks), `ndash`, `mdash`, `nbsp`, `ellipsis`, `fn`, `ul`/`ol` with `li`, `url`,
  `blockquote`, `articletitle` and `pubtitle` (a title cited in prose), `notation` (feeds
  a notation list), `idx` (index entries, optional in a paper).
- Back matter: `backmatter/references` with `biblio` entries (see `csl-bibliography.md`).
- Acknowledgements: an `article` has no `acknowledgement` element (that is a book's front
  matter) and no unnumbered division.  An unnumbered "Acknowledgements" section is a
  `paragraphs` with that `title`, closing the last section.
