# -*- coding: utf-8 -*-
import sys
from PIL import Image
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
f = r"C:\Users\Jloeh\.aside\u\1\sessions\2026-11-08_sIbJ63jY5p1sXMzN\tmp\pb20\pages\wbb\page_003.png"
im = Image.open(f).convert("L"); w, h = im.size; px = im.load()
print("size", w, h)
for x in (0, 1, 2, 3, 5, 10, 20, 40, 60, 80, w - 80, w - 60, w - 40, w - 20, w - 10, w - 5, w - 3, w - 1):
    ys = [y for y in range(h) if px[x, y] < 200]
    bands = []
    prev = -9
    for y in ys:
        if y != prev + 1:
            bands.append([y, y])
        else:
            bands[-1][1] = y
        prev = y
    print("x=%-5d dark px=%-5d bands=%s" % (x, len(ys), [(b[0], b[1]) for b in bands][:6]))
# horizontal profile of row y=200..260 to find the pagehead rule extent
for y in (int(h * 0.055), int(h * 0.06), int(h * 0.065), int(h * 0.07), int(h * 0.11)):
    xs = [x for x in range(w) if px[x, y] < 200]
    print("y=%-5d first=%s last=%s count=%d" % (y, xs[0] if xs else None, xs[-1] if xs else None, len(xs)))
