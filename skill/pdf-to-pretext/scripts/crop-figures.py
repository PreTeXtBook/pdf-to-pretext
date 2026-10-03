#!/usr/bin/env python3
"""Crop every figure panel of a paper out of its PDF pages, for `image/@source`.

Meant for papers whose figures are pictures on the page with labels typeset over them
(raster PNGs under LaTeX overlays, or vector drawings): a page-region crop keeps picture
and labels together, where pulling the embedded picture out would drop the labels.

Usage:
    crop-figures.py <paper.pdf> <spec.json> <external-dir> [--work DIR] [--dpi N] [--pad PT]

<spec.json> is a list of figures, in page order:
    {"figure": "5.4", "page": 10, "panels": ["figure-generalized-rectangle",
     "figure-degenerate-rectangle"], "split": ["cols", 2]}
with "split" one of: null (one panel), ["cols", n] (n panels across, at the widest white
gaps), or ["grid", [n1, n2, ...]] (rows of n1, n2, ... panels, rows split first).
Panel names become <external-dir>/<name>.svg and .pdf (so `image/@source` needs no
extension: HTML takes the SVG, LaTeX the PDF).

How a figure is found on its page: the text layer gives every line's box in points
(pdftool.py, with PyMuPDF).  The caption is the line beginning "Figure N.M";
subcaptions are the "(a) ...", "(b) ..." lines within 60 points above it, with their
continuation lines; the figure region runs from the last body-text line above (any line
wider than a label, or a line at the left margin with a letter in it) down to the
caption.  Inside that region the ink of a render at --dpi gives the tight box, with
caption and subcaption text blanked first.  Composite figures split at the widest white
gaps.  Boxes are padded by --pad points and written to <work>/figure-boxes.json (x, y, w,
h in points: w is the width to set against the text block's when choosing `image/@width`);
each panel is also rendered to PNG in <work>/panels/, and contact sheets
<work>/sheet-N.png show them all together, each over its name.  Reading the contact
sheets is the check to make before authoring.

Needs: Python with PyMuPDF, Pillow, and numpy (setup.sh installs all three).

The layout options.  The defaults suit letter paper with a text block from about 72 to
540 points, and any narrower block centered on such a page.  `pdftool.py info` prints the
block's edges.  Give the options when the block is wider than that, or the paper is not
letter or A4, or a contact sheet shows a panel cut short at a side or holding body text:
--left and --right are the block's edges (a little outside the text), and --margin is a
little right of where body lines begin, since a line that starts left of --margin is
taken for body text, not for a label in the picture.

Two limits, each kept because loosening it moved boxes that were right (the 58 panels
of arXiv 2607.05283 are the regression test: change a rule only if they all stay put).
A caption is "Figure N:" or "Figure N" alone on its line, N being the number in the
specification, and only when neither exists a line that goes on after a space; "Figure
N." is not taken, since a paragraph can end with those words on a line of their own.
Subcaptions are recognized for (a), (b), (c) only; a wider range took the items of a
lettered list near a caption for subcaptions.  Check a figure with more lettered panels
on the contact sheet with particular care.
"""
import argparse, json, math, os, re, sys
import venv_python; venv_python.ensure("numpy", "PIL", "pymupdf|fitz")
import numpy as np
from PIL import Image, ImageDraw
import pdftool

ap = argparse.ArgumentParser()
ap.add_argument("pdf"); ap.add_argument("spec"); ap.add_argument("external")
ap.add_argument("--work", help="working directory (default: crop-work beside the spec)")
ap.add_argument("--dpi", type=int, default=300); ap.add_argument("--pad", type=float, default=3.0)
ap.add_argument("--left", type=float, default=60.0, help="left edge of the text block, points")
ap.add_argument("--right", type=float, default=552.0, help="right edge of the text block, points")
ap.add_argument("--margin", type=float, default=110.0, help="a line starting left of this is at the margin")
args = ap.parse_args()
WORK = args.work or os.path.join(os.path.dirname(os.path.abspath(args.spec)), "crop-work")
os.makedirs(WORK, exist_ok=True)
os.makedirs(os.path.join(WORK, "panels"), exist_ok=True); os.makedirs(args.external, exist_ok=True)
K = args.dpi / 72.0
spec = json.load(open(args.spec))
DOC = pdftool.document(args.pdf)

# 1. text positions: every line of a page as (top, bottom, left, right, text), in points
def lines(page):
    return pdftool.page_lines(DOC, page)

# 2. ink: where a render of the page at --dpi is not white
_pages = {}
def ink(page):
    if page not in _pages:
        pix = pdftool.page_pixels(DOC, page, args.dpi)
        rgb = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)[:, :, :3]
        _pages[page] = rgb.min(axis=2) < 235
    return _pages[page]

def ink_box(mask, y0, y1, x0, x1):
    sub = mask[int(y0):int(y1), int(x0):int(x1)]
    rows = np.where(sub.any(axis=1))[0]; cols = np.where(sub.any(axis=0))[0]
    if len(rows) == 0: return None
    return (int(x0) + cols[0], int(y0) + rows[0], int(x0) + cols[-1] + 1, int(y0) + rows[-1] + 1)

def gaps(profile, min_gap):
    out, start = [], None
    for i, v in enumerate(profile):
        if not v and start is None: start = i
        if v and start is not None:
            if i - start >= min_gap: out.append((start, i))
            start = None
    return out

def split(mask, box, n, axis):
    x0, y0, x1, y1 = box
    prof = mask[y0:y1, x0:x1].any(axis=axis)
    lo, hi = (x0, x1) if axis == 0 else (y0, y1)
    g = [(a + lo, b + lo) for a, b in gaps(prof, 8) if a + lo > lo and b + lo < hi]
    g = sorted(g, key=lambda t: t[1] - t[0], reverse=True)[:n - 1]
    cuts = sorted((a + b) // 2 for a, b in g)
    edges = [lo] + cuts + [hi]
    if len(edges) != n + 1:
        sys.exit(f"could not find {n - 1} white gaps to split a figure ({'columns' if axis == 0 else 'rows'}); found {len(cuts)}")
    if axis == 0: return [ink_box(mask, y0, y1, edges[i], edges[i + 1]) for i in range(n)]
    return [ink_box(mask, edges[i], edges[i + 1], x0, x1) for i in range(n)]

# 3. boxes
result, floors = [], {}
for fig in spec:
    num, page, names, sp = fig["figure"], fig["page"], fig["panels"], fig.get("split")
    L = lines(page)
    # the caption line: "Figure N.M:" or a bare "Figure N.M"; only if neither exists, a line
    # that continues after a space (a body sentence can start "Figure N.M gives ...")
    cap = [l for l in L if re.match(r"Figure %s(:|$)" % re.escape(num), l[4].strip())] or \
          [l for l in L if re.match(r"Figure %s\s" % re.escape(num), l[4].strip())]
    if not cap: sys.exit(f"no caption line 'Figure {num}' on page {page}")
    cap_top = cap[0][0]
    floor = floors.get(page, 0.0)
    subcaps = [l for l in L if floor < l[0] < cap_top and cap_top - l[0] < 60 and re.match(r"\([abc]\)(\s|$)", l[4].strip())]
    if subcaps:
        first = min(l[0] for l in subcaps)
        subcaps = [l for l in L if first <= l[0] < cap_top]
    bottom = cap_top - 1.5
    def is_body(l):
        w = l[3] - l[2]
        return w > 60 or (l[2] < args.margin and w > 40) or (l[2] < args.margin - 10 and re.search(r"[A-Za-z]", l[4]))
    body = [l for l in L if floor < l[0] and l[1] < bottom - 2 and is_body(l) and l not in subcaps]
    top = (max(l[1] for l in body) + 1.5) if body else max(40.0, floor)
    floors[page] = cap[0][1]
    mask = ink(page).copy()
    for l in [c for c in L if re.match(r"Figure \d+\.\d+", c[4].strip())]:
        mask[int((l[0] - 3) * K):int((l[1] + 4) * K), int((l[2] - 3) * K):int((l[3] + 3) * K)] = False
    for l in subcaps:
        mask[int((l[0] - 2) * K):int((l[1] + 2) * K), int((l[2] - 2) * K):int((l[3] + 2) * K)] = False
    box = ink_box(mask, top * K, bottom * K, args.left * K, args.right * K)
    if not box: sys.exit(f"no ink found for Figure {num} between {top:.0f} and {bottom:.0f} points on page {page}")
    if not sp: boxes = [box]
    elif sp[0] == "cols": boxes = split(mask, box, sp[1], 0)
    else:
        boxes = []
        for r, n in zip(split(mask, box, len(sp[1]), 1), sp[1]):
            boxes += split(mask, r, n, 0) if n > 1 else [r]
    if len(boxes) != len(names) or not all(boxes): sys.exit(f"Figure {num}: {len(boxes)} boxes for {len(names)} panel names")
    for name, b in zip(names, boxes):
        x0, y0, x1, y1 = b
        result.append({"figure": num, "name": name, "page": page, "x": round(x0 / K - args.pad, 1), "y": round(y0 / K - args.pad, 1),
                       "w": round((x1 - x0) / K + 2 * args.pad, 1), "h": round((y1 - y0) / K + 2 * args.pad, 1)})
        print(f"{num:5} {name:45} p{page:2d}  x={x0/K:6.1f} y={y0/K:6.1f} w={(x1-x0)/K:6.1f} h={(y1-y0)/K:6.1f}")
json.dump(result, open(os.path.join(WORK, "figure-boxes.json"), "w"), indent=1)

# 4. crops and previews
for b in result:
    x, y = math.floor(b["x"]), math.floor(b["y"])
    w, h = math.ceil(b["x"] + b["w"]) - x, math.ceil(b["y"] + b["h"]) - y
    stem = os.path.join(args.external, b["name"])
    pdftool.crop(DOC, b["page"], x, y, w, h, stem)
    pdftool.page_pixels(pdftool.document(stem + ".pdf"), 1, 110).save(os.path.join(WORK, "panels", b["name"] + ".png"))

# 5. contact sheets: every panel over its name; a panel narrower than its name gets the name's width
sheet_w, x, y, row_h, sheets = 1400, 10, 10, 0, []
canvas = Image.new("RGB", (sheet_w, 1800), "white"); d = ImageDraw.Draw(canvas)
for b in result:
    im = Image.open(os.path.join(WORK, "panels", b["name"] + ".png"))
    if im.width > 650: im = im.resize((650, int(im.height * 650 / im.width)))
    cell = max(im.width, int(d.textlength(b["name"])) + 2)
    if x + cell + 10 > sheet_w: x, y, row_h = 10, y + row_h + 26, 0
    if y + im.height + 26 > canvas.height:
        sheets.append(canvas); canvas = Image.new("RGB", (sheet_w, 1800), "white"); d = ImageDraw.Draw(canvas); x = y = 10; row_h = 0
    canvas.paste(im, (x, y)); d.rectangle([x - 1, y - 1, x + im.width, y + im.height], outline="gray")
    d.text((x, y + im.height + 2), b["name"], fill="black"); x += cell + 14; row_h = max(row_h, im.height)
sheets.append(canvas)
for i, s in enumerate(sheets, 1): s.save(os.path.join(WORK, f"sheet-{i}.png"))
print(f"{len(result)} panels cropped into {args.external}")
print(f"boxes: {os.path.join(WORK, 'figure-boxes.json')}   contact sheets to read: " + " ".join(os.path.join(WORK, f"sheet-{i}.png") for i in range(1, len(sheets) + 1)))
