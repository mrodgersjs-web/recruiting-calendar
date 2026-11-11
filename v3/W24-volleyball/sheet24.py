# -*- coding: utf-8 -*-
"""Proof images for W24: a contact sheet of the volleyball deck, and a crop of the
two pages that carry the sample email and the size ladder."""
import glob, re, sys, os
from PIL import Image, ImageDraw
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

T = r"C:\Users\Jloeh\.aside\u\1\sessions\2026-11-08_sIbJ63jY5p1sXMzN\tmp\pb24"
P = T + r"\pages"
TMP = r"C:\Users\Jloeh\.aside\u\1\sessions\2026-11-08_sIbJ63jY5p1sXMzN\tmp"

files = sorted(glob.glob(P + r"\page_*.png"))
pages = [Image.open(f).convert("RGB") for f in files]
cols = 6
rows = (len(pages) + cols - 1) // cols
tw, th = 260, int(260 * pages[0].size[1] / pages[0].size[0])
sheet = Image.new("RGB", (cols * (tw + 8) + 8, rows * (th + 26) + 8), "#ffffff")
d = ImageDraw.Draw(sheet)
for i, im in enumerate(pages):
    r, c = divmod(i, cols)
    x = 8 + c * (tw + 8); y = 8 + r * (th + 26)
    sheet.paste(im.resize((tw, th), Image.LANCZOS), (x, y))
    d.text((x + 2, y + th + 6), "%02d" % (i + 1), fill="#141414")
out = TMP + r"\sheet-volleyball-31pp.png"
sheet.save(out)
print("contact sheet", sheet.size, "->", out)

def page_of(dump, needle):
    txt = open(dump, encoding="utf-8").read()
    parts = re.split(r"===== PAGE (\d+) =====", txt)
    for i in range(1, len(parts) - 1, 2):
        if needle in parts[i + 1]:
            return int(parts[i])
    return None

for label, needle in [("email page", "Madison Weber"), ("ladder page", "Counted roster heights"),
                      ("calendar page", "Badger Region Qualifier at the")]:
    n = page_of(T + r"\..\..\vb-text.txt" if False else r"C:\Users\Jloeh\Developer\recruiting-calendar\v3\W24-volleyball\vb-text.txt", needle)
    print(label, "->", "page", n)
    if n:
        pages[n - 1].save(TMP + r"\proof-vb-%s.png" % label.split()[0])
