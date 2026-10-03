#!/usr/bin/env python3
"""List what an HTML build shows, as text, for checking it without a browser.

Usage: html-outline.py <the HTML build's directory>        e.g. <project>/output/web

The mathematics of an HTML build is typeset in the reader's browser, so the pages cannot
be read as rendered from here, and this skill does not ask for a browser.  What can be
checked is what the files say: for every page, its headings with their numbers, its
captions, the tags of its numbered equations, the text of its cross-references (the
number each one will show), and its images, with a mark on any image whose file is
missing.  Compare these with the built PDF, which was read page by page: the same
blocks, the same numbers, the same captions, every picture present.
"""
import glob
import html
import os
import re
import sys


def text(fragment):
    plain = html.unescape(re.sub(r"<[^>]+>", "", fragment))
    return re.sub(r"\s+", " ", plain.replace("\U0001F517", "")).strip()


def main(directory):
    pages = sorted(glob.glob(os.path.join(directory, "*.html")))
    if not pages:
        sys.exit("no HTML files in " + directory)
    missing = 0
    for page in pages:
        source = open(page, encoding="utf-8").read()
        body = source[source.find("<main"):] if "<main" in source else source
        items = []
        for m in re.finditer(r'<h[1-6][^>]*class="heading[^"]*"[^>]*>(.*?)</h[1-6]>|<figcaption[^>]*>(.*?)</figcaption>'
                             r'|\\tag\{([^}]*)\}|<img[^>]*src="([^"]*)"[^>]*>|<a [^>]*class="[^"]*xref[^"]*"[^>]*>(.*?)</a>',
                             body, re.S):
            heading, caption, tag, image, reference = m.groups()
            if heading is not None:
                items.append("heading    " + text(heading))
            elif caption is not None:
                items.append("caption    " + text(caption))
            elif tag is not None:
                items.append("equation   (" + tag + ")")
            elif image is not None:
                if image.startswith("data:"):
                    continue  # the logos in a page's footer
                there = os.path.exists(os.path.join(directory, image))
                missing += not there
                items.append("image      " + image + ("" if there else "   FILE MISSING"))
            else:
                items.append("reference  " + text(reference))
        items = [i for i in items if i not in ("heading    Read aloud settings", "heading    Readability settings")]
        if items:
            print(os.path.basename(page))
            for item in items:
                print("    " + item)
    print("pages: {}   images whose file is missing: {}".format(len(pages), missing))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
