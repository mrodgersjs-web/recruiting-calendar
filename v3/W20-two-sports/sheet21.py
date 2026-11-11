# -*- coding: utf-8 -*-
"""Proof images for the W21 formatting pass: one contact sheet per deck, plus a
close pair showing the callout page and the fresh start of chapter 3."""
import glob, sys
from PIL import Image, ImageDraw
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

T = r"C:\Users\Jloeh\.aside\u\1\sessions\2026-11-08_sIbJ63jY5p1sXMzN\tmp\pb20\pages"
A = r"C:\Users\Jloeh\.aside\u\1\sessions\2026-11-08_sIbJ63jY5p1sXMzN\tmp\pb20"


def thumb(src, w):
    im = Image.open(src).convert("RGB")
    return im.resize((w, int(im.height * (w / im.width))))


def sheet(dirs, cols, cellw, out, title):
    files = []
    for d in dirs:
        files += sorted(glob.glob(T + "\\" + d + r"\page_*.png"))
    ims = [thumb(f, cellw) for f in files]
    per = max(im.height for im in ims) + 26
    rows = (len(ims) + cols - 1) // cols
    canvas = Image.new("RGB", (cols * (cellw + 10) + 10, rows * per + 44), "#e8e2d4")
    dr = ImageDraw.Draw(canvas)
    dr.text((12, 10), title, fill="#141414")
    for n, im in enumerate(ims):
        r, c = divmod(n, cols)
        x = 10 + c * (cellw + 10)
        y = 34 + r * per
        canvas.paste(im, (x, y))
        dr.text((x + 2, y + im.height + 6), "page %d" % (n + 1), fill="#4a4438")
    canvas.save(out)
    print(out, canvas.size)


sheet(["wbb7"], 8, 236, A + r"\sheet-girls-16pp.png", "Girls' basketball playbook - 16 pages, no split blocks")
sheet(["fb7"], 9, 236, A + r"\sheet-football-18pp.png", "Football playbook - 18 pages, no split blocks")

pair = Image.new("RGB", (2 * 620 + 30, 880 + 40), "#e8e2d4")
dr = ImageDraw.Draw(pair)
dr.text((12, 10), "Football, pages 4 and 5: the callout holds together, chapter 3 starts fresh", fill="#141414")
for n, pg in enumerate(("page_004.png", "page_005.png")):
    pair.paste(thumb(T + r"\fb7" + "\\" + pg, 620), (10 + n * 630, 34))
pair.save(A + r"\proof-p4-p5.png")
print(A + r"\proof-p4-p5.png", pair.size)
