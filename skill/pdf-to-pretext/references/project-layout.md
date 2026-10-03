# The layout of a transcription

`scripts/new-transcription.sh <paper.pdf> <directory> <model-id>` makes this:

```
<directory>/
    project.ptx                   manifest for the PreTeXt-CLI (not used by the skill)
    source/
        main.ptx                  docinfo, front matter, one xi:include per section
        sections/
            section-<words>.ptx   one file per section of the original
            references.ptx        the bibliography
    publication/
        publication.ptx           numbering; where generated files are
    assets/                       cropped figures and any other file the source names
    generated-assets/             what PreTeXt generates from the source (PreFigure, ...)
    output/
        web/                      scripts/build.sh <directory> html
        print/                    scripts/build.sh <directory> pdf   (main.pdf, build.log)
        web-work/, print-work/    PreTeXt's working files for each build (the LaTeX source
                                  and its log are here when a PDF build fails)
        validation/               scripts/validate.sh <directory>   (the report, and the
                                  assembled source that count-items.py reads)
    transcription/
        original.pdf              the document being transcribed
        original.txt              its text layer, layout kept
        pages/                    page-1.png, page-2.png, ... at 150 dpi (page-01.png
                                  and so on when there are ten pages or more)
        manifest.md               pass 1
        notes.md                  header, effort, what was done, what remains
        upstream-notes.md         what the skill should learn from this document
    .gitignore                    keeps builds and the original out of version control
```

The names are the PreTeXt-CLI's, so that an author who works with the CLI can carry on
from the result: `project.ptx` declares the targets `web` and `print`, which write where
the skill's builds write.  The skill itself never runs the CLI.  It validates and builds
with PreTeXt's own script, through `scripts/validate.sh` and `scripts/build.sh`.

Things to know:

- The scaffold is for a paper with an introduction and a bibliography.  Rename
  `section-introduction.ptx` when the first section is called something else, add a file
  and an `xi:include` for each further section, and take the `backmatter` and
  `references.ptx` out when the paper has no bibliography.

- The directory of external files is declared in `docinfo` (`source/main.ptx`), as
  `../assets`, relative to the main file.  The directory of generated files is declared in
  the publication file, as `../generated-assets`.
- `image/@source` names a file in `assets/` without an extension when both an SVG and a
  PDF of it are there: HTML takes the SVG, LaTeX the PDF.
- `scripts/build.sh` does not empty an output directory.  For a build from nothing, name
  another one as its third argument.  PreTeXt's HTML build downloads some of its static
  files, so it needs the network.
- PreTeXt's change of 2026-07-30 moved the declaration of the external directory from
  the publication file to `docinfo`, and the template follows it.  A CLI that carries an
  older PreTeXt may not find the figures; if so, add `external="../assets"` to the
  `directories` element of the publication file.
- A second publication file for another style of the same source (a journal's, say) sits
  beside the first; build it with
  `scripts/build.sh source/main.ptx publication/<other>.ptx pdf <output-directory>`.
- Anything you make while working goes in `transcription/`, never in `source/` or
  `assets/`: crops at 300 dpi in `zoom/`, the figure specification `figure-spec.json`
  and the cropping script's `crop-work/`, lookup results.
- The `.gitignore` leaves out `transcription/original.pdf`, its text, its page images, and
  the renderings in `zoom/` and `crop-work/`.
  They belong to the document's rights holder; take those lines out only when the
  document's license allows redistribution.
