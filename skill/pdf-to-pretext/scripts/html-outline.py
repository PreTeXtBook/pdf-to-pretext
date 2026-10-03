#!/usr/bin/env python3
"""List what an HTML build shows, as text, for checking it without a browser.

Usage: html-outline.py <the HTML build's directory>        e.g. <project>/output/web

The mathematics of an HTML build is typeset in the reader's browser, so the pages cannot
be read as rendered from here, and this skill does not ask for a browser.  What can be
checked is what the files say.  For every page, in reading order (the order of the
table of contents): its headings with their numbers; on the title page the authors, what
is printed under each, the date, and the first words of the abstract; its captions; the
tags of its numbered equations; the text of its cross-references and citations (the
number each one will show); its footnotes; and its images, with a mark on any image
whose file is missing.  Compare these with the built PDF, which was read page by page:
the same blocks, the same numbers, the same captions, every picture present.

A page that only sends the reader on to another (index.html) is counted and not listed.
"""
import glob
import html
import os
import re
import sys

PATTERN = re.compile(
    r'<h[1-6][^>]*class="heading[^"]*"[^>]*>(?P<heading>.*?)</h[1-6]>'
    r'|<figcaption[^>]*>(?P<caption>.*?)</figcaption>'
    r'|\\tag\{(?P<tag>[^}]*)\}'
    r'|<img[^>]*src="(?P<image>[^"]*)"[^>]*>'
    r'|<a [^>]*class="[^"]*\b(?:xref|internal)\b[^"]*"[^>]*>(?P<reference>.*?)</a>'
    r'|<div class="author-name">(?P<author>.*?)</div>'
    r'|<div class="author-info">(?P<under>.*?)</div>'
    r'|<div class="date">(?P<date>.*?)</div>'
    r'|<div class="abstract"[^>]*>(?P<abstract>.*?</div>)'
    r'|<details class="ptx-footnote"[^>]*>\s*<summary[^>]*>(?P<mark>.*?)</summary>(?P<footnote>.*?)</details>',
    re.S)
FURNITURE = ("Read aloud settings", "Readability settings")


def text(fragment):
    plain = html.unescape(re.sub(r"<[^>]+>", " ", fragment))
    return re.sub(r"\s+", " ", plain.replace("\U0001F517", "")).strip()


def beginning(fragment, count=12):
    words = text(fragment).split()
    return " ".join(words[:count]) + (" ..." if len(words) > count else "")


def reading_order(directory, pages):
    """The pages as the table of contents orders them; any it does not name come first."""
    for page in pages:
        source = open(page, encoding="utf-8").read()
        if 'id="ptx-toc"' in source and "<main" in source:
            contents = source[source.find('id="ptx-toc"'):source.find("<main")]
            named = []
            for target in re.findall(r'<a href="([^"#]+)[^"]*" class="internal"', contents):
                path = os.path.join(directory, target)
                if path not in named and path in pages:
                    named.append(path)
            return [p for p in pages if p not in named] + named
    return pages


def main(directory):
    pages = sorted(glob.glob(os.path.join(directory, "*.html")))
    if not pages:
        sys.exit("no HTML files in " + directory)
    missing, redirects = 0, 0
    for page in reading_order(directory, pages):
        source = open(page, encoding="utf-8").read()
        if "<main" not in source:
            redirects += 1
            continue
        body = source[source.find("<main"):]
        items = []
        for m in PATTERN.finditer(body):
            found = m.groupdict()
            if found["heading"] is not None:
                if text(found["heading"]) not in FURNITURE:
                    items.append("heading    " + text(found["heading"]))
            elif found["caption"] is not None:
                items.append("caption    " + text(found["caption"]))
            elif found["tag"] is not None:
                items.append("equation   (" + found["tag"] + ")")
            elif found["image"] is not None:
                image = found["image"]
                if image.startswith("data:"):
                    continue  # the logos in a page's footer
                there = os.path.exists(os.path.join(directory, image))
                missing += not there
                items.append("image      " + image + ("" if there else "   FILE MISSING"))
            elif found["reference"] is not None:
                # a line of a table of contents holds a title; a reference in the text does not
                label = "contents   " if 'class="title"' in found["reference"] else "reference  "
                items.append(label + text(found["reference"]))
            elif found["author"] is not None:
                items.append("author     " + text(found["author"]))
            elif found["under"] is not None:
                lines = [text(part) for part in re.split(r"<br\s*/?>", found["under"])]
                items += ["           " + line for line in lines if line]
            elif found["date"] is not None:
                items.append("date       " + text(found["date"]))
            elif found["abstract"] is not None:
                items.append("abstract   " + beginning(re.sub(r'^\s*<span class="title">.*?</span>', "", found["abstract"], flags=re.S)))
            elif found["footnote"] is not None:
                items.append("footnote   " + text(found["mark"]) + ": " + beginning(found["footnote"]))
        print(os.path.basename(page))
        for item in items or ["(nothing of these kinds)"]:
            print("    " + item)
    print("pages listed: {}{}   images whose file is missing: {}".format(
        len(pages) - redirects,
        "   (and {} that only send the reader on)".format(redirects) if redirects else "", missing))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
