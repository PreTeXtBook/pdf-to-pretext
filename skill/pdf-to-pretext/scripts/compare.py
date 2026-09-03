#!/usr/bin/env python3
"""Compare the words of an original PDF with the words of a PDF built from the
transcription: a similarity ratio and the longest runs of original text that
are missing from the build.

Usage: compare.py <original.pdf> <built.pdf>

Both PDFs go through pdftotext; hyphenation at line ends, ligatures, and
whitespace are normalized before comparison.  Mathematics extracts as noise
from both, so this measures prose, structure, and omissions — not formulas.
"""
import difflib
import re
import subprocess
import sys


def words(pdf_path):
    text = subprocess.run(["pdftotext", pdf_path, "-"], capture_output=True,
                          text=True, check=True).stdout
    text = text.replace("ﬁ", "fi").replace("ﬂ", "fl")
    text = re.sub(r"-\n(?=[a-z])", "", text)
    text = text.replace("\f", " ")
    return re.findall(r"[A-Za-z][A-Za-z'-]*", text)


def main(original_path, built_path):
    original = words(original_path)
    built = words(built_path)
    matcher = difflib.SequenceMatcher(None, original, built, autojunk=False)
    print("original words: {}   built words: {}".format(len(original), len(built)))
    print("similarity: {:.3f}".format(matcher.ratio()))
    missing = []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag in ("delete", "replace") and i2 - i1 >= 8:
            missing.append((i2 - i1, " ".join(original[i1:i2])))
    missing.sort(reverse=True)
    print("longest runs of original words absent from the build:")
    for length, run in missing[:10]:
        print("  [{} words] {}".format(length, run[:160]))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
