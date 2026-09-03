# PreTeXt elements for a research article

Verify each against `pretext/schema/pretext.rnc` before use (`grep -n 'element NAME {'`);
this list is a map, not the authority.  Names in effect 2026-09-03.

- Root: `pretext` (`@xml:lang="en-US"`), `docinfo` (`macros`), `article` (`title`).
- Front matter: `frontmatter/bibinfo` with `author` (`personname`, `institution`, `email`),
  `date`, `keywords` (`@authority="msc"`, `@variant` for the year, `keyword`s), `support`;
  `frontmatter/abstract` with `p`s.
- Divisions: `section`, `subsection`, `subsubsection`, each with `@xml:id` and `title`;
  an `introduction`/`conclusion` inside a sectioned division when the paper has text
  before its first subsection.
- Blocks: see `block-classes.md`.  Theorem-like: `statement` then `proof`s (a `proof` may
  carry a `title`, or `@ref` when detached from its theorem).  `definition`,
  `remark`-class, `axiom`-class, `example`-class, `openproblem`-class as mapped there.
- Mathematics: `m` inline; `md` display — a single line with `@number="yes"` when the
  original numbers it, or `mrow` children (each with `@number`) for aligned lines;
  `intertext` between rows.  Reference a numbered line by its `@xml:id`.
- Cross-references: `xref` with `@ref` (or `@first`/`@last` for a range), `@text` to choose
  the style, `@detail` for a pinpoint.
- Figures: `figure` (`caption`) around `image` (`@source`, `@width`) with `description`
  or `shortdescription`; several graphics side by side: `sidebyside` with one panel each,
  inside one `figure` when they share a caption.
- Tables: `table` (`title`) around `tabular` (`row`/`cell`, `col` widths, `@halign`).
- Text: `p`, `em`, `term` (a defined term), `q`, `fn`, `ul`/`ol` with `li`, `url`,
  `notation` (feeds a notation list), `idx` (index entries — optional in a paper).
- Back matter: `backmatter/references` with `biblio` entries (see `csl-bibliography.md`);
  `acknowledgement` in the front matter.
