import pathlib,sys,re
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
SITE=pathlib.Path("site")
rows=[]
for p in sorted(SITE.rglob("*.html")):
    t=p.read_text(encoding="utf-8",errors="ignore")
    body=re.sub(r"(?is)<(script|style|svg)[^>]*>.*?</\1>"," ",t)
    txt=re.sub(r"\s+"," ",re.sub(r"<[^>]+>"," ",body))
    n_story=len(re.findall(r"(?i)stor(?:y|ies)",txt))
    n_school=len(re.findall(r"(?i)high school|junior college|juco",txt))
    n_real=len(re.findall(r"(?i)real athlete",txt))
    if n_story or n_real:
        rows.append((n_story+n_real, n_story, n_school, n_real, str(p.relative_to(SITE))))
rows.sort(reverse=True)
print(f"{'sum':>4} {'story':>5} {'school':>6} {'real':>4}  page")
for r in rows[:26]:
    print(f"{r[0]:>4} {r[1]:>5} {r[2]:>6} {r[3]:>4}  {r[4]}")
print("... total pages with story/real mentions:", len(rows))
