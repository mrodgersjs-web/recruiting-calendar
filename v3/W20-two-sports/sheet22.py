# -*- coding: utf-8 -*-
"""Proof images for W22: the two pages that now carry the rewritten email, side by
side, plus a contact sheet of each deck."""
import glob, re, sys
from PIL import Image, ImageDraw
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

T = r"C:\Users\Jloeh\.aside\u\1\sessions\2026-11-08_sIbJ63jY5p1sXMzN\tmp\pb20"
P = T + r"\pages"


def page_of(dump, needle):
    txt = open(dump, encoding="utf-8").read()
    parts = re.split(r"===== PAGE (\d+) =====", txt)
    for i in range(1, len(parts) - 1, 2):
        if needle in parts[i + 1]:
            return int(parts[i])
    return None


def thumb(src, w):
    im = Image.open(src).convert("RGB")
    return im.resize((w, int(im.height * (w / im.width))))


def sheet(folder, cols, cellw, out, title):
    files = sorted(glob.glob(P + "\\" + folder + r"\page_*.png"))
    ims = [thumb(f, cellw) for f in files]
    per = max(im.height for im in ims) + 26
    rows = (len(ims) + cols - 1) // cols
    c = Image.new("RGB", (cols * (cellw + 10) + 10, rows * per + 44), "#e8e2d4")
    d = ImageDraw.Draw(c)
    d.text((12, 10), title, fill="#141414")
    for n, im in enumerate(ims):
        r, col = divmod(n, cols)
        x, y = 10 + col * (cellw + 10), 34 + r * per
        c.paste(im, (x, y))
        d.text((x + 2, y + im.height + 6), "page %d" % (n + 1), fill="#4a4438")
    c.save(out)
    print(out.split("\\")[-1], c.size)


fbp = page_of(r"C:\Users\Jloeh\Developer\recruiting-calendar\v3\W20-two-sports\fb-text.txt", "2029 MIKE LB Danny Whitfield")
wbp = page_of(r"C:\Users\Jloeh\Developer\recruiting-calendar\v3\W20-two-sports\wbb-text.txt", "2029 PG Madison Weber")
print("email pages: football", fbp, "girls", wbp)

pair = Image.new("RGB", (2 * 640 + 30, 900 + 36), "#e8e2d4")
d = ImageDraw.Draw(pair)
d.text((12, 10), "The rewritten outreach emails, one page each, left football right girls' basketball", fill="#141414")
for n, (folder, pg) in enumerate((("fb8", fbp), ("wbb8", wbp))):
    pair.paste(thumb(P + "\\" + folder + "\\page_%03d.png" % pg, 640), (10 + n * 650, 32))
pair.save(T + r"\proof-emails-2026-11-11.png")
print("proof-emails-2026-11-11.png", pair.size)

sheet("fb8", 11, 208, T + r"\sheet-football-21pp.png", "Football playbook, 21 pages, rewritten email and the size table")
sheet("wbb8", 10, 208, T + r"\sheet-girls-19pp.png", "girls' basketball playbook, 20 pages, rewritten email and the size floors")
