import re,sys,pathlib,html as H
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
t=pathlib.Path("site/sports/basketball/index.html").read_text(encoding="utf-8")
body=re.sub(r"(?is)<(script|style|svg|nav|footer|header)[^>]*>.*?</\1>"," ",t)
txt=re.sub(r"\s+"," ",H.unescape(re.sub(r"<[^>]+>"," ",body))).strip()
print(txt[880:2600])
