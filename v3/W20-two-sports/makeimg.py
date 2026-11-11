# -*- coding: utf-8 -*-
"""Make the two proof images for the report: three covers side by side, and a
two-row contact sheet of the new decks."""
import glob, sys
from PIL import Image
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
T = r"C:\Users\Jloeh\.aside\u\1\sessions\2026-11-08_sIbJ63jY5p1sXMzN\tmp\pb20\pages"
A = r"C:\Users\Jloeh\.aside\u\1\sessions\2026-11-08_sIbJ63jY5p1sXMzN\tmp\pb20"

def thumb(src, w):
    im = Image.open(src).convert("RGB"); r = w / im.width
    return im.resize((w, int(im.height * r)))

covers = [thumb(T + r"\..\wbb_cover.png" if False else f, 380) for f in
          (glob.glob(A + r"\cover_*.png") or [])]
row = ["wbb3", "fb3"]
# covers: first page of each rendered set, plus the mens reprint rendered below
def grid(dirs, cols, cellw, out, gap=10):
    files = []
    for d in dirs:
        files += sorted(glob.glob(T + "\\" + d + r"\page_*.png"))
    ims = [thumb(f, cellw) for f in files]
    per = max(im.height for im in ims)
    rows = (len(ims) + cols - 1) // cols
    W = cols * cellw + (cols + 1) * gap
    H = rows * (per + gap) + gap
    sheet = Image.new("RGB", (W, H), (60, 55, 48))
    for i, im in enumerate(ims):
        r, c = divmod(i, cols)
        sheet.paste(im, (gap + c * (cellw + gap), gap + r * (per + gap)))
    sheet.save(out)
    print(out, sheet.size, "from", len(ims), "pages")

grid(row, 7, 300, A + r"\proof-contact-sheets.png")
