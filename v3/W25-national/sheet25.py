# -*- coding: utf-8 -*-
"""Proof images for the national pass: a full contact sheet for the volleyball book, plus one
three-panel proof of the pages that changed most (the roster count, the camp prices, the sample
email). Pages are found by the words on them, not by a hardcoded number."""
import sys, glob, re, pathlib
from PIL import Image, ImageDraw
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

TMP = pathlib.Path(r"C:\Users\Jloeh\.aside\u\1\sessions\2026-11-08_sIbJ63jY5p1sXMzN\tmp")
SHEET = pathlib.Path(r"C:\Users\Jloeh\.aside\u\1\sessions\2026-11-08_sIbJ63jY5p1sXMzN\tmp")


def pages(dirn):
    return sorted(glob.glob(str(TMP / dirn / "page_*.png")))


def find(dirn, needle):
    txt = (TMP / "pb25" / (dirn.split("-")[-1] + "-text.txt")).read_text(encoding="utf-8")
    parts = re.split(r"===== PAGE (\d+) =====", txt)
    for i in range(1, len(parts) - 1, 2):
        if re.sub(r"\s+", "", needle).lower() in re.sub(r"\s+", "", parts[i + 1]).lower():
            return int(parts[i])
    return None


def thumb(path, w):
    im = Image.open(path)
    return im.resize((w, int(w * im.height / im.width)))


# --- contact sheet, 32 pages, 6 across
src = pages("pb25/pages-vb")
cols, tw = 6, 240
rows = -(-len(src) // cols)
pad, lab = 10, 16
sheet = Image.new("RGB", (cols * (tw + pad) + pad, rows * (int(tw * 1.294) + pad + lab) + pad), (24, 22, 20))
d = ImageDraw.Draw(sheet)
for i, f in enumerate(src):
    r, c = divmod(i, cols)
    t = thumb(f, tw)
    x, y = pad + c * (tw + pad), pad + r * (t.height + pad + lab)
    sheet.paste(t, (x, y))
    d.text((x, y + t.height + 3), str(i + 1), fill=(220, 210, 190))
out = SHEET / "sheet-volleyball-32pp.png"
sheet.save(out)
print("contact sheet", sheet.size, "->", out)

# --- three-panel proof of the reworked pages
panels = [("pb25/pages-vb", "Pages counted", "chapter 2: the counted roster sample"),
          ("pb25/pages-vb", "What camps cost", "chapter 5: what camps cost"),
          ("pb25/pages-vb", "Coach Rivera", "chapter 6: the sample email")]
imgs = []
for dirn, needle, caption in panels:
    n = find(dirn, needle)
    if not n:
        print("   !! no page found for", needle)
        continue
    imgs.append((thumb(src[n - 1], 470), caption, n))
w = sum(i.width for i, _, _ in imgs) + 20 * (len(imgs) + 1)
h = max(i.height for i, _, _ in imgs) + 40
proof = Image.new("RGB", (w, h), (24, 22, 20))
dd = ImageDraw.Draw(proof)
x = 10
for im, caption, n in imgs:
    proof.paste(im, (x, 30))
    dd.text((x, 8), "page %d - %s" % (n, caption), fill=(220, 210, 190))
    x += im.width + 10
out2 = SHEET / "proof-national-pages.png"
proof.save(out2)
print("proof", proof.size, "->", out2)
print("panel pages:", [n for _, _, n in imgs])
