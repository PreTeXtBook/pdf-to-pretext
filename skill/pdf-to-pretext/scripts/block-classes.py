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
             "Regenerate with `scripts/block-classes.py pretext/xsl/entities.ent "
             "references/block-classes.md` after a `git pull` of the clone.", "",
             "| class | elements |", "|---|---|"]
    for name, union in classes:
        lines.append("| {} | {} |".format(name.lower(),
                     ", ".join("`{}`".format(e) for e in union.split("|"))))
    lines += ["",
              "## Mapping a paper's environments",
              "",
              "- Theorem, Lemma, Corollary, Proposition, Claim, Fact, Algorithm: the theorem "
              "class, with `statement` and `proof` children.",
              "- Definition: `definition`.  Conjecture, Principle, Hypothesis, Assumption, Axiom: "
              "the axiom class (a statement never followed by a proof).",
              "- Remark, Note, Observation, Warning, Convention: the remark class.  A `Notation` "
              "environment is usually a `convention` (or a `remark` titled Notation).",
              "- Example, Question, Problem: the example class.  An open research question or "
              "conjecture posed as such: the openproblem class.",
              "- A named result (\"Theorem 2.1 (Main Theorem)\") keeps the name as its `title`; "
              "\"Proof of Theorem 3\" is a `proof` with that `title`.",
              "- Verify each element against `pretext/schema/pretext.rnc` before use."]
    open(output_path, "w", encoding="utf-8").write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
