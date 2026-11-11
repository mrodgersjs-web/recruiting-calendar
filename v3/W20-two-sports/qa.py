# -*- coding: utf-8 -*-
"""Layout QA for the two plain decks: ink per page, margins, biggest white gap."""
import sys, glob
from PIL import Image
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

def audit(folder, label):
    print("\n=== %s ===" % label)
    files = sorted(glob.glob(folder + r"\page_*.png"))
    for f in files:
        im = Image.open(f).convert("L")
        w, h = im.size
        px = im.load()
        dark_cols = [0] * w
        dark_rows = [0] * h
        ink = 0
        for y in range(h):
            run = 0
            for x in range(w):
                if px[x, y] < 200:
                    run += 1
                    dark_cols[x] += 1
            dark_rows[y] = run
            ink += run
        rows_used = [y for y in range(h) if dark_rows[y] > 0]
        cols_used = [x for x in range(w) if dark_cols[x] > 0]
        # biggest white gap inside the body (skip header band 6% and footer band 6%)
        lo, hi = int(h * 0.055), int(h * 0.945)
        gap = best = 0
        for y in range(lo, hi):
            if dark_rows[y] == 0:
                gap += 1
                best = max(best, gap)
            else:
                gap = 0
        mm = lambda p: round(p / (w / 8.5) * 25.4, 1)
        print("p%s ink %.1f%%  left %smm right %smm top %smm bottom %smm  biggest white gap %dpx (%smm)" % (
            f[-7:-4], 100.0 * ink / (w * h),
            mm(cols_used[0]), mm(w - 1 - cols_used[-1]), mm(rows_used[0]), mm(h - 1 - rows_used[-1]),
            best, mm(best)))

audit(r"C:\Users\Jloeh\.aside\u\1\sessions\2026-11-08_sIbJ63jY5p1sXMzN\tmp\pb20\pages\wbb", "WOMENS BASKETBALL 15pp")
audit(r"C:\Users\Jloeh\.aside\u\1\sessions\2026-11-08_sIbJ63jY5p1sXMzN\tmp\pb20\pages\fb", "FOOTBALL 17pp")
