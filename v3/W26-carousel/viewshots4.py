from PIL import Image, ImageChops
import json, pathlib
T = pathlib.Path(r"C:\Users\Jloeh\.aside\u\1\sessions\2026-11-08_sIbJ63jY5p1sXMzN\tmp")
g = json.loads((T / "w26b-geo2.json").read_text())
def fig(key):
    im = Image.open(T / ("full-%s.png" % key)).convert("RGB")
    dpr = im.size[0] / 1440.0
    r = g[key]["img"]
    box = tuple(int(v * dpr) for v in (r["x"], r["y"], r["x"] + r["w"], r["y"] + r["h"]))
    return im, dpr, im.crop(box)
def sig(crop):
    px = list(crop.getdata())
    solid = [p for p in px if max(p) < 245]
    def near(c, t, d=45): return all(abs(x - y) <= d for x, y in zip(c, t))
    return {"gold%": round(100*sum(1 for c in solid if near(c, (210,165,45), 45))/len(px), 1),
            "navy%": round(100*sum(1 for c in solid if near(c, (20,30,70), 40) and c[2] > c[0])/len(px), 1),
            "ball_orange%": round(100*sum(1 for c in solid if c[0] > 150 and 40 < c[1] < 130 and c[2] < 80)/len(px), 1),
            "white%": round(100*sum(1 for c in solid if min(c) > 210)/len(px), 1),
            "mean_colour": round(sum(max(p)-min(p) for p in solid)/max(1,len(solid)), 1)}
ims, dprs, crops = {}, {}, {}
for k in ("mbb", "wbb", "vb", "swim"):
    ims[k], dprs[k], crops[k] = fig(k)
    print("%-5s %-20s %s" % (k, g[k]["line"], sig(crops[k])))
a = crops["mbb"]; b = crops["wbb"].resize(crops["mbb"].size)
d = ImageChops.difference(a, b)
print("\nthe two basketball cards differ by mean channel delta %.1f (0 would be the same picture)"
      % (sum(sum(p) for p in d.getdata())/len(d.getdata())/3))
print("the pending card's colour is 0.0 -> greyed: mean colour %.1f" % sig(crops["swim"])["mean_colour"])
# chat crops: the card plus its strip
for k, w in (("mbb", 460), ("wbb", 460), ("vb", 460), ("swim", 520)):
    im = ims[k]; c = g[k]["card"]; dpr = dprs[k]
    box = tuple(int(v * dpr) for v in (c["x"] - 12, max(0, c["y"] - 20), c["x"] + c["w"] + 12, c["y"] + c["h"] + 8))
    cut = im.crop(box)
    cut.resize((w, int(cut.size[1]*w/cut.size[0])), Image.LANCZOS).save(T / ("card-%s.png" % k), optimize=True)
ring = Image.open(T / "full-vb.png").convert("RGB").crop((0, int(60*dprs["vb"]), ims["vb"].size[0], int(900*dprs["vb"])))
ring.resize((1100, int(ring.size[1]*1100/ring.size[0])), Image.LANCZOS).save(T / "card-ring.png", optimize=True)
print("\nchat files:", [(p.name, round(p.stat().st_size/1024)) for p in sorted(T.glob("card-*.png"))])
