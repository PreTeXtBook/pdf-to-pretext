# pdf-to-pretext

A skill for [Claude Code](https://claude.com/claude-code) that transcribes a mathematics
research article from its PDF into [PreTeXt](https://pretextbook.org): every word and
every formula as the author wrote them, in PreTeXt's own structure, validated, built to
HTML and PDF, and compared with the original.  From that source PreTeXt makes accessible
HTML, EPUB, braille, and print.

## What you need

- Claude Code: you can type `claude` at a terminal.
- A TeX distribution with `xelatex`.  If it is missing, the skill gives you the one
  command that installs it.

That is all.  The first time it is used, the skill gets PreTeXt itself and builds a
Python environment for it, in `~/.local/share/pdf-to-pretext`, and it keeps both up to
date.  It runs PreTeXt's own script, `pretext/pretext`, and it reads PDFs with PyMuPDF,
which is among PreTeXt's own requirements.

## Installing

Claude Code looks for skills in `~/.claude/skills/`.  The skill is the directory
`skill/pdf-to-pretext` of this repository.  Put it there as a copy or as a link.

**A copy** is the simplest.  Clone the repository anywhere (or download it as a zip
file), and copy the one directory:

```
git clone REPOSITORY-URL
mkdir -p ~/.claude/skills
cp -r pdf-to-pretext/skill/pdf-to-pretext ~/.claude/skills/
```

To update a copy, get the repository again and copy the directory again.

**A link** keeps the skill in step with a clone, and is the one to choose if you might
send a correction back, since a change you make is then in a working tree:

```
git clone REPOSITORY-URL ~/src/pdf-to-pretext
mkdir -p ~/.claude/skills
ln -s ~/src/pdf-to-pretext/skill/pdf-to-pretext ~/.claude/skills/pdf-to-pretext
```

To update a link, `git pull` in the clone.

Either way the skill is then available in every directory.  To have it in one project
only, put the copy or the link in `.claude/skills/` inside that project's directory
instead.

There is nothing more to install by hand.  If you would like to see it get ready before
you give it a paper, run `~/.claude/skills/pdf-to-pretext/scripts/setup.sh`: it gets
PreTeXt, builds the Python environment, checks for TeX, and builds a small trial
article.  When it says "Ready", it is.

If you already keep a clone of PreTeXt and want the skill to use it, name it and its
Python in a file `config.local` in the skill's directory (`PRETEXT_HOME=...` and
`PRETEXT_PYTHON=...`, one to a line).  The skill then leaves both alone.

## A first transcription

In the directory where you want the result, start Claude Code and say:

```
Use the pdf-to-pretext skill to transcribe the PDF at <path> into a new directory <name>.
Tell me its license before you begin.  Do pass 1 and show me the manifest before going on.
```

Read the manifest it writes (`<name>/transcription/manifest.md`).  It lists every
division, numbered item, equation, figure, and bibliography entry of the paper, with the
decisions the page did not settle.  Correct anything there, then say "on to pass 2".  The
transcription ends with the source validated, HTML and PDF built, and the built PDF
compared with the original.

## What you get

```
<name>/
    source/           the PreTeXt: main.ptx and one file per section
    publication/      the publication file (numbering)
    assets/           the figures, cropped from the pages
    output/web        the HTML build
    output/print      the PDF build
    transcription/    the manifest, the notes, the original, its page images
    project.ptx       so that an author who uses the PreTeXt-CLI can carry on from here
```

The layout is the PreTeXt-CLI's.  `examples/sylow-subgraphs` is a complete transcription
of a ten-page article, with its manifest and its notes.

## Rights

A transcription is a derivative work of the paper.  Whether you may distribute it depends
on the paper's license or on its author's permission, not on this skill.  The skill finds
the license and tells you before it starts, and the project's `.gitignore` keeps the
original and its page images out of version control.  The license of this repository
covers the skill, not what you transcribe with it.

## What it has been tried on

Four papers so far, of 10 to 28 pages, all typeset with LaTeX, all with a text layer and
a single column, one of them with 33 figures.  Each took a quarter of an hour to an hour of machine time
and several hundred thousand tokens.  On the one paper checked against its LaTeX source,
the transcription made from the PDF alone had no error of words or of mathematics
(`notes/2026-10-03-pdf-only-versus-latex.md`).

The skill was then given, twice, to two fresh sessions with nothing but the skill and a
test document each.  All four transcriptions matched their keys, and what those sessions
had to work out for themselves has gone into the skill.

It has not been tried on scanned PDFs (it needs a text layer), two-column layouts, books,
or documents not made with LaTeX.  It is for articles.

## When the skill is wrong

It will be, on some construct nobody has met yet.  While it works, the skill writes
`transcription/upstream-notes.md`: what it had to work out for itself, sorted into gaps
in the skill, defects in PreTeXt, and peculiarities of your one document.  At the end it
offers to draft an issue from the first two kinds.  Please send it: that file is how one
person's transcription improves the next person's.  `CONTRIBUTING.md` says what makes a
report or a change easy to accept.

## This repository

| | |
|---|---|
| `skill/pdf-to-pretext/` | the skill: `SKILL.md`, its reference files, scripts, and templates |
| `examples/` | a worked example |
| `corpus/round-trip/` | small articles written as test cases; `tests/run.sh` checks them |
| `tests/` | the checks that need no model, and the comparison of a transcription with its key |
| `corpus/MANIFEST.md`, `evaluation/`, `notes/` | the documents the skill was developed on, their scores, and reports |
| `CLAUDE.md`, `TRANSITION.md` | the maintainers' working rules and state of work; not needed to use the skill |

## License

GNU General Public License, version 2 or version 3, the license of PreTeXt itself.  See
`COPYING` and the directory `legal`.
