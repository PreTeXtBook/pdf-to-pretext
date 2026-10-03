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
