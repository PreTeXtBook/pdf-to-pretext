# Author macros

Keep in `docinfo/macros` only what is semantic and MathJax-compatible; both the LaTeX and
the HTML conversions read that block.

- Keep: `\newcommand{\R}{\mathbb{R}}`, `\newcommand{\norm}[1]{\lVert #1\rVert}`,
  `\DeclareMathOperator{\Re}{Re}` — meaning-carrying, argument counts fixed.
- Drop (expand inline): spacing and layout (`\medskip`, `\vspace`, `\linebreak`, `\noindent`),
  anything defined with `\def` and delimiters, anything conditional, anything that reaches
  outside mathematics.
- A macro redefined anywhere in the paper is expanded inline everywhere; a macro used
  in exactly one place is expanded inline.
- Record every macro in the manifest with keep/expand and the reason.  Give up easily.
- With only the PDF at hand the author's macros cannot be seen.  Leave `docinfo/macros`
  empty, write every notation out in forms both MathJax and LaTeX accept
  (`\operatorname{conv}`, `\mathbb{R}`), and list the forms in the manifest so that every
  section writes a notation the same way.  Do not invent macros of your own.

## A notation from a LaTeX package

A paper may take its notation from a LaTeX package that MathJax does not have: a
specialist package with a font of its own, often not in TeX Live.  Loading the package is
no answer.  `docinfo/math-package` puts it in the LaTeX only; `docinfo/macros` goes to
LaTeX and to MathJax alike, so MathJax cannot be given a definition of its own without
colliding with the package in LaTeX; and every reader of the source would have to install
the package by hand.  Replace the package by a handful of macros instead.

- Find which of its commands the paper uses (from the source; with only the PDF, from the
  symbols on the page) and read what each one does in the package's code.  A paper that
  loads a large package usually uses two or three of its commands.
- Define each in `docinfo/macros` from what LaTeX and MathJax both have, under the
  package's own name when it is a symbol: `\newcommand{\cgstar}{{\ast}}` for a package
  that sets the star as an ordinary symbol.
- A command that works by a catcode trick (an active character, as a package that scales
  the bar in a game `{ L | R }` to the height of the braces does) cannot be a macro in
  MathJax.  Write what it produces, with a macro for the part that recurs:
  `\left\{ L \cgslash R \right\}` with `\newcommand{\cgslash}{\;\middle|\;}`, the
  package's own name for that bar.
- A symbol no standard font has is built from pieces:
  `\newcommand{\cglfuz}{\mathrel{\lhd\mkern2mu\rule[-0.03em]{0.045em}{0.58em}}}` for a
  triangle with a short bar beside it.  Try every built symbol in both outputs before
  writing a section: the two fonts differ in their side bearings, so a kern that is right
  in LaTeX is loose in MathJax or the other way round, while a `\rule` has no bearings and
  sets the same in both.  Look at the result on a built page at the size it will be read:
  a bar kerned too close to a triangle merges with it at 150 dpi and reads as a different
  relation.
- Record each command in the manifest's table of macros: the package, what the command
  did, and what stands for it.

Where the package itself fails in the original (a command that cannot act inside an
environment that reads its body before the command runs, so the same construct prints two
ways), the transcription renders what the package intends, everywhere: a difference of
typography, recorded in the manifest among the things that look wrong in the original.
