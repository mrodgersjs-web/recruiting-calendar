import json, pathlib
from PIL import Image
ROOT = pathlib.Path(r"C:\Users\Jloeh\Developer\recruiting-calendar")
SITE = ROOT / "site"
T = pathlib.Path(r"C:\Users\Jloeh\.aside\u\1\sessions\2026-11-08_sIbJ63jY5p1sXMzN\tmp")
man = json.loads((SITE / "IMAGES.json").read_text(encoding="utf-8"))
for e in man["images"]:
    f = e["file"][0] if isinstance(e["file"], list) else e["file"]
    if any(k in f for k in ("derrick", "wbasketball", "football")):
        print("=== %s | subject: %s" % (f, e.get("subject")))
        print(e.get("prompt"))
        print("   other keys:", {k: v for k, v in e.items() if k not in ("prompt", "subject", "file")})
        print()
# flattened refs for style
for name in ("cut-wbasketball-640.webp", "cut-football-640.webp"):
    im = Image.open(SITE / "assets/media" / name).convert("RGBA")
    bg = Image.new("RGBA", im.size, (245, 241, 232, 255))
    bg.alpha_composite(im)
    bg.convert("RGB").save(T / ("ref-" + name.replace(".webp", ".png")))
    print("reference written:", "ref-" + name.replace(".webp", ".png"), (T / ("ref-" + name.replace(".webp", ".png"))).stat().st_size)
