# Contributing

The skill improves when a transcription that went wrong somewhere is carried back.  This
file says how to carry it back so that it can be accepted quickly.

## What to send

**A report.**  The skill keeps `transcription/upstream-notes.md` in every project and
offers to draft an issue from it.  An entry there already has the form wanted: what the
skill says now, what happened, what was done, and the change proposed.

**A change.**  A pull request with the corrected sentence, script, or template, and a
case that shows it (below).

**A case.**  A small article that exercises something the skill gets wrong or has never
met.  A case with no fix is still welcome: it is the hard half.

## Never an excerpt of a paper

Do not put a page, a crop, a sentence, or a formula of someone's paper in an issue, a
pull request, or a case.  It is not yours to publish, and it is not needed.  Describe the
construct, or write a few lines of your own that show it.  Three lines of invented text
around a display that overruns the margin show the problem as well as the paper did.

## Which kind of problem it is

- **The skill** lacks something or says it wrongly: this repository.
- **PreTeXt** misbehaves (a build fails on valid source, an element renders wrongly): the
  issue belongs at [PreTeXtBook/pretext](https://github.com/PreTeXtBook/pretext), with a
  minimal source.  A note here that the skill should warn about it is still useful.
- **One document's peculiarity** (a publisher's own theorem styling, an author's private
  macros): probably not for the skill.  A rule that fits one document and misleads on the
  next ten does harm.  Say so if you think it is commoner than it looks.

## Cases

A case is a directory in `corpus/round-trip`:

```
corpus/round-trip/<name>/
    source/main.ptx              the PreTeXt, which is also the right answer
    publication/publication.ptx
    figures/<picture>.tex        optional: standalone LaTeX files that draw the pictures
```

The source is built to PDF by PreTeXt, the PDF is what a transcription starts from, and
the source is the key the transcription is compared with.  So a case is written in
PreTeXt, by you, and is exact by construction.

- Write it yourself.  Invented people, places, and publications; mathematics too simple
  to be anyone's.
- Keep it small: one or two pages, one thing exercised and named in the comment at the
  top of `main.ptx`.
- It must validate with no message and build: `tests/run.sh` checks every case.

What a PDF built by PreTeXt cannot show is the look of another typesetting: a journal's
class, a two-column page, a remark set in upright type with nothing to mark its end.  For
those, describe the layout in the issue, in your own words.  A way to keep such cases is
wanted.

## Before sending a change

```
tests/run.sh
```

It checks the setup, the skill's template, every case (validation, the HTML and PDF
builds, the glyph check, both comparison scripts), the worked example, and the figure
cropping script against 58 boxes it has to leave where they are.  It needs no model and
takes a few minutes.  Run it too when PreTeXt has moved: the schema changes, and a template that was
valid last month may not be now.

## Scoring the skill on a case

This takes a model run, so it is done by hand, on the cases a change could affect.

1. `tests/run.sh` builds each case's PDF at `corpus/round-trip/<name>/output/print/main.pdf`.
   Copy it somewhere outside the repository.
2. In a fresh Claude Code session that has not seen the case, have the skill transcribe
   that copy into a new directory.  Tell it not to read `corpus/`.
3. Compare the result with the key:

   ```
   tests/compare-transcriptions.py <new directory>/source/main.ptx \
       corpus/round-trip/<name>/source/main.ptx <a directory for the diffs>
   ```

   It reports structure, words, and formulas.  Formulas are compared after a short list of
   equivalences (two spellings of one symbol, redundant braces, spacing), so what it lists
   as still different is what to read.

Say in the pull request which cases you scored and what the comparison printed.

## Where a change goes

- A mistake to avoid: one entry in `skill/pdf-to-pretext/references/pitfalls.md`, under
  the heading it fits.
- An element or a convention: the reference file for that subject.
- `SKILL.md` is the procedure and is kept short.  A change there should be a change to
  the procedure.
- Explain why.  The skill is read by a model that follows reasons better than orders.

## What the skill will not take on

- PreTeXt is run through its own script only.  The project a transcription produces is
  laid out as the PreTeXt-CLI lays one out, but the skill does not process with the CLI.
- No step that needs a web browser or any tool beyond those `check-setup.sh` lists.
- No correcting of authors, and nothing added to a transcription that its document does
  not print, DOIs in the bibliography excepted.

## License

Contributions are accepted under the license of the repository: the GNU General Public
License, version 2 or version 3 (`COPYING`).
