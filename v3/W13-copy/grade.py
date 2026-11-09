import re,pathlib,statistics
def syl(w):
    w=re.sub(r"[^a-z]","",w.lower())
    if not w: return 0
    n=len(re.findall(r"[aeiouy]+",w))
    if w.endswith("e") and n>1: n-=1
    return max(1,n)
def fk(t):
    t=re.sub(r"\s+"," ",t)
    s=[x for x in re.split(r"[.!?]+(?=\s|$)",t) if len(x.split())>2]
    w=re.findall(r"[A-Za-z][A-Za-z'\-]*",t)
    if not s or len(w)<40: return None,len(w)
    return round(0.39*(len(w)/len(s))+11.8*(sum(syl(x) for x in w)/len(w))-15.59,1),len(w)
def main_text(html):
    m=re.search(r"(?is)<main[^>]*>(.*?)</main>",html)
    t=m.group(1) if m else re.sub(r"(?is)<header.*?</header>|<footer.*?</footer>"," ",html)
    t=re.sub(r"(?is)<(script|style|svg|noscript)[^>]*>.*?</\1>"," ",t)
    return re.sub(r"\s+"," ",re.sub(r"<[^>]+>"," ",t)).strip()
rows=[]
for p in sorted(pathlib.Path("site").rglob("*.html")):
    g,w=fk(main_text(p.read_text(encoding="utf-8",errors="ignore")))
    if g: rows.append((g,w,str(p).replace("\\","/")))
rows.sort(reverse=True)
print(f"scored pages with >=40 body words: {len(rows)}   median: {statistics.median(r[0] for r in rows):.1f}")
print(f"pages above grade 8.9: {sum(1 for r in rows if r[0]>8.9)}   above 12: {sum(1 for r in rows if r[0]>12)}")
print("\ngrade  words  path")
for g,w,p in rows[:26]: print(f" {g:>5}  {w:>5}  {p}")
