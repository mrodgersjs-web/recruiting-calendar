import pathlib,sys,re
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
src=[p.name for p in sorted(pathlib.Path("site/playbooks").iterdir()) if p.is_dir() and 'id="sources"' in (p/"index.html").read_text(encoding="utf-8",errors="ignore")]
print("playbooks with a sources block:", src)
t=pathlib.Path("site/sports/football/index.html").read_text(encoding="utf-8")
i=t.find('<h2>How this has played out</h2>'); j=t.find('</section>', i)
print("\nproof slice chars:", j-i)
print(re.sub(r"\s+"," ",t[i:j+10])[:820])
e=pathlib.Path("site/emerging-sports/index.html").read_text(encoding="utf-8")
k=e.find('Stories and tools for these sports')
print("\nemerging block:\n", re.sub(r"\s+"," ",e[k-60:k+780]))
