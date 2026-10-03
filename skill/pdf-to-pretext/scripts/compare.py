#!/usr/bin/env python3
"""Compare an original PDF with a PDF built from the transcription, two ways.

1. Words: a similarity ratio and the longest runs of original text absent from the
   build.  Mathematics extracts as noise from both, so this measures prose, structure,
   and omissions -- not formulas.  A run that moved (a footnote, a floated caption)
   counts as absent; read the runs, do not trust the number alone.  A second ratio is
   for the text before the reference list (up to the last line that reads "References"
   or "Bibliography" in each PDF): PreTeXt sets a CSL entry in its own order, so the
   list drags the first ratio down by an amount that says nothing about the
   transcription, most of all in a short paper.
2. Symbols: counts of every non-ASCII character in the two text layers, after
   normalization, and the characters whose count is lower in the build.  Words cannot
   see a lost Greek letter; this can ("GREEK CAPITAL LETTER GAMMA  original 79  built 78").
   Characters found only in the build are listed briefly: those are usually extraction
   differences, not errors.

Usage: compare.py <original.pdf> <built.pdf>
"""
import collections
import difflib
import re
import subprocess
import sys
import unicodedata

LIGATURES = {"ﬁ": "fi", "ﬂ": "fl", "ﬀ": "ff", "ﬃ": "ffi", "ﬄ": "ffl"}
PUNCTUATION = {"’": "'", "‘": "'", "“": '"', "”": '"',
               "–": "-", "—": "-", "˜": "~", " ": " "}


HEADING = re.compile(r"^[ \t]*(?:\d+\.?[ \t]+)?(References|Bibliography)[ \t]*$", re.M | re.I)


def before_references(t):
    """The text up to the last heading of a reference list, or None when there is none."""
    hits = list(HEADING.finditer(t))
    return t[:hits[-1].start()] if hits else None


def text(pdf_path):
    return subprocess.run(["pdftotext", pdf_path, "-"], capture_output=True,
                          text=True, check=True).stdout


def words(t):
    for k, v in LIGATURES.items():
        t = t.replace(k, v)
    t = re.sub(r"-\n(?=[a-z])", "", t)
    t = t.replace("\f", " ")
    return re.findall(r"[A-Za-z][A-Za-z'-]*", t)


def symbols(t):
    for k, v in LIGATURES.items():
        t = t.replace(k, v)
    for k, v in PUNCTUATION.items():
        t = t.replace(k, v)
    t = t.replace("ı́", "í")  # dotless i with acute has no precomposed form
    t = unicodedata.normalize("NFC", t)
    return collections.Counter(c for c in t if ord(c) > 127 and not c.isspace())


def main(original_path, built_path):
    original_text, built_text = text(original_path), text(built_path)
    original, built = words(original_text), words(built_text)
    matcher = difflib.SequenceMatcher(None, original, built, autojunk=False)
    print("original words: {}   built words: {}".format(len(original), len(built)))
    print("similarity: {:.3f}".format(matcher.ratio()))
    original_body, built_body = before_references(original_text), before_references(built_text)
    if original_body is None or built_body is None:
        print("similarity before the reference list: no such heading found in {}".format(
            " or ".join(name for name, body in (("the original", original_body), ("the build", built_body))
                        if body is None)))
    else:
        a_words, b_words = words(original_body), words(built_body)
        print("similarity before the reference list: {:.3f}   (original words: {}   built words: {})".format(
            difflib.SequenceMatcher(None, a_words, b_words, autojunk=False).ratio(), len(a_words), len(b_words)))
    missing = []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag in ("delete", "replace") and i2 - i1 >= 8:  # shorter runs are mostly mathematics
            missing.append((i2 - i1, " ".join(original[i1:i2])))
    missing.sort(reverse=True)
    print("longest runs of original words absent from the build:")
    for length, run in missing[:10]:
        print("  [{} words] {}".format(length, run[:160]))
    if not missing and matcher.ratio() < 1:
        # nothing long is absent, yet the texts differ: show where, however short
        short = sorted(((i2 - i1, " ".join(original[i1:i2]), " ".join(built[j1:j2]))
                        for tag, i1, i2, j1, j2 in matcher.get_opcodes() if tag != "equal"), reverse=True)
        print("  none of eight words or more; the longest differences:")
        for length, was, now in short[:10]:
            print("  original: {!r}   build: {!r}".format(was[:80], now[:80]))
    a, b = symbols(original_text), symbols(built_text)
    lost = sorted(((c, a[c], b[c]) for c in a if b[c] < a[c]), key=lambda r: r[2] - r[1])
    print("symbols with a lower count in the build ({}):".format(len(lost)))
    for c, x, y in lost:
        print("  {} {:<38} original {:>4}  built {:>4}".format(
            c, unicodedata.name(c, "?")[:38], x, y))
    extra = sorted(c for c in b if a[c] == 0)
    if extra:
        print("symbols only in the build (extraction differences, usually): " + " ".join(extra))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
