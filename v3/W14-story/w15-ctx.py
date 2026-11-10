import pathlib,sys,re,html
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
for f in ["site/playbooks/walk-on/index.html","site/sports/index.html","site/sports/football/index.html",
          "site/emerging-sports/index.html","site/index.html","site/about/index.html"]:
    t=pathlib.Path(f).read_text(encoding="utf-8",errors="ignore")
    body=re.sub(r"(?is)<(script|style|svg)[^>]*>.*?</\1>"," ",t)
    txt=re.sub(r"\s+"," ",re.sub(r"<[^>]+>"," ",body))
    print("###",f)
    for m in list(re.finditer(r"(?i)stor(?:y|ies)|real athlete|Illustration",txt))[:6]:
        print("   ...",txt[max(0,m.start()-70):m.start()+95].strip(),"...")
