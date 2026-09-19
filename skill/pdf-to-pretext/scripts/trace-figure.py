#!/usr/bin/env python3
"""Vectorize one panel of a hand-drawn mathematical figure from a 600-dpi render, as the
raw material for a PreFigure recreation.

Usage as a module:  trace_panel(png, labels) -> dict;  overlay(png, dict, out.png)
Usage as a script:  trace-figure.py <crop.png> <labels.json> <out.json> <overlay.png>
    where labels.json is a list of the text lines laid over the picture, each with
    x0, x1, y0, y1 in PDF points from the crop's lower-left corner (they are blanked
    before tracing; the crop-figures.py work directory's stext files give them).

What it finds, all in PDF points from the crop's lower-left corner:
- curves, by color class (black, gray, red, orange, gold, green, blue, magenta, and
  the pale "-light" tints used for highlight bands): the thinned centerline of each
  stroke, walked along breadth-first spines, joined straight through junctions by
  direction continuity, bridged across the small gaps another color leaves, resampled
  and simplified; each with its stroke width and mean color; closed loops marked;
- dashed and dotted curves: short pieces of one color chained by nearest neighbor when
  evenly spaced, with the dash and gap lengths;
- arrowheads, filled (a place where the stroke's half-width jumps) and open (two short
  barbs meeting at a junction), each with its tip and base points;
- dots: round filled blobs of any color, found by erosion so touching lines do not hide
  them, with their radius;
- filled regions (gray): convex hulls;
- highlight bands: pale tints closed over the strand they cover.
The overlay PNG draws every result on the crop, and is the check to make.  The figures of
arXiv 2607.05283 (2026-09-18) were the test set; expect to tune the color ranges in
PALETTE and the thresholds for another paper's drawing style.  Needs numpy, scipy, Pillow.
"""
import json, math, numpy as np
from collections import deque
from PIL import Image
from scipy import ndimage
K = 72 / 600
PALETTE = {  # hue ranges in degrees, saturated strokes
    "red": (-18, 14), "orange": (14, 38), "gold": (38, 62), "green": (80, 165), "blue": (200, 262), "magenta": (270, 335)}

def rgb_to_hsv(im):
    im = im.astype(float) / 255.0
    mx, mn = im.max(axis=2), im.min(axis=2); d = mx - mn
    h = np.zeros_like(mx)
    r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]
    m = d > 1e-6
    rc = np.where(m & (mx == r), ((g - b) / np.where(d == 0, 1, d)) % 6, 0)
    gc = np.where(m & (mx == g) & (mx != r), (b - r) / np.where(d == 0, 1, d) + 2, 0)
    bc = np.where(m & (mx == b) & (mx != r) & (mx != g), (r - g) / np.where(d == 0, 1, d) + 4, 0)
    h = (rc + gc + bc) * 60.0
    s = np.where(mx > 0, d / np.where(mx == 0, 1, mx), 0)
    return h, s, mx

def classify(im):
    """Return {class: mask}.  Classes: black, gray, <color>, <color>-light (low saturation tints)."""
    h, s, v = rgb_to_hsv(im)
    masks = {}
    white = (v > 0.92) & (s < 0.10)
    masks["black"] = v < 0.38
    masks["gray"] = (s < 0.14) & (v >= 0.38) & ~white
    colored = ~white & ~masks["black"] & ~masks["gray"]
    hh = np.where(h > 340, h - 360, h)
    for name, (a, b) in PALETTE.items():
        sel = colored & (hh >= a) & (hh < b)
        masks[name] = sel & (s >= 0.42)
        masks[name + "-light"] = sel & (s < 0.42)
    return {k: v for k, v in masks.items() if v.sum() > 60}

def thin(img):
    img = img.copy(); changed = True
    while changed:
        changed = False
        for step in (0, 1):
            P = np.pad(img, 1)
            p2 = P[:-2,1:-1]; p3 = P[:-2,2:]; p4 = P[1:-1,2:]; p5 = P[2:,2:]; p6 = P[2:,1:-1]; p7 = P[2:,:-2]; p8 = P[1:-1,:-2]; p9 = P[:-2,:-2]
            nb = [p2,p3,p4,p5,p6,p7,p8,p9]; Bn = sum(n.astype(int) for n in nb); seq = nb + [p2]
            A = sum(((~seq[i]) & seq[i+1]).astype(int) for i in range(8))
            c1 = ~(p2 & p4 & p6) if step == 0 else ~(p2 & p4 & p8); c2 = ~(p4 & p6 & p8) if step == 0 else ~(p2 & p6 & p8)
            m = img & (Bn >= 2) & (Bn <= 6) & (A == 1) & c1 & c2
            if m.any(): img[m] = False; changed = True
    return img

N8 = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]

def skeleton_graph(mask, w0):
    """Chains between junction nodes of the thinned mask, after removing open arrowheads (two short
    barbs at a junction) and spurs.  Returns (chains, nodes, open_arrowheads)."""
    sk = thin(mask)
    ys, xs = np.where(sk); pix = set(zip(ys.tolist(), xs.tolist()))
    def nb(p): return [(p[0]+dy, p[1]+dx) for dy, dx in N8 if (p[0]+dy, p[1]+dx) in pix]
    RING = [(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1)]
    def cross(p):
        ring = [((p[0]+dy, p[1]+dx) in pix) for dy, dx in RING]
        return sum(1 for i in range(8) if not ring[i] and ring[(i + 1) % 8])
    def is_junc(p): return cross(p) >= 3
    def branch(e, limit):
        path = [e]; prev = None; cur = e
        while True:
            if is_junc(cur) and cur != e: return path, cur
            nxt = [n for n in nb(cur) if n not in path]
            if not nxt: return path, None
            prev, cur = cur, nxt[0]; path.append(cur)
            if len(path) > limit: return path, None
    arrows = []
    # open arrowheads: two barbs of similar length meeting at a junction
    ends = [p for p in pix if len(nb(p)) == 1]
    at_junction = {}
    for e in ends:
        path, j = branch(e, int(6 * w0 + 30))
        if j is not None and 6 <= len(path) <= 6 * w0 + 30: at_junction.setdefault(j, []).append(path)
    for j, paths in at_junction.items():
        if len(paths) < 2: continue
        paths = sorted(paths, key=len)
        for a in range(len(paths)):
            for b in range(a + 1, len(paths)):
                pa, pb = paths[a], paths[b]
                if len(pb) > 1.6 * len(pa): continue
                va = np.array(pa[0]) - np.array(j); vb = np.array(pb[0]) - np.array(j)
                cos = np.dot(va, vb) / (np.hypot(*va) * np.hypot(*vb) + 1e-9)
                if -0.2 < cos < 0.9:
                    arrows.append({"tip": j, "barbs": [pa[0], pb[0]]})
                    for p in pa[:-1] + pb[:-1]: pix.discard(p)
                    break
            else: continue
            break
    # spurs
    spur = int(2.5 * w0 + 4); changed = True
    while changed:
        changed = False
        for e in [p for p in pix if p in pix and len(nb(p)) == 1]:
            path, j = branch(e, spur)
            if j is not None and len(path) <= spur:
                for p in path[:-1]: pix.discard(p)
                changed = True
    for e in [p for p in pix if p in pix and len(nb(p)) == 1]:
        path, j = branch(e, int(6 * w0 + 30))
        if j is not None and len(path) <= 6 * w0 + 30:
            arrows.append({"tip": j, "barbs": [e]})
            for p in path[:-1]: pix.discard(p)
    junc = {p for p in pix if is_junc(p)}
    # junction nodes: adjacent junction pixels
    jl = np.zeros(mask.shape, bool)
    for y, x in junc: jl[y, x] = True
    jl = ndimage.binary_dilation(jl, iterations=1)
    lab, n = ndimage.label(jl, structure=np.ones((3, 3)))
    node_of = {}; members = {}
    for p in pix:
        if lab[p] > 0 and p in junc:
            node_of[p] = lab[p] - 1; members.setdefault(lab[p] - 1, []).append(p)
    rest = pix - set(node_of)
    seen = set(); chains = []
    def rnb(p): return [(p[0]+dy, p[1]+dx) for dy, dx in N8 if (p[0]+dy, p[1]+dx) in rest]
    def touching(p):
        for dy, dx in N8:
            m = (p[0]+dy, p[1]+dx)
            if m in node_of: return node_of[m]
        return None
    def spine(cs, start):
        """The pixel path from start to the farthest pixel of the set, by breadth-first parents."""
        dist = {start: 0}; parent = {start: None}; q = deque([start])
        while q:
            c = q.popleft()
            for m in rnb(c):
                if m in cs and m not in dist: dist[m] = dist[c] + 1; parent[m] = c; q.append(m)
        last = max(dist, key=dist.get); path = []; p = last
        while p is not None: path.append(p); p = parent[p]
        return path[::-1], last, set(dist)
    def extract(pixset, allow_cycles=True):
        seen = set(); found = []; covered = set()
        for p in pixset:
            if p in seen: continue
            comp = []; q = deque([p]); seen.add(p)
            while q:
                c = q.popleft(); comp.append(c)
                for m in rnb(c):
                    if m in pixset and m not in seen: seen.add(m); q.append(m)
            cs = set(comp)
            if len(cs) < 3: continue
            endsc = [c for c in comp if len([m for m in rnb(c) if m in cs]) <= 1 or touching(c) is not None]
            if endsc:
                path, last, reached = spine(cs, endsc[0])
                found.append({"pts": [(float(a), float(b)) for a, b in path], "ends": [touching(endsc[0]), touching(last)]})
            else:
                start = comp[0]; cs2 = cs - {start}; nbs = [m for m in rnb(start) if m in cs2]
                if not nbs: continue
                path, last, reached = spine(cs2, nbs[0]); path = path + [start]
                found.append({"pts": [(float(a), float(b)) for a, b in path], "ends": [None, None], "cycle": True})
            for (y, x) in path:
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1): covered.add((y + dy, x + dx))
        return found, covered
    chains, covered = extract(rest)
    leftover = {p for p in rest if p not in covered}
    if len(leftover) > 8:                      # arms the spines skipped (an undetected junction)
        more, _ = extract(leftover)
        chains += [c for c in more if len(c["pts"]) > 6]
    # merge nodes joined by a very short chain (an X crossing thinned into two Y's)
    parent = list(range(n))
    def find(a):
        while parent[a] != a: parent[a] = parent[parent[a]]; a = parent[a]
        return a
    keep = []
    for c in chains:
        a, b = c["ends"]
        if a is not None and b is not None and a != b and len(c["pts"]) <= 2.5 * w0 + 2:
            ra, rb = find(a), find(b); parent[ra] = rb
            members.setdefault(rb, []).extend(c["pts"])
        else: keep.append(c)
    chains = keep
    roots = sorted({find(i) for i in range(n)})
    index = {r: k for k, r in enumerate(roots)}
    allm = {}
    for i in range(n):
        allm.setdefault(index[find(i)], []).extend(members.get(i, []))
    nodes = [(float(np.mean([p[0] for p in allm[k]])), float(np.mean([p[1] for p in allm[k]]))) if allm.get(k) else (0.0, 0.0) for k in range(len(roots))]
    for c in chains:
        c["ends"] = [None if e is None else index[find(e)] for e in c["ends"]]
    return chains, nodes, arrows

def direction(chain, at_start, w0):
    pts = chain["pts"]; k = min(len(pts) - 1, max(6, int(2.5 * w0)))
    if len(pts) < 2: return None
    a, b = (pts[0], pts[k]) if at_start else (pts[-1], pts[-1 - k])
    v = np.array([b[0] - a[0], b[1] - a[1]], float); n = np.hypot(*v)
    return v / n if n else None

def assemble(chains, nodes, w0, min_spur):
    # prune spurs: chains with a free end and short length
    chains = list(chains)
    # pair chain ends at each node by direction
    incident = {}
    for i, c in enumerate(chains):
        for side in (0, 1):
            nd = c["ends"][side]
            if nd is not None: incident.setdefault(nd, []).append((i, side))
    pair = {}
    for nd, ends in incident.items():
        dirs = {}
        for (i, side) in ends:
            d = direction(chains[i], side == 0, w0)
            dirs[(i, side)] = d if d is not None else np.zeros(2)
        remaining = list(ends)
        while len(remaining) > 1:
            best, bestv = None, -2
            for a in range(len(remaining)):
                for b in range(a + 1, len(remaining)):
                    v = -float(np.dot(dirs[remaining[a]], dirs[remaining[b]]))   # 1 when opposite
                    if v > bestv: bestv, best = v, (remaining[a], remaining[b])
            if bestv < 0.2: break        # not close to straight-through: leave the rest unpaired
            pair[best[0]] = best[1]; pair[best[1]] = best[0]
            remaining.remove(best[0]); remaining.remove(best[1])
    # walk
    used = set(); curves = []
    for i, c in enumerate(chains):
        if i in used: continue
        seq = list(c["pts"]); used.add(i); closed = bool(c.get("cycle"))
        # extend forward from (i,1)
        for side, forward in ((1, True), (0, False)):
            cur = (i, side)
            while cur in pair:
                j, jside = pair[cur]
                if j in used:
                    if j == i: closed = True
                    break
                used.add(j)
                nd = nodes[chains[j]["ends"][jside]]
                pts = chains[j]["pts"] if jside == 0 else chains[j]["pts"][::-1]
                if forward: seq = seq + [(nd[0], nd[1])] + pts
                else: seq = pts[::-1] + [(nd[0], nd[1])] + seq
                cur = (j, 1 - jside)
        # a chain ending at an unpaired node still reaches the node center
        curves.append({"pts": seq, "closed": closed})
    return curves

def simplify(points, eps):
    pts = np.asarray(points, float)
    if len(pts) < 3: return pts
    a, b = pts[0], pts[-1]; ab = b - a; n = np.hypot(*ab)
    d = np.abs(ab[0] * (pts - a)[:, 1] - ab[1] * (pts - a)[:, 0]) / n if n > 1e-9 else np.hypot(*(pts - a).T)
    i = int(np.argmax(d))
    if d[i] > eps: return np.vstack([simplify(pts[:i+1], eps)[:-1], simplify(pts[i:], eps)])
    return np.vstack([a, b])

def resample(points, step):
    pts = np.asarray(points, float)
    if len(pts) < 2: return pts
    seg = np.hypot(*np.diff(pts, axis=0).T); s = np.concatenate([[0], np.cumsum(seg)])
    if s[-1] < step: return pts[[0, -1]]
    t = np.arange(0, s[-1], step); t = np.append(t, s[-1])
    return np.column_stack([np.interp(t, s, pts[:,0]), np.interp(t, s, pts[:,1])])


def end_dir(pts, at_start, k=8):
    n = min(len(pts) - 1, k)
    a, b = (pts[0], pts[n]) if at_start else (pts[-1], pts[-1 - n])
    v = np.array([a[0] - b[0], a[1] - b[1]], float); m = np.hypot(*v)      # points outward from the curve
    return v / m if m else np.zeros(2)

def bridge(curves, gapmax, minlong=40):
    """Merge open curves across small gaps (one color drawn over another, or a blanked label)."""
    curves = [c for c in curves]
    changed = True
    while changed:
        changed = False; best = None
        for i, a in enumerate(curves):
            if a["closed"]: continue
            for j, b in enumerate(curves):
                if j <= i or b["closed"]: continue
                if len(a["pts"]) < minlong and len(b["pts"]) < minlong: continue
                for sa in (0, 1):
                    for sb in (0, 1):
                        pa = a["pts"][0 if sa == 0 else -1]; pb = b["pts"][0 if sb == 0 else -1]
                        d = math.hypot(pa[0] - pb[0], pa[1] - pb[1])
                        if d > gapmax or d < 1e-6: continue
                        da = end_dir(a["pts"], sa == 0); db = end_dir(b["pts"], sb == 0)
                        link = np.array([pb[0] - pa[0], pb[1] - pa[1]]) / d
                        if np.dot(da, link) < 0.55 or np.dot(db, -link) < 0.55: continue
                        score = d - 10 * (np.dot(da, link) + np.dot(db, -link))
                        if best is None or score < best[0]: best = (score, i, j, sa, sb)
        if best:
            _, i, j, sa, sb = best
            a, b = curves[i], curves[j]
            pa = a["pts"] if sa == 1 else a["pts"][::-1]      # a ends at the gap
            pb = b["pts"] if sb == 0 else b["pts"][::-1]      # b starts at the gap
            merged = {"pts": pa + pb, "closed": False, "w": a.get("w", b.get("w")), "band": a.get("band", False), "rgb": a.get("rgb")}
            curves = [c for k, c in enumerate(curves) if k not in (i, j)] + [merged]; changed = True
    for c in curves:            # close a curve whose ends meet
        if not c["closed"] and len(c["pts"]) > 60:
            p, q = c["pts"][0], c["pts"][-1]
            if math.hypot(p[0] - q[0], p[1] - q[1]) < gapmax and np.dot(end_dir(c["pts"], True), end_dir(c["pts"], False)) < -0.3: c["closed"] = True
    return curves

def chain_bits(bits, gapmax=45):
    """Order short pieces (dashes, dots) into dotted curves by nearest neighbor."""
    bits = list(bits); out = []
    while bits:
        y, x = bits.pop(0); chain = [(y, x)]; grown = True
        while grown:
            grown = False
            for end in (0, -1):
                cy, cx = chain[end]
                cand = [(math.hypot(b[0] - cy, b[1] - cx), k) for k, b in enumerate(bits)]
                if cand:
                    d, k = min(cand)
                    if d < gapmax:
                        b = bits.pop(k); chain = ([b] + chain) if end == 0 else (chain + [b]); grown = True
        if len(chain) >= 3:
            gaps = [math.hypot(a[0] - b[0], a[1] - b[1]) for a, b in zip(chain, chain[1:])]
            if np.std(gaps) > 0.6 * np.mean(gaps): continue        # not evenly spaced: noise, not dashes
            closed = math.hypot(chain[0][0] - chain[-1][0], chain[0][1] - chain[-1][1]) < gapmax and len(chain) > 6
            out.append({"pts": chain, "closed": closed})
    return out

def find_dots(black):
    """Round black blobs, found by erosion so lines touching them do not hide them."""
    core = ndimage.binary_erosion(black, iterations=5)
    lab, n = ndimage.label(core); dots = []
    H, W = black.shape; yy, xx = np.ogrid[:H, :W]
    for i in range(1, n + 1):
        comp = lab == i; ys, xs = np.where(comp)
        if len(ys) < 12: continue
        rmax = float(ndimage.distance_transform_edt(comp).max())
        if len(ys) > 1.25 * math.pi * rmax * rmax + 6: continue        # the core is not a disk: a line piece or a triangle
        cx, cy = xs.mean(), ys.mean(); r = math.sqrt(len(ys) / math.pi) + 5
        disk = (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r
        if (black & disk).sum() > 0.85 * disk.sum() and 7 <= r < 45:
            ang = np.linspace(0, 2 * math.pi, 96, endpoint=False); rr = r + 7
            hits = []
            for a in ang:
                px_, py_ = int(round(cx + rr * math.cos(a))), int(round(cy + rr * math.sin(a)))
                hits.append(bool(0 <= py_ < H and 0 <= px_ < W and black[py_, px_]))
            runs = sum(1 for i in range(96) if hits[i] and not hits[i - 1])
            if runs > 2: continue                       # three or more strokes meet here: a junction, not a dot
            dots.append((cx, cy, r, disk))
    return dots

def trace_panel(png, labels, eps_px=1.5):
    im = np.asarray(Image.open(png).convert("RGB")).astype(int); H, W, _ = im.shape
    for l in labels:      # blank the label text, with a small margin
        x0, x1 = int((l["x0"] - 1.0) / K), int((l["x1"] + 1.0) / K); y0, y1 = int(H - (l["y1"] + 1.0) / K), int(H - (l["y0"] - 1.0) / K)
        im[max(0, y0):min(H, y1), max(0, x0):min(W, x1)] = 255
    masks = classify(im)
    for cls in list(masks):
        if cls.endswith("-light") and cls[:-6] in masks:
            fringe = ndimage.binary_dilation(masks[cls[:-6]], iterations=4)
            masks[cls] = masks[cls] & ~fringe
            if masks[cls].sum() < 200: del masks[cls]
    out = {"size_pt": [round(W * K, 2), round(H * K, 2)], "curves": [], "dots": [], "arrowheads": [], "regions": [],
           "colors": {cls: "#%02x%02x%02x" % tuple(int(v) for v in im[m].mean(axis=0)) for cls, m in masks.items() if m.sum() > 0}}
    topt = lambda p: [round(p[1] * K, 2), round((H - p[0]) * K, 2)]
    for cls, mask in masks.items():
        mask = ndimage.binary_opening(ndimage.binary_closing(mask, iterations=1), iterations=1)
        mask = ndimage.binary_fill_holes(mask) if cls in ("gray",) else mask
        if cls.endswith("-light"):
            closed = ndimage.binary_fill_holes(ndimage.binary_closing(mask, iterations=6))
            lab0, n0 = ndimage.label(closed, structure=np.ones((3, 3)))
            keep = np.zeros_like(mask)
            for i0 in range(1, n0 + 1):
                comp0 = lab0 == i0
                if ndimage.distance_transform_edt(comp0).max() > 9: keep |= comp0      # a band: use the closed shape
                else: keep |= comp0 & mask                                              # a thin strand: as drawn
            mask = keep
        if not cls.endswith("-light"):
            for cx, cy, r, disk in find_dots(mask):
                out["dots"].append({"x": round(cx * K, 2), "y": round((H - cy) * K, 2), "r": round(r * K, 2), "color": cls,
                                    "rgb": "#%02x%02x%02x" % tuple(int(v) for v in im[disk & mask].mean(axis=0))})
                mask = mask & ~ndimage.binary_dilation(disk, iterations=5)
        lab, n = ndimage.label(mask, structure=np.ones((3, 3)))
        sizes = ndimage.sum(mask, lab, range(1, n + 1))
        small_bits = []; class_curves = []; class_w = []
        for i in range(1, n + 1):
            comp = lab == i; area = sizes[i - 1]
            if area < 12: continue
            ys, xs = np.where(comp); h, w = np.ptp(ys) + 1, np.ptp(xs) + 1
            dist = ndimage.distance_transform_edt(comp)
            rmax = dist.max()
            if cls == "gray":
                if area < 1500: continue
                if True:
                    from scipy.spatial import ConvexHull
                    pts = np.column_stack([xs, ys]); hull = ConvexHull(pts); poly = pts[hull.vertices]
                    poly = simplify(np.vstack([poly, poly[:1]]), 3.0)[:-1]
                    out["regions"].append({"color": "gray", "points": [[round(x * K, 2), round((H - y) * K, 2)] for x, y in poly]}); continue
            if area < 60 and rmax < 6:
                small_bits.append((ys.mean(), xs.mean())); continue
            sk_w = 2 * float(np.median(dist[thin(comp)])) if area > 30 else 2 * rmax
            w0 = max(1.5, sk_w / 2)
            comp_rgb = "#%02x%02x%02x" % tuple(int(v) for v in im[comp].mean(axis=0))
            # arrowheads: places where the half-width is well above the stroke's (not on bands)
            arrow_core = comp & (dist > 1.75 * w0 + 1.0) if not (cls.endswith("-light") or rmax > 9) else np.zeros_like(comp)
            al, an = ndimage.label(arrow_core, structure=np.ones((3, 3)))
            work = comp.copy()
            for j in range(1, an + 1):
                cy, cx = np.where(al == j)
                if len(cy) < 4: continue
                # the arrowhead region: mask pixels near the core
                near = comp & (ndimage.distance_transform_edt(~(al == j)) < 2.6 * w0 + 2)
                py, px = np.where(near)
                P = np.column_stack([px, py]).astype(float); c0 = P.mean(axis=0)
                u, sv, vt = np.linalg.svd(P - c0, full_matrices=False); axis = vt[0]
                proj = (P - c0) @ axis; perp = (P - c0) @ vt[1]
                hi, lo = proj.max(), proj.min()
                spread_hi = np.abs(perp[proj > hi - 0.25 * (hi - lo)]).mean(); spread_lo = np.abs(perp[proj < lo + 0.25 * (hi - lo)]).mean()
                if spread_hi < spread_lo: tip = P[np.argmax(proj)]; base_sel = proj < lo + 0.3 * (hi - lo)
                else: tip = P[np.argmin(proj)]; base_sel = proj > hi - 0.3 * (hi - lo)
                bp = P[base_sel]; bperp = (bp - c0) @ vt[1]
                b1, b2 = bp[np.argmax(bperp)], bp[np.argmin(bperp)]
                if np.hypot(*(b1 - b2)) < max(2.2 * w0, 12): continue     # not wider than the stroke: not an arrowhead
                out["arrowheads"].append({"color": cls, "tip": [round(tip[0] * K, 2), round((H - tip[1]) * K, 2)],
                                          "base": [[round(b1[0] * K, 2), round((H - b1[1]) * K, 2)], [round(b2[0] * K, 2), round((H - b2[1]) * K, 2)]]})
                # replace the arrowhead by a thin line along its axis so the curve stays connected
                work[near] = False
                base_mid = (b1 + b2) / 2; axis_v = tip - base_mid; axis_v = axis_v / (np.hypot(*axis_v) + 1e-9)
                ext = 3.0 * w0 + 6
                p0 = base_mid - ext * axis_v; p1 = tip + ext * axis_v; L = int(np.hypot(*(p1 - p0))) + 1
                for t in np.linspace(0, 1, 2 * L + 2):
                    q = p0 + t * (p1 - p0)
                    yy, xx = int(round(q[1])), int(round(q[0]))
                    work[max(0, yy - 1):yy + 2, max(0, xx - 1):xx + 2] = True
            chains, nodes, open_arrows = skeleton_graph(work, w0)
            for a in open_arrows:
                out["arrowheads"].append({"color": cls, "open": True, "tip": [round(a["tip"][1] * K, 2), round((H - a["tip"][0]) * K, 2)],
                                          "base": [[round(b[1] * K, 2), round((H - b[0]) * K, 2)] for b in a["barbs"]]})
            for cv in assemble(chains, nodes, w0, min_spur=max(8, int(2.5 * w0))):
                cv["w"] = sk_w; cv["band"] = bool(rmax > 9); cv["rgb"] = comp_rgb; class_curves.append(cv)
        # bridge gaps across the whole class, then separate short pieces (dashes) from curves
        wmed = float(np.median([c["w"] for c in class_curves])) if class_curves else 4.0
        merged = bridge(class_curves, gapmax=max(2.0 * wmed + 14, 55))
        short = [cv for cv in merged if not cv["closed"] and len(cv["pts"]) < 90]
        cents = {id(cv): (float(np.mean([p[0] for p in cv["pts"]])), float(np.mean([p[1] for p in cv["pts"]]))) for cv in short}
        plen = {tuple(v): len(cv["pts"]) for cv, v in ((cv, cents[id(cv)]) for cv in short)}
        chained_ids = set()
        medlen = float(np.median([len(cv["pts"]) for cv in short])) if short else 10.0
        for ch in chain_bits(list(cents.values()) + small_bits, gapmax=max(45.0, 2.6 * medlen + 20)):
            lens = [plen.get(tuple(p), 3) for p in ch["pts"]]
            spacing = float(np.median([math.hypot(a[0] - b[0], a[1] - b[1]) for a, b in zip(ch["pts"], ch["pts"][1:])]))
            dash = float(np.median(lens)) + wmed; gap = max(spacing - dash, 0.3 * dash)
            piece_w = [cv["w"] for cv in short if tuple(cents[id(cv)]) in {tuple(p) for p in ch["pts"]} and cv.get("w")]
            wdot = float(np.median(piece_w)) if piece_w else min(wmed, 6.0)
            out["curves"].append({"color": cls, "closed": ch["closed"], "width": round(wdot * K, 2), "dotted": True, "band": False,
                                  "dash": [round(dash * K, 2), round(gap * K, 2)],
                                  "points": [[round(x * K, 2), round((H - y) * K, 2)] for y, x in ch["pts"]]})
            for cv in short:
                if tuple(cents[id(cv)]) in {tuple(p) for p in ch["pts"]}: chained_ids.add(id(cv))
        small_bits = []
        for cv in merged:
            if cv["closed"] and len(cv["pts"]) < 40: continue
            if id(cv) in chained_ids: continue
            if len(cv["pts"]) < 34 and not cv["closed"]: continue
            arr = np.array([(p[1], p[0]) for p in cv["pts"]], float)
            if len(arr) > 9:
                k = np.ones(5) / 5
                sm = np.column_stack([np.convolve(arr[:, 0], k, mode="valid"), np.convolve(arr[:, 1], k, mode="valid")])
                arr = np.vstack([arr[:2], sm, arr[-2:]])
            if cv["closed"]: arr = np.vstack([arr, arr[:1]])
            simp = simplify(resample(arr, 2.0), max(eps_px, 2.0))
            if cv["closed"] and len(simp) > 2: simp = simp[:-1]
            out["curves"].append({"color": cls, "closed": bool(cv["closed"]), "width": round(cv.get("w", wmed) * K, 2), "band": cv.get("band", False), "rgb": cv.get("rgb"),
                                  "points": [[round(x * K, 2), round((H - y) * K, 2)] for x, y in simp]})
    kept = []
    for a in sorted(out["arrowheads"], key=lambda a: -len(a["base"])):
        if all(math.hypot(a["tip"][0] - b["tip"][0], a["tip"][1] - b["tip"][1]) > 3.0 for b in kept): kept.append(a)
    out["arrowheads"] = kept
    return out

def overlay(png, out, path):
    from PIL import ImageDraw
    im = Image.open(png).convert("RGB"); d = ImageDraw.Draw(im); H = im.height
    px = lambda p: (p[0] / K, H - p[1] / K)
    for c in out["curves"]:
        pts = [px(p) for p in c["points"]]
        if c["closed"]: pts.append(pts[0])
        col = {"red": "darkred", "blue": "navy", "gold": "darkgoldenrod", "black": "green", "magenta": "purple", "green": "darkgreen", "gray": "gray"}.get(c["color"].replace("-light", ""), "cyan")
        d.line(pts, fill=col, width=3)
        for p in pts: d.ellipse([p[0]-3, p[1]-3, p[0]+3, p[1]+3], outline="lime")
    for a in out["arrowheads"]:
        if a.get("open"):
            for b in a["base"]: d.line([px(b), px(a["tip"])], fill="magenta", width=3)
        else: d.polygon([px(a["tip"]), px(a["base"][0]), px(a["base"][1])], outline="magenta", width=3)
    for dt in out["dots"]:
        c = px([dt["x"], dt["y"]]); r = dt["r"] / K; d.ellipse([c[0]-r, c[1]-r, c[0]+r, c[1]+r], outline="cyan", width=3)
    for r in out["regions"]:
        d.polygon([px(p) for p in r["points"]], outline="orange", width=3)
    im.save(path)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 5:
        sys.exit("usage: trace-figure.py <crop.png> <labels.json> <out.json> <overlay.png>")
    labels = json.load(open(sys.argv[2]))
    result = trace_panel(sys.argv[1], labels)
    json.dump(result, open(sys.argv[3], "w"))
    overlay(sys.argv[1], result, sys.argv[4])
    print("curves", len(result["curves"]), "arrowheads", len(result["arrowheads"]), "dots", len(result["dots"]), "regions", len(result["regions"]))
