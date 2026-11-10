import pathlib,sys,re
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
d=sorted(pathlib.Path("site/athlete").iterdir())[0]
t=(d/"index.html").read_text(encoding="utf-8")
print("page:",d)
print("h1:", re.findall(r"<h1[^>]*>(.*?)</h1>", t, re.S)[:1])
print("title:", re.findall(r"<title>([^<]*)</title>", t)[:1])
print("og:title:", re.findall(r'property="og:title" content="([^"]*)"', t)[:1])
i=t.find("Composite"); print(repr(t[max(0,i-120):i+140]))
