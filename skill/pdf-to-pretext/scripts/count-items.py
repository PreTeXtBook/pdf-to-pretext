#!/usr/bin/env python3
"""Count what a transcription holds, and find references with no target.

Usage: count-items.py <project-directory>
       count-items.py <assembled.xml>
       count-items.py --references <assembled.xml>     only the references, one line

It reads the assembled source that validate.sh leaves in output/validation (every
included file knitted into one), so run validate.sh first.  Pass 3 asks that every item
of the manifest be present: compare these counts with the manifest's tables, not with
its own tallies.

It prints the number of each kind of element a manifest lists (the formulas written
inside image descriptions apart, since the page prints none of them), the numbered
equations in order, every cross-reference and citation whose target does not exist, and every
bibliography entry that is never cited.  PreTeXt's validation checks none of the last
three.
"""
import glob
import os
import sys
import xml.etree.ElementTree as ET

ID = "{http://www.w3.org/XML/1998/namespace}id"
KINDS = ["section", "subsection", "subsubsection", "paragraphs",
         "theorem", "lemma", "corollary", "proposition", "claim", "fact", "identity", "algorithm",
         "definition", "axiom", "conjecture", "principle", "hypothesis", "assumption",
         "remark", "convention", "note", "observation", "warning", "insight",
         "example", "question", "problem", "proof",
         "figure", "image", "sidebyside", "table", "tabular", "ol", "ul", "dl", "fn",
         "md", "mrow", "m", "xref", "biblio"]


def assembled(argument):
    if os.path.isdir(argument):
        found = glob.glob(os.path.join(argument, "output", "validation", "*-assembled.xml"))
        if not found:
            sys.exit("no assembled source in {}/output/validation: run validate.sh first".format(argument))
        return found[0]
    return argument


def main(arguments):
    only_references = arguments[0] == "--references"
    root = ET.parse(assembled(arguments[-1])).getroot()
    ids = {e.get(ID) for e in root.iter() if e.get(ID)}
    missing = []
    for e in root.iter():
        for attribute in ("ref", "first", "last"):
            if e.tag in ("xref", "proof") and e.get(attribute):
                missing += [(e.tag, target) for target in e.get(attribute).replace(",", " ").split() if target not in ids]
    if only_references:
        if missing:
            print("references with no target ({}): {}".format(
                len(missing), ", ".join(sorted({t for _, t in missing}))))
        else:
            print("references: every one has its target")
        return
    # a description of an image is written by the transcriber: its formulas are not the paper's
    described = {m for d in root.iter() if d.tag in ("description", "shortdescription") for m in d.iter("m")}
    print("counts, from the assembled source:")
    for kind in KINDS:
        n = sum(1 for e in root.iter(kind) if e not in described)
        if n:
            extra = ""
            if kind == "m" and described:
                extra = "   (and {} more inside image descriptions)".format(len(described))
            if kind == "proof":
                extra = "   ({} detached, with @ref)".format(sum(1 for p in root.iter("proof") if p.get("ref")))
            if kind == "md":
                extra = "   ({} numbered on the md itself)".format(sum(1 for p in root.iter("md") if p.get("number") == "yes"))
            if kind == "mrow":
                extra = "   ({} numbered)".format(sum(1 for p in root.iter("mrow") if p.get("number") == "yes"))
            print("  {:<14} {:>4}{}".format(kind, n, extra))
    numbered = [e for e in root.iter() if e.tag in ("md", "mrow") and e.get("number") == "yes"]
    print("numbered equations, in order ({}):".format(len(numbered)))
    for k, e in enumerate(numbered, 1):
        print("  {:>3}  {}".format(k, e.get(ID) or "(no identifier)"))
    cited = []
    for x in root.iter("xref"):
        cited += [t for t in (x.get("ref") or "").replace(",", " ").split()]
    entries = [b.get(ID) for b in root.iter("biblio")]
    keys = [t for t in cited if t in entries]
    print("citations: {} keys naming {} of {} bibliography entries".format(len(keys), len(set(keys)), len(entries)))
    never = [b for b in entries if b not in keys]
    if never:
        print("  never cited: " + ", ".join(str(b) for b in never))
    if missing:
        print("REFERENCES WITH NO TARGET ({}):".format(len(missing)))
        for tag, target in missing:
            print("  {} -> {}".format(tag, target))
    else:
        print("references: every one has its target")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1:])
