import pathlib,sys,re,html
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
t=pathlib.Path("site/athlete/composite-swingman/index.html").read_text(encoding="utf-8")
for m in list(re.finditer(r"Composite",t))[:3]:
    print(repr(t[max(0,m.start()-90):m.start()+120]))
print("h1:", re.findall(r"<h1[^>]*>(.*?)</h1>", t, re.S)[:1])
print("og:title:", re.findall(r'property="og:title" content="([^"]*)"', t)[:1])
print("title:", re.findall(r"<title>([^<]*)</title>", t)[:1])
