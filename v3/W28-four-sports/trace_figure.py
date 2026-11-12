# -*- coding: utf-8 -*-
"""trace_figure.py — how the women's soccer card's stand-in figure is made (W28).

The image model on this account returns 403, so no new athlete can be generated. The card
needed something that reads as a person rather than a missing image, so the alpha channel of
an unused cutout in the W5 archive is traced into solid house ink and cropped to the aspect
of the eleven photographs it sits beside.

It is a silhouette of a real photograph of a different sport, which is why the card's tag
says SILHOUETTE and the caption says it is traced. When the image model is enabled, generate
the figure, save it as cut-womens-soccer-640.webp and -1080, point the config's `art` at it,
and delete the sil- files.

Both outputs are written to the aspect of the other figures: 640 x 1137 and 1080 x 1920,
content bottom-anchored, with 6 per cent headroom above the content box.
"""
import pathlib
import sys

from PIL import Image

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
SRC = pathlib.Path(__file__).resolve().parent.parent / 'W5-athletes' / 'v1media' / 'cut-pirosko-1080.webp'
OUT = pathlib.Path(__file__).resolve().parent.parent.parent / 'site' / 'assets' / 'media'
INK = (17, 17, 17, 255)
HEADROOM = 0.06
ASPECTS = {640: (640, 1137), 1080: (1080, 1920)}

src = Image.open(SRC).convert('RGBA')
alpha = src.split()[3]
box = alpha.getbbox()
fig = Image.new('RGBA', src.size, (0, 0, 0, 0))
fig.paste(Image.new('RGBA', src.size, INK), (0, 0), alpha)
fig = fig.crop(box)
print('source %s  content box %s  ->  %dx%d' % (SRC.name, box, fig.width, fig.height))

for w_out, (W, H) in ASPECTS.items():
    scale = min((H * (1 - HEADROOM)) / fig.height, W / fig.width)
    fw, fh = int(round(fig.width * scale)), int(round(fig.height * scale))
    small = fig.resize((fw, fh), Image.LANCZOS)
    canvas = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    canvas.paste(small, ((W - fw) // 2, H - fh), small)
    name = 'sil-womens-soccer-%d.webp' % w_out
    canvas.save(OUT / name, 'WEBP', quality=90)
    got = Image.open(OUT / name)
    print('  %-34s %dx%d (wanted %dx%d)  %d B' % (name, got.width, got.height, W, H, (OUT / name).stat().st_size))
