import re,pathlib,sys
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
for f in ["site/story/hunter/index.html","site/story/composite-swim/index.html"]:
    t=pathlib.Path(f).read_text(encoding="utf-8",errors="ignore")
    print("###",f)
    for m in re.finditer(r".{60}(renfrow|2362).{40}",t):
        print("   ...",re.sub(r"\s+"," ",m.group(0)),"...")
    print("   canonical:",re.findall(r'<link rel="canonical"[^>]*>',t)[:1])
    print("   og:url:",re.findall(r'property="og:url"[^>]*',t)[:1])
