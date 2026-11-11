from PIL import Image
import json, pathlib
T = pathlib.Path(r"C:\Users\Jloeh\.aside\u\1\sessions\2026-11-08_sIbJ63jY5p1sXMzN\tmp")
g = json.loads((T / "w26-geom2.json").read_text())
c = g["live"]["card"]
def stats(name, x, y, w, h):
    im = Image.open(T / (name + ".png")).convert("RGB")
    dpr = im.size[0] / 1424.0
    px = list(im.crop(tuple(int(v * dpr) for v in (x, y, x + w, y + h))).get_flattened_data()) if hasattr(im, "get_flattened_data") else list(im.crop(tuple(int(v * dpr) for v in (x, y, x + w, y + h))).getdata())
    sat = [max(p) - min(p) for p in px]
    return (round(sum(sat) / len(sat), 1),
            round(100 * sum(1 for p in px if min(p) > 235) / len(px), 1),
            round(100 * sum(1 for p in px if max(p) < 70) / len(px), 1))
X, Y, W, H = c["x"], c["y"], c["w"], c["h"]
print("region = mean_colour_saturation, %white, %near-black")
for label, box in (("athlete art, above the stamp", (X + W * .15, Y + H * .05, W * .7, H * .28)),
                   ("the strip across the athlete", (X - W * .05, Y + H * .33, W * 1.1, H * .20)),
                   ("name and sport line", (X + W * .05, Y + H * .78, W * .6, H * .14))):
    a = stats("w26-proof-live", *box); b = stats("w26-proof-pending", *box)
    print("  %-30s live %s   pending %s" % (label, a, b))
for nm in ("w26-proof-live", "w26-proof-pending"):
    im = Image.open(T / (nm + ".png")).convert("RGB")
    im.resize((1100, int(im.size[1] * 1100 / im.size[0])), Image.LANCZOS).save(T / (nm + "-small.png"), optimize=True)
print("chat-size files:", [(p.name, round(p.stat().st_size / 1024) , 'KB') for p in sorted(T.glob('w26-proof-*-small.png'))])
