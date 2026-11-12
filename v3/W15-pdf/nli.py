import re,sys,pathlib
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
pat=re.compile(r"(?i)letter of intent|\bNLI\b|national letter")
print("=== pages that still talk about the NLI")
for p in sorted(pathlib.Path("site").rglob("*.html")):
    t=p.read_text(encoding="utf-8",errors="ignore")
    for m in pat.finditer(t):
        ctx=re.sub(r"\s+"," ",re.sub(r"<[^>]+>"," ",t[max(0,m.start()-160):m.start()+140]))
        print(f"  {str(p.relative_to('site')):38} {ctx[:170]}")
print("=== '24 pages' style claims and division claims on the basketball page")
t=pathlib.Path("site/sports/basketball/index.html").read_text(encoding="utf-8")
for m in re.finditer(r"(?i)(juco|njcaa|naia|division|d[123]|roster math)", t):
    ctx=re.sub(r"\s+"," ",re.sub(r"<[^>]+>"," ",t[max(0,m.start()-90):m.start()+90]))
    print("   ", ctx[:150])
