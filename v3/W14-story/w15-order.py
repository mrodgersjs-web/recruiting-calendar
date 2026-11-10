import pathlib,sys,re
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
t=pathlib.Path("site/sports/football/index.html").read_text(encoding="utf-8")
print("section order on a sport page:")
for m in re.finditer(r'<h2[^>]*>(.*?)</h2>', t, re.S):
    print("   ", re.sub(r"\s+"," ",re.sub(r"<[^>]+>","",m.group(1))).strip()[:60])
i=t.find("How this has played out")
print("\nproof block:", re.sub(r"\s+"," ",t[i-90:i+520])[:600])
print("\nhub tagline:")
h=pathlib.Path("site/sports/index.html").read_text(encoding="utf-8")
j=h.find("No story to read first")
print("   ", re.sub(r"\s+"," ",h[j-260:j+80]))
