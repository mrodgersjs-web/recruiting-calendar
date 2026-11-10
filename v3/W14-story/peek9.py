import re,pathlib,sys
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
t=pathlib.Path("v3/W14-story/build_sports.py").read_text(encoding="utf-8")
i=t.find("def store_cards")
print(t[i:i+1000])
print("=== leaks in built pages")
for p in sorted(pathlib.Path("site/sports").rglob("*.html")):
    s=p.read_text(encoding="utf-8")
    print(f"  {p.parent.name:14} mains={s.count('<main')} closes={s.count('</main>')} bundles={'pb-bund' in s} cells={s.count('class=\"pb-cell\"')} h2={len(re.findall('<h2',s))}")
