#!/usr/bin/env python3
"""Write references/block-classes.md from PreTeXt's xsl/entities.ent.

Usage: block-classes.py <entities.ent> <output.md>

The "-LIKE" entities are PreTeXt's own definition of which elements behave
alike; the transcription maps a paper's environments onto these classes.
"""
import re
import sys


def main(entities_path, output_path):
    text = open(entities_path, encoding="utf-8").read()
    classes = re.findall(r'<!ENTITY ([A-Z]+)-LIKE "([^"]*)">', text)
    lines = ["# Block classes (generated from `xsl/entities.ent`)", "",
             "PreTeXt's own list of which elements behave alike.  (For maintainers: regenerate "
             "with `scripts/block-classes.py <clone>/xsl/entities.ent references/block-classes.md` "
             "when the clone has moved.)", "",
             "| class | elements |", "|---|---|"]
    for name, union in classes:
        lines.append("| {} | {} |".format(name.lower(),
                     ", ".join("`{}`".format(e) for e in union.split("|"))))
    lines += ["",
              "## Mapping a paper's environments",
              "",
              "- Theorem, Lemma, Corollary, Proposition, Claim, Fact, Algorithm: the theorem "
              "class, with a `statement` and then its `proof`s.",
              "- Definition: `definition`, with a `statement`.  Conjecture, Principle, Hypothesis, "
              "Assumption, Axiom: the axiom class (a `statement` never followed by a proof).",
              "- Remark, Note, Observation, Warning, Convention: the remark class, which holds its "
              "paragraphs directly, with no `statement`.  A `Notation` environment is usually a "
              "`convention` (or a `remark` titled Notation).",
              "- Example, Question, Problem: the example class, which may hold its paragraphs "
              "directly or a `statement`.  An open research question or conjecture posed as such: "
              "the openproblem class.",
              "- A named result (\"Theorem 2.1 (Main Theorem)\") keeps the name as its `title`; "
              "\"Proof of Theorem 3\", set apart from its theorem, is a `proof` whose `@ref` "
              "names the theorem.",
              "- Verify each element against `schema/pretext.rnc` in the PreTeXt clone before use."]
    open(output_path, "w", encoding="utf-8").write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
