#!/usr/bin/env python3
"""Everything this skill asks of a PDF, done with PyMuPDF.

PyMuPDF is installed with PreTeXt's own requirements, so no other PDF program is needed.

Usage: pdftool.py info   <file.pdf>
           pages, page size, the left and right edges of the text block, producer, and
           how much text, how many fonts and pictures
       pdftool.py pages  <file.pdf>
           the number of pages, alone
       pdftool.py text   <file.pdf> [--layout]
           the text layer; with --layout, set out as on the page (for reading prose)
       pdftool.py lines  <file.pdf> <page>
           every line of the page with where it sits (points): top, bottom, left, right
       pdftool.py fonts  <file.pdf> <page>
           every line of the page, each run of text with the font that sets it
       pdftool.py render <file.pdf> <directory> [dpi]
           every page as page-NN.png (150 dpi unless given)
       pdftool.py zoom   <file.pdf> <page> <left> <top> <width> <height> <out.png> [dpi]
           one region of a page, rendered at 300 dpi unless given.  The box is in the
           pixels of the 150-dpi page image, where you will have read it off.
       pdftool.py images <file.pdf>
           every embedded picture: page, where it sits and how large (points), pixels
       pdftool.py crop   <file.pdf> <page> <x> <y> <width> <height> <stem>
           the region (points, from the page's top left) as <stem>.pdf and <stem>.svg,
           holding only what is inside it
       pdftool.py svg    <picture.pdf> <picture.svg>
           a one-page PDF picture as SVG
       pdftool.py lost   <file.pdf>
           how many glyphs of a PDF you built did not reach its text layer

Pages are numbered from 1, as the PDF numbers them, which need not be the printed number.

Two things the text layer does to symbols, which are not the same thing.  In a PDF built
here, a character the font did not have is set as the font's empty glyph and comes out as
U+FFFF (U+FFFD from some programs); `lost` counts those, and build.sh fails a PDF that
has any.  In an original, a symbol whose font names no character for it comes out as
whatever its position in the font suggests, often an ordinary letter or digit (the bar of
an arrow "maps to" as a 7): nothing marks it and `lost` says 0, which is one reason the
mathematics is read from the page image and never from the text.
"""
import os
import re
import statistics
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


# MuPDF has no character for the glyphs of the Dingbats font, which are named a73 and
# the like, and gives the number in the name as if it were a character code: the filled
# square that ends a proof in a PDF built by PreTeXt, glyph a73, comes out as the letter
# "I".  A Dingbats font holds no letters, so within one the reading is safe to undo.
# These are the glyphs in common use.
DINGBATS = {19: "\u2713", 20: "\u2714", 21: "\u2715", 22: "\u2716", 23: "\u2717", 24: "\u2718", 35: "\u2605",
            71: "\u25cf", 72: "\u274d", 73: "\u25a0", 74: "\u274f", 75: "\u2751", 76: "\u25b2", 77: "\u25bc",
            78: "\u25c6", 79: "\u2756"}


def is_dingbats(span):
    return "dingbats" in span["font"].lower()


def dingbats(text):
    return "".join(DINGBATS.get(ord(c), c) for c in text)


def span_text(span):
    return dingbats(span["text"]) if is_dingbats(span) else span["text"]


def document(path):
    return pymupdf.open(path)


def plain_text(path):
    """The text layer, page by page, in the order the PDF holds it; ligatures written out."""
    flags = pymupdf.TEXTFLAGS_TEXT & ~pymupdf.TEXT_PRESERVE_LIGATURES

    def page_text(page):
        blocks = page.get_text("dict", flags=flags)["blocks"]
        return "".join("".join(span_text(span) for span in line["spans"]) + "\n"
                       for block in blocks for line in block.get("lines", []))
    return join_accents("\f".join(page_text(page) for page in document(path)))


def layout_page(page):
    """One page's text set out as on the page: words in rows, placed by their left edge.

    Words set sideways (a stamp up the margin) are told by the direction of their line,
    taken out of the rows, and given at the end.  A row is the words whose middles are
    within a third of a line of the row's first word, so that a tall bracket or a large
    operator does not gather its neighbors' lines.  Ligatures are written out.
    """
    flags = pymupdf.TEXTFLAGS_WORDS & ~pymupdf.TEXT_PRESERVE_LIGATURES
    words = [w for w in page.get_text("words", flags=flags) if w[4].strip()]
    if not words:
        return ""
    set_lines = [line for block in page.get_text("dict")["blocks"] for line in block.get("lines", [])]
    turned = [pymupdf.Rect(line["bbox"]) for line in set_lines
              if abs(line["dir"][0] - 1) > 0.01 or abs(line["dir"][1]) > 0.01]
    ornaments = [pymupdf.Rect(span["bbox"]) for line in set_lines for span in line["spans"] if is_dingbats(span)]

    def within(w, rects):
        center = pymupdf.Point((w[0] + w[2]) / 2, (w[1] + w[3]) / 2)
        return any(rect.contains(center) for rect in rects)

    def is_turned(w):
        return within(w, turned)
    words = [w[:4] + (dingbats(w[4]),) + w[5:] if within(w, ornaments) else w for w in words]
    sideways = [w for w in words if is_turned(w)]
    words = [w for w in words if not is_turned(w)]
    note = ["[set sideways on the page: " + " ".join(w[4] for w in sideways) + "]"] if sideways else []
    if not words:
        return "\n".join(note)
    widths = [(w[2] - w[0]) / len(w[4]) for w in words if len(w[4]) > 2]
    unit = statistics.median(widths) if widths else 5.0
    line = statistics.median(w[3] - w[1] for w in words)
    rows = []  # each: [middle, top, bottom, words]
    for w in sorted(words, key=lambda w: ((w[1] + w[3]) / 2, w[0])):
        middle = (w[1] + w[3]) / 2
        if rows and abs(middle - rows[-1][0]) <= line / 3:
            rows[-1][3].append(w)
            rows[-1][2] = max(rows[-1][2], w[3])
        else:
            rows.append([middle, w[1], w[3], [w]])
    out, last_bottom = [], None
    for middle, top, bottom, members in rows:
        if last_bottom is not None and top - last_bottom > 0.8 * line:
            out.append("")
        text = ""
        for w in sorted(members, key=lambda w: w[0]):
            column = int(round(w[0] / unit))
            text += " " * max(column - len(text), 1 if text else 0) + w[4]
        out.append(text.rstrip())
        last_bottom = bottom
    return "\n".join(out + ([""] + note if note else []))


def layout_text(path):
    """The text layer set out as on the page, page after page."""
    return join_accents("\f".join(layout_page(page) + "\n" for page in document(path)))


def lost_glyphs(path):
    text = "".join(page.get_text() for page in document(path))
    return sum(text.count(mark) for mark in LOST)


def page_lines(doc, number):
    """Every line of text on a page: (top, bottom, left, right, text), in points, sorted."""
    flags = pymupdf.TEXTFLAGS_TEXT & ~pymupdf.TEXT_PRESERVE_LIGATURES
    out = []
    for block in doc[number - 1].get_text("dict", flags=flags)["blocks"]:
        for line in block.get("lines", []):
            x0, y0, x1, y1 = line["bbox"]
            out.append((y0, y1, x0, x1, "".join(span_text(span) for span in line["spans"])))
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
    other text into the document that includes it, and (the page's resources being
    cleaned on saving) none of the fonts that only the removed text used.
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
    one.save(stem + ".pdf", garbage=4, deflate=True, clean=True)
    cut = pymupdf.open(stem + ".pdf")
    open(stem + ".svg", "w", encoding="utf-8").write(cut[0].get_svg_image(text_as_path=True))


def fonts(path, number):
    lines = []
    for block in document(path)[number - 1].get_text("dict")["blocks"]:
        for line in block.get("lines", []):
            runs, last = [], None
            for span in line["spans"]:
                if not span["text"].strip():
                    if runs:
                        runs[-1][1] += " "  # a space set as a run of its own
                    continue
                name = "{} {:g}".format(span["font"], round(span["size"], 1))
                if name == last:
                    runs[-1][1] += span_text(span)
                else:
                    runs.append([name, span_text(span)])
                    last = name
            if runs:
                lines.append((round(line["bbox"][1]), round(line["bbox"][0]), runs))
    for _, _, runs in sorted(lines, key=lambda t: (t[0], t[1])):
        print("   ".join("[{}] {}".format(name, re.sub(r"\s+", " ", text).strip()) for name, text in runs))


def lines(path, number):
    print("   top  bottom    left   right   text")
    for top, bottom, left, right, text in page_lines(document(path), number):
        if text.strip():
            print("{:6.1f}  {:6.1f}  {:6.1f}  {:6.1f}   {}".format(top, bottom, left, right, join_accents(text).strip()))


def images(path):
    doc, count = document(path), 0
    for number, page in enumerate(doc, 1):
        for item in page.get_images(full=True):
            for rect in page.get_image_rects(item[0]):
                count += 1
                print("page {:>3}  at x={:6.1f} y={:6.1f}  {:6.1f} by {:6.1f} points  ({} by {} pixels)".format(
                    number, rect.x0, rect.y0, rect.width, rect.height, item[2], item[3]))
    print("{} embedded picture(s).  A figure that is not listed is a vector drawing.".format(count))


def text_block(doc):
    """The left and right edges of the text block, in points: where full lines begin and end."""
    lines = [l for number in range(1, doc.page_count + 1) for l in page_lines(doc, number)]
    if not lines:
        return None
    longest = max(l[3] - l[2] for l in lines)
    full = [l for l in lines if l[3] - l[2] > 0.9 * longest] or lines
    return statistics.median(l[2] for l in full), statistics.median(l[3] for l in full)


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
    block = text_block(doc)
    if block:
        print("text block: {:.0f} points wide, from x = {:.0f} to x = {:.0f}".format(block[1] - block[0], *block))
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
    elif command == "lines":
        lines(rest[0], int(rest[1]))
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
