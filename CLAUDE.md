# pdf-to-pretext — project rules

Transcribing research articles in mathematics from PDF into PreTeXt source.  The end
product is the Skill in `skill/pdf-to-pretext/`, refined on the documents in `corpus/`.
The global rules in `~/.claude/CLAUDE.md` apply here unchanged.

## The fidelity principle

Fully PreTeXt-native.  A difference from the original is acceptable when it changes
neither content nor meaning: numbering, the wording of a reference ("Section 5.2"
becomes an `xref` and PreTeXt supplies "Section"), placement of floats, typography.
Words, mathematics, and structure are never such differences.

## Inputs, and what is never an input

- The PDF is always an input.  When LaTeX source exists (arXiv e-print), it is the primary
  text for words and mathematics and the PDF is the visual check.  Every PDF+LaTeX document
  is ALSO transcribed once from the PDF alone, so the hard path is scored against a key.
- The words of a PDF-only document come from `pdftotext`; the mathematics and the structure
  come from reading the rendered page images.  Never guess a formula: an unreadable spot
  gets an XML comment `<!-- UNREADABLE: page N, ... -->` and a line in the run notes.
- Never consult an HTML rendering of a paper (arXiv HTML, ar5iv, a journal's HTML view).

## Decisions already made (Rob, 2026-09-03)

- Identifiers are semantic, the kind an author would remember when editing
  (`theorem-real-zeros`, `lemma-degree-bound`), full words, no abbreviations.  The original
  numbering is preserved as an XML comment immediately before the element:
  `<!-- Original: Theorem 2.3 -->`, `<!-- Original: (4.1) -->`, `<!-- Original: Section 5 -->`.
- Cross-references are `xref`s; PreTeXt supplies the "Section"/"Theorem" word and the number.
- Numbering: mimic the original's levels in the publication file where PreTeXt allows;
  where PreTeXt's scheme is more constrained, PreTeXt wins.  Agreement with the original
  numbers is a happy accident, not a requirement.
- Author macros go in `docinfo/macros` when they are semantic (`\R`, `\norm{}`), never when
  presentational (spacing, breaks).  Both LaTeX and MathJax read them, so only forms
  MathJax accepts.  A macro redefined mid-paper is expanded inline everywhere.  Give up easily.
- Bibliographies use the CSL-style `biblio` (`@type` from the CSL vocabulary, fields in the
  canonical order); citations are `xref`s; DOIs recovered when findable.
- Figures: a composite graphic is split into `sidebyside` panels; each image is cropped
  from the PDF page with `pdftocairo` to SVG and gets a description written from the image.
  Recreation in PreFigure is a later bonus.  Tables become `tabular`; Claude does them.
- Every run records, at the top of its notes: date, model id, Claude Code version, and
  the commit of `pretext/` used to build.

## The three passes

1. Survey the whole document and write the manifest (`runs/<date>-<name>/manifest.md`):
   divisions; every numbered item with its original number and proposed id; equations;
   figures and tables; bibliography keys; macros with keep/expand decisions; notation.
   Much of PreTeXt is global — the manifest is what keeps section-by-section work consistent.
2. Author section by section against the manifest.
3. Whole-document passes: resolve every `xref`, validate, build HTML and PDF, compare with
   the original (`scripts/compare.py`), read sample pages side by side, record the score.

## Building and validating

`pretext/` is a dedicated clone of PreTeXtBook/pretext, kept current with
`git -C pretext pull --ff-only`.  **Pull before every new task, not just once per session:**
a fresh paper, or an update or rebuild of an earlier run (Rob, 2026-09-23, after the scvt
demonstration was rebuilt on a clone 26 commits behind).  Record the commit in the run
notes, as the decisions above require.  Use the in-repo script through the
venv; never pretext-cli, never raw `xsltproc`.  Output directories go under `/tmp`
(`mkdir -p` first); always pass `-p`:

```
mkdir -p /tmp/pdf-to-pretext/<name>-html && \
/home/rob/.claude/pretext-venv/bin/python3 pretext/pretext/pretext -vv -c doc -f html \
    -p runs/<run>/publication.ptx -d /tmp/pdf-to-pretext/<name>-html runs/<run>/main.ptx
```

Validation: the same script with `-V full` in place of `-c doc -f html`; it writes
`<name>-validation.txt` (line numbers refer to the assembled file).  `scripts/build.sh` and
`scripts/validate.sh` wrap both.  Verify every element name against
`pretext/schema/pretext.rnc` before using it; `me`, `men`, `mdn` no longer exist —
display math is `md` (with `@number` for a single numbered line, `mrow`s for several).

## Working style

- Ask before creating, deleting, or restructuring anything outside `runs/`.
- Never type `rm`.  A dirty output directory gets a new name.
- Commits: subject line, blank line, one `Co-Authored-By: Claude <MODEL> <noreply@anthropic.com>`
  line.  No body, no session link, ever.  Full words in subjects.
- Keep `notes/` for findings worth keeping across sessions; `TRANSITION.md` is the hand-off
  document — update it at the end of a session.
