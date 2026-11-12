import re,sys,pathlib,html
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
for y in ("2027","2028","2029","2030"):
    p=pathlib.Path(f"site/rules/football/{y}/index.html"); t=p.read_text(encoding="utf-8")
    body=re.sub(r"(?is)<(script|style|svg)[^>]*>.*?</\1>"," ",t)
    txt=html.unescape(re.sub(r"<[^>]+>"," ",body)); txt=re.sub(r"\s+"," ",txt)
    dates=len(re.findall(r"(?m)\b(?:Aug|Sep|Oct|Nov|Dec|Jan|Feb|Mar|Apr|May|Jun|Jul)\b",txt))
    print(f"football/{y}: {len(txt.split())} words, month mentions {dates}, class-year mentions {len(re.findall(y,txt))}")
p=pathlib.Path("site/rules/football/2027/index.html").read_text(encoding="utf-8")
i=p.find("<h1"); print("\n2027 page, first 400 visible chars:")
print(re.sub(r"\s+"," ",html.unescape(re.sub(r"<[^>]+>"," ",p[i:i+900]))) [:420])
