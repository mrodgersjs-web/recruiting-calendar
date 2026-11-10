import pathlib,sys,re,collections
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
vals=collections.Counter()
for p in pathlib.Path("site").rglob("*.html"):
    t=p.read_text(encoding="utf-8")
    vals.update(re.findall(r'\?v=([0-9a-f]{6,12})', t))
print("distinct asset versions on disk:", dict(vals))
hits=[str(p) for p in pathlib.Path("v3").rglob("*.py") if "?v=" in p.read_text(encoding="utf-8",errors="ignore")]
print("scripts that write ?v=:", hits[:10])
for s in ["v3/W14-story/build_sports.py","v3/W13-copy/plainfix.py","v3/W13-copy/scrub.py"]:
    if pathlib.Path(s).exists():
        for m in re.finditer(r"[?]?v=.{0,60}", pathlib.Path(s).read_text(encoding="utf-8",errors="ignore")):
            print("  ",s,"->",m.group(0)[:80])
