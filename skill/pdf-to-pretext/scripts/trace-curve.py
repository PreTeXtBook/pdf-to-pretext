#!/usr/bin/env python3
"""Trace one simple (non-self-crossing) curve of a single color in a rendered figure, for
recreating a hand-drawn arc in PreFigure.

Usage: trace-curve.py <crop.png> red|black <out.json> <overlay.png>

The PNG is a 600-dpi render of the figure's crop (pdftoppm -r 600 -x -y -W -H).  The curve's
pixels are thinned to a skeleton, ordered from the endpoint lowest on the page along the
skeleton to the farthest endpoint, sampled by arc length, and simplified (Douglas-Peucker,
1.5 px).  The JSON holds "dense" (every 10 px) and "simple" point lists in PDF points from
the crop's lower-left corner, ready for a PreFigure spline with chord-length t-values; the
overlay marks the simplified points (green), the start (blue), and the end (magenta) on
the image, which is the check to make.  Needs numpy, scipy, Pillow."""
import venv_python; venv_python.ensure("numpy", "scipy", "PIL")
import sys, json, numpy as np
from collections import deque
from PIL import Image, ImageDraw
from scipy import ndimage
png, color, out, overlay = sys.argv[1:5]
im = np.asarray(Image.open(png).convert("RGB")).astype(int)
H, W, _ = im.shape
R, G, B = im[:,:,0], im[:,:,1], im[:,:,2]
if color == "red": mask = (R > 130) & (R - G > 50) & (R - B > 50)
else: mask = im.max(axis=2) < 110
mask = ndimage.binary_closing(mask, iterations=1)
mask = ndimage.binary_dilation(mask, iterations=1)

def thin(img):
    img = img.copy(); changed = True
    while changed:
        changed = False
        for step in (0, 1):
            P = np.pad(img, 1)
            p2 = P[:-2,1:-1]; p3 = P[:-2,2:]; p4 = P[1:-1,2:]; p5 = P[2:,2:]; p6 = P[2:,1:-1]; p7 = P[2:,:-2]; p8 = P[1:-1,:-2]; p9 = P[:-2,:-2]
            nb = [p2,p3,p4,p5,p6,p7,p8,p9]
            Bn = sum(n.astype(int) for n in nb)
            seq = nb + [p2]
            A = sum(((~seq[i]) & seq[i+1]).astype(int) for i in range(8))
            if step == 0: c1 = ~(p2 & p4 & p6); c2 = ~(p4 & p6 & p8)
            else: c1 = ~(p2 & p4 & p8); c2 = ~(p2 & p6 & p8)
            m = img & (Bn >= 2) & (Bn <= 6) & (A == 1) & c1 & c2
            if m.any(): img[m] = False; changed = True
    return img
sk = thin(mask)
ys, xs = np.where(sk)
pix = set(zip(ys.tolist(), xs.tolist()))
def nbrs(p):
    y, x = p
    return [(y+dy, x+dx) for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx) and (y+dy, x+dx) in pix]
ends = [p for p in pix if len(nbrs(p)) == 1]
print("skeleton px", len(pix), "endpoints", len(ends))
start = max(ends, key=lambda p: p[0])          # lowest on the page = largest y
dist = {start: 0}; parent = {start: None}; q = deque([start])
while q:
    p = q.popleft()
    for n in nbrs(p):
        if n not in dist: dist[n] = dist[p] + 1; parent[n] = p; q.append(n)
end = max((e for e in ends if e in dist), key=lambda e: dist[e])
path = []; p = end
while p is not None: path.append(p); p = parent[p]
path.reverse()
print("start px", start[::-1], "end px", end[::-1], "path length px", len(path))
pts = np.array([(x, y) for y, x in path], float)
seg = np.hypot(*np.diff(pts, axis=0).T); s = np.concatenate([[0], np.cumsum(seg)])
def sample(step):
    t = np.arange(0, s[-1], step); t = np.append(t, s[-1])
    return np.column_stack([np.interp(t, s, pts[:,0]), np.interp(t, s, pts[:,1])])
def dp(points, eps):
    if len(points) < 3: return points
    a, b = points[0], points[-1]
    ab = b - a; n = np.hypot(*ab)
    d = np.abs((ab[0] * (points - a)[:, 1] - ab[1] * (points - a)[:, 0])) / n if n else np.hypot(*(points - a).T)
    i = int(np.argmax(d))
    if d[i] > eps:
        return np.vstack([dp(points[:i+1], eps)[:-1], dp(points[i:], eps)])
    return np.vstack([a, b])
dense = sample(10.0)
simple = dp(sample(2.0), 1.5)
print("dense points", len(dense), "simplified points", len(simple), "total length px", round(s[-1]))
K = 72 / 600
conv = lambda P: [[round(x * K, 2), round((H - y) * K, 2)] for x, y in P]
json.dump({"width_pt": round(W * K, 2), "height_pt": round(H * K, 2), "start_px": [int(start[1]), int(start[0])], "end_px": [int(end[1]), int(end[0])],
           "dense": conv(dense), "simple": conv(simple)}, open(out, "w"))
img = Image.open(png).convert("RGB"); d = ImageDraw.Draw(img)
for x, y in simple: d.ellipse([x-5, y-5, x+5, y+5], outline="green", width=2)
d.ellipse([start[1]-9, start[0]-9, start[1]+9, start[0]+9], outline="blue", width=3)
d.ellipse([end[1]-9, end[0]-9, end[1]+9, end[0]+9], outline="magenta", width=3)
img.save(overlay)
