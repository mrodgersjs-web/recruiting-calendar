import re,pathlib,json
out={}
for p in sorted(pathlib.Path("site/playbooks").glob("*/index.html")):
    h=p.read_text(encoding="utf-8",errors="ignore")
    def g(pat):
        m=re.search(pat,h)
        return re.sub(r"\s+"," ",m.group(1)).strip() if m else None
    out[str(p.parent.name)]={"h1":g(r"(?is)<h1[^>]*>(.*?)</h1>"),"lede":g(r"(?is)<p class=\"lede\"[^>]*>(.*?)</p>"),
        "for":g(r"(?is)<p class=\"for\">(.*?)</p>") or g(r"(?is)For:\s*(.*?)<"),
        "trust":g(r"(?is)<p class=\"note\"[^>]*>(.*?)</p>"),"inside":[x.strip() for x in re.findall(r"(?is)<li>(.*?)</li>",h)][:8]}
print(json.dumps(out,indent=1,ensure_ascii=False)[:3800])
