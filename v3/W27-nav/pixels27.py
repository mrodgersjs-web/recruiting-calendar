from PIL import Image, ImageStat
import json, pathlib
T = pathlib.Path(r"C:\Users\Jloeh\.aside\u\1\sessions\2026-11-08_sIbJ63jY5p1sXMzN\tmp")
b = json.loads((T / "w27-boxes.json").read_text())
im = Image.open(T / "w27-full.png").convert("RGB")
dpr = im.size[0] / 1440.0
print("full shot", im.size, "dpr", dpr)
def crop(name, y0, y1, w=1150):
    box = (int(b["grid1"]["x"] * dpr) - 20, int(y0 * dpr), int((b["grid1"]["x"] + b["grid1"]["w"]) * dpr) + 20, int(y1 * dpr))
    c = im.crop(box)
    c.resize((w, int(c.size[1] * w / c.size[0])), Image.LANCZOS).save(T / (name + ".png"), optimize=True)
    print(name, c.size)
crop("w27-shot-A", b["h1"]["y"] - 20, b["grid1"]["y"] + b["grid1"]["h"] + 24)
crop("w27-shot-B", b["heads"][2]["y"] - 10, b["grid3"]["y"] + b["grid3"]["h"] + 24)
ph = Image.open(T / "w27-store-390.png").convert("RGB")
ph.resize((430, int(ph.size[1] * 430 / ph.size[0])), Image.LANCZOS).save(T / "w27-shot-C.png", optimize=True)
# pending art vs live art, from the document shot
def bright(x, y, w, h):
    return round(ImageStat.Stat(im.crop(tuple(int(v * dpr) for v in (x, y, x + w, y + h))).convert("L")).mean[0], 1)
g1 = b["grid1"]; g3 = b["grid3"]
cw = g1["w"] / 3
print("live volleyball thumb brightness", bright(g1["x"] + cw, g1["y"], cw, 480))
print("pending baseball thumb brightness", bright(g3["x"], g3["y"], cw, 480))
print("chat files:", [(p.name, round(p.stat().st_size / 1024)) for p in sorted(T.glob("w27-shot-*.png"))])
