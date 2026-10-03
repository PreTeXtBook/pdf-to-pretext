# Worked example: a ten-page article with one figure

Robert A. Beezer, "Sylow Subgraphs in Self-Complementary Vertex Transitive Graphs", in the
version submitted on December 30, 2004.  The published version is Expositiones
Mathematicae 24 (2006) 185-194, <https://doi.org/10.1016/j.exmath.2005.09.003>.

The author permits the redistribution of this transcription.  The PDF it was made from is
not here.

It was transcribed from the PDF alone on 2026-09-03; the LaTeX source was not opened.
Every word, formula, block, and reference of the original is present (54 of 54 numbered
and listed items), every number agrees with the original's, and in the comparison of the
built PDF with the original 97.9 percent of the words pair up (what does not is the
bibliography's formatting, running heads, and mathematics, which extracts as noise).
The notes say 0.958: that was measured when the text was extracted by another program.

## What to read

- `transcription/manifest.md` is pass 1: the survey of the whole paper, made before any
  section was written.  It is the best picture of what the skill asks for.
- `transcription/notes.md` is the working log, including a mistake.  A bold capital gamma
  vanished from the built PDF and was not noticed, because only some pages were read; the
  account of why is in the notes, and the glyph check in `scripts/build.sh` and the rule
  to read every page of a short paper both come from it.
- `source/` is the PreTeXt: `main.ptx` and one file per section.
- `publication/publication-ams.ptx` builds the same source in PreTeXt's style for AMS
  journals.
- The figure was first cropped from the page (`assets/`) and later redrawn as a PreFigure
  diagram, which is what the source now holds.  The generated diagram is included in
  `generated-assets/`, so the example builds without PreFigure installed.

The working papers are as they were written.  The skill then laid a transcription out
differently (`main.ptx` beside `sections/`, figures in `external/`, a run directory in
the maintainers' `runs/`), and the paths in the papers are of that time.

## Building it

From the root of the repository:

```
skill/pdf-to-pretext/scripts/validate.sh examples/sylow-subgraphs
skill/pdf-to-pretext/scripts/build.sh examples/sylow-subgraphs html
skill/pdf-to-pretext/scripts/build.sh examples/sylow-subgraphs pdf
```

The builds go to `examples/sylow-subgraphs/output/`.
