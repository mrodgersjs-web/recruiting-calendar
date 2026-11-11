import pathlib, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
for n in ("wbb-sources.html", "fb-sources.html"):
    p = pathlib.Path(n); t = p.read_text(encoding="utf-8")
    t2 = t.replace('<div class="two small">', '<div class="two small flow">', 1)
    print(n, "patched" if t2 != t else "MISSING")
    p.write_text(t2, encoding="utf-8")
