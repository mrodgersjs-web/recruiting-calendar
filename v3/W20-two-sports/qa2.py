# -*- coding: utf-8 -*-
"""Layout QA: ink per page, real margins, biggest white gap. Usage: qa2.py <png dir> <label>"""
import sys, glob, re
from PIL import Image
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

folder, label = sys.argv[1], sys.argv[2]
print("\n=== %s ===" % label)
worst = []
for f in sorted(glob.glob(folder + r"\page_*.png")):
    im = Image.open(f).convert("L"); w, h = im.size; px = im.load()
    dark_rows = [0] * h; ink = 0
    for y in range(h):
        run = sum(1 for x in range(w) if px[x, y] < 200)
        dark_rows[y] = run; ink += run
    # ignore the full-bleed header hairline at the top and the footer one
    rows = [y for y in range(h) if dark_rows[y] > 2]
    lo, hi = int(h * 0.06), int(h * 0.93)
    gap = best = 0
    for y in range(lo, hi):
        if dark_rows[y] <= 2:
            gap += 1; best = max(best, gap)
        else:
            gap = 0
    dpi = w / 8.5
    mm = lambda p: round(p / dpi * 25.4, 1)
    firstcol = next((x for x in range(w) if any(px[x, y] < 200 for y in rows)), w)
    lastcol = next((x for x in range(w - 1, -1, -1) if any(px[x, y] < 200 for y in rows)), 0)
    print("p%s ink %.1f%%  text block %s-%smm  gap %smm  bottom fill to %smm" % (
        f[-7:-4], 100.0 * ink / (w * h), mm(firstcol), mm(lastcol), mm(best), mm(rows[-1])))
    worst.append((best, f[-7:-4]))
worst.sort(reverse=True)
print("largest gaps:", [(g, mm(g)) for g, _ in worst[:3]][0][0], "px ->", mm(worst[0][0]), "mm on page", worst[0][1])
