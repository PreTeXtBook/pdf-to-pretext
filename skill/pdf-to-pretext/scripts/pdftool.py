#!/usr/bin/env python3
"""Everything this skill asks of a PDF, done with PyMuPDF.

PyMuPDF is installed with PreTeXt's own requirements, so no other PDF program is needed.

Usage: pdftool.py info   <file.pdf>
           pages, page size, producer, and how much text, how many fonts and pictures
       pdftool.py text   <file.pdf> [--layout]
           the text layer; with --layout, set out as on the page (for reading prose)
       pdftool.py render <file.pdf> <directory> [dpi]
           every page as page-NN.png (150 dpi unless given)
       pdftool.py zoom   <file.pdf> <page> <left> <top> <width> <height> <out.png> [dpi]
           one region of a page, rendered at 300 dpi unless given.  The box is in the
           pixels of the 150-dpi page image, where you will have read it off.
       pdftool.py fonts  <file.pdf> <page>
           every line of the page, each run of text with the font that sets it
       pdftool.py images <file.pdf>
           every embedded picture: page, where it sits and how large (points), pixels
       pdftool.py crop   <file.pdf> <page> <x> <y> <width> <height> <stem>
           the region (points, from the page's top left) as <stem>.pdf and <stem>.svg,
           holding only what is inside it

Pages are numbered from 1, as the PDF numbers them, which need not be the printed number.

A glyph that did not reach the text layer shows in `text` as U+FFFF or U+FFFD; `lost`
counts them (pdftool.py lost <file.pdf>), and build.sh fails a PDF that has any.
"""
import io
import os
import re
import sys
import unicodedata

import venv_python
venv_python.ensure("pymupdf|fitz")
try:
    import pymupdf
except ImportError:  # PyMuPDF before 1.24.3
    import fitz as pymupdf

LOST = ("￿", "�")


# TeX's older fonts set an accent as a glyph of its own, before its letter (after it, for
# a cedilla), and that is how the text layer holds it: "Koml" + acute + "os".
ACCENTS = {"\u00b4": "\u0301", "\u00a8": "\u0308", "\u02c6": "\u0302", "\u02dc": "\u0303",
           "\u02c7": "\u030c", "\u02d8": "\u0306", "\u02da": "\u030a", "\u02dd": "\u030b",
           "\u00af": "\u0304", "\u02d9": "\u0307"}
PLAIN = {"\u0131": "i", "\u0237": "j"}


def join_accents(text):
    """Put each separately set accent on its letter."""
    def before(m):
        return unicodedata.normalize("NFC", PLAIN.get(m.group(2), m.group(2)) + ACCENTS[m.group(1)])
    text = re.sub("([{}])([A-Za-z\u0131\u0237])".format("".join(ACCENTS)), before, text)
    text = re.sub("(?<=[A-Za-z])`([aeiouAEIOU])", lambda m: unicodedata.normalize("NFC", m.group(1) + "\u0300"), text)
    return re.sub("([A-Za-z])\u00b8", lambda m: unicodedata.normalize("NFC", m.group(1) + "\u0327"), text)


def document(path):
    return pymupdf.open(path)


def plain_text(path):
    """The text layer, page by page, in the order the PDF holds it."""
    return join_accents("\f".join(page.get_text() for page in document(path)))


def layout_text(path):
    """The text layer set out as on the page: columns stay columns, lines stay lines."""
    try:
        from pymupdf.__main__ import page_layout
    except ImportError:
        return join_accents("\f".join(page.get_text(sort=True) for page in document(path)))
    out = io.BytesIO()
    flags = pymupdf.TEXT_PRESERVE_WHITESPACE | pymupdf.TEXT_MEDIABOX_CLIP
    for page in document(path):
        page_layout(page, out, 2, 3, False, True, flags)
    return join_accents(out.getvalue().decode("utf-8", errors="replace"))


def lost_glyphs(path):
    text = plain_text(path)
    return sum(text.count(mark) for mark in LOST)


def page_lines(doc, number):
    """Every line of text on a page: (top, bottom, left, right, text), in points, sorted."""
    flags = pymupdf.TEXT_PRESERVE_WHITESPACE | pymupdf.TEXT_MEDIABOX_CLIP
    out = []
    for block in doc[number - 1].get_text("dict", flags=flags)["blocks"]:
        for line in block.get("lines", []):
            x0, y0, x1, y1 = line["bbox"]
            out.append((y0, y1, x0, x1, "".join(span["text"] for span in line["spans"])))
    return sorted(out)


def page_pixels(doc, number, dpi, clip=None):
    """A page (or a region of it, in points) rendered: a pixmap, RGB, no transparency."""
    return doc[number - 1].get_pixmap(dpi=dpi, colorspace=pymupdf.csRGB, alpha=False,
                                      clip=pymupdf.Rect(*clip) if clip else None)


def render(path, directory, dpi=150):
    doc = document(path)
    os.makedirs(directory, exist_ok=True)
    width = max(2, len(str(doc.page_count)))
    for number in range(1, doc.page_count + 1):
        page_pixels(doc, number, dpi).save(os.path.join(directory, "page-{:0{}d}.png".format(number, width)))
    return doc.page_count


def zoom(path, number, left, top, width, height, out, dpi=300, read_at=150):
    k = 72.0 / read_at
    clip = (left * k, top * k, (left + width) * k, (top + height) * k)
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    page_pixels(document(path), number, dpi, clip).save(out)


def crop(doc, number, x, y, width, height, stem):
    """Write <stem>.pdf and <stem>.svg holding the region and nothing outside it.

    The page is copied alone into a new document; the text, pictures, and line art that
    lie wholly outside the region are removed (as redactions, which delete rather than
    cover); and the page is cut to the region.  So a crop carries none of the page's
    other text into the document that includes it.
    """
    one = pymupdf.open()
    one.insert_pdf(doc, from_page=number - 1, to_page=number - 1)
    page = one[0]
    box = page.rect
    region = pymupdf.Rect(x, y, x + width, y + height) & box
    outside = [pymupdf.Rect(box.x0, box.y0, box.x1, region.y0), pymupdf.Rect(box.x0, region.y1, box.x1, box.y1),
               pymupdf.Rect(box.x0, region.y0, region.x0, region.y1), pymupdf.Rect(region.x1, region.y0, box.x1, region.y1)]
    for rect in outside:
        if not rect.is_empty:
            page.add_redact_annot(rect)
    # of a picture that reaches outside the region, the pixels outside are blanked
    try:
        page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_PIXELS, graphics=pymupdf.PDF_REDACT_LINE_ART_REMOVE_IF_COVERED)
    except (AttributeError, TypeError):  # an older PyMuPDF, without the choice for line art
        page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_PIXELS)
    page.set_cropbox(region)
    one.save(stem + ".pdf", garbage=4, deflate=True)
    cut = pymupdf.open(stem + ".pdf")
    open(stem + ".svg", "w", encoding="utf-8").write(cut[0].get_svg_image(text_as_path=True))


def fonts(path, number):
    lines = []
    for block in document(path)[number - 1].get_text("dict")["blocks"]:
        for line in block.get("lines", []):
            runs, last = [], None
            for span in line["spans"]:
                if not span["text"].strip():
                    continue
                name = "{} {:g}".format(span["font"], round(span["size"], 1))
                if name == last:
                    runs[-1][1] += span["text"]
                else:
                    runs.append([name, span["text"]])
                    last = name
            if runs:
                lines.append((round(line["bbox"][1]), round(line["bbox"][0]), runs))
    for _, _, runs in sorted(lines, key=lambda t: (t[0], t[1])):
        print("   ".join("[{}] {}".format(name, text.strip()) for name, text in runs))


def images(path):
    doc, count = document(path), 0
    for number, page in enumerate(doc, 1):
        for item in page.get_images(full=True):
            for rect in page.get_image_rects(item[0]):
                count += 1
                print("page {:>3}  at x={:6.1f} y={:6.1f}  {:6.1f} by {:6.1f} points  ({} by {} pixels)".format(
                    number, rect.x0, rect.y0, rect.width, rect.height, item[2], item[3]))
    print("{} embedded picture(s).  A figure that is not listed is a vector drawing.".format(count))


def info(path):
    doc = document(path)
    meta = doc.metadata or {}
    for key in ("title", "author", "creator", "producer"):
        if meta.get(key):
            print("{:<9} {}".format(key + ":", meta[key]))
    rect = doc[0].rect
    words = sum(len(page.get_text("words")) for page in doc)
    print("pages:    {}".format(doc.page_count))
    print("size:     {:g} by {:g} points".format(rect.width, rect.height))
    print("text:     {} words".format(words))
    print("fonts:    {}".format(len({f[3] for page in doc for f in page.get_fonts()})))
    print("pictures: {} embedded (vector drawings are not counted)".format(sum(len(page.get_images()) for page in doc)))
    return doc.page_count, words


def main(arguments):
    if not arguments:
        sys.exit(__doc__)
    command, rest = arguments[0], arguments[1:]
    if command == "info":
        info(rest[0])
    elif command == "pages":
        print(document(rest[0]).page_count)
    elif command == "text":
        sys.stdout.write(layout_text(rest[0]) if "--layout" in rest[1:] else plain_text(rest[0]))
    elif command == "lost":
        print(lost_glyphs(rest[0]))
    elif command == "render":
        print("pages rendered:", render(rest[0], rest[1], int(rest[2]) if len(rest) > 2 else 150))
    elif command == "zoom":
        zoom(rest[0], int(rest[1]), *[float(v) for v in rest[2:6]], rest[6], int(rest[7]) if len(rest) > 7 else 300)
    elif command == "fonts":
        fonts(rest[0], int(rest[1]))
    elif command == "images":
        images(rest[0])
    elif command == "crop":
        crop(document(rest[0]), int(rest[1]), *[float(v) for v in rest[2:6]], rest[6])
    elif command == "svg":  # a one-page PDF picture as SVG
        open(rest[1], "w", encoding="utf-8").write(document(rest[0])[0].get_svg_image(text_as_path=True))
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
