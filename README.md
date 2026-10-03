# pdf-to-pretext

A skill for [Claude Code](https://claude.com/claude-code) that transcribes a mathematics
research article from its PDF into [PreTeXt](https://pretextbook.org): every word and
every formula as the author wrote them, in PreTeXt's own structure, validated, built to
HTML and PDF, and compared with the original.  From that source PreTeXt makes accessible
HTML, EPUB, braille, and print.

## What you need

- Claude Code.
- The poppler tools (`pdftotext`, `pdftoppm`, `pdftocairo`, and the rest), Python 3.10 or
  newer, `jing`, and a TeX distribution with `xelatex`.
- A clone of [PreTeXtBook/pretext](https://github.com/PreTeXtBook/pretext) and a Python
  with its requirements installed.  The skill runs PreTeXt's own script, `pretext/pretext`,
  and nothing else; it does not use the PreTeXt-CLI.
- For papers with figures: MuPDF's `mutool`, and the Python packages numpy, scipy, Pillow.

The skill's `check-setup.sh` tests for each of these and says how to get what is missing.

## Installing

Clone this repository, and link the skill into Claude Code's skills directory, so that a
correction you make is in a working tree and can be sent back:

```
git clone REPOSITORY-URL ~/src/pdf-to-pretext
mkdir -p ~/.claude/skills
ln -s ~/src/pdf-to-pretext/skill/pdf-to-pretext ~/.claude/skills/pdf-to-pretext
```

Get PreTeXt and a Python for it:

```
git clone https://github.com/PreTeXtBook/pretext ~/src/pretext
python3 -m venv ~/src/pretext-venv
~/src/pretext-venv/bin/pip install -r ~/src/pretext/pretext/requirements.txt
```

Tell the skill where they are, in the file `config.local` in the skill's directory, and
check:

```
cat > ~/src/pdf-to-pretext/skill/pdf-to-pretext/config.local <<EOF
PRETEXT_HOME=$HOME/src/pretext
PRETEXT_PYTHON=$HOME/src/pretext-venv/bin/python3
EOF
~/.claude/skills/pdf-to-pretext/scripts/check-setup.sh
```

The check ends with a trial run: it lays out the skill's template, validates it, and
builds it to HTML and to PDF.  When it says "Ready", it is.

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

The skill as it now stands was then given to two fresh sessions with nothing but the
skill and a test document each; both transcriptions matched their keys, and what those
sessions had to work out for themselves has gone into the skill.

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
