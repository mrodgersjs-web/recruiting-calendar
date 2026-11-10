import pathlib,sys,re
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
t=pathlib.Path("site/assets/deck.js").read_text(encoding="utf-8")
i=t.find("host.innerHTML")
print("assembly:\n", re.sub(r"\s+"," ",t[i:i+420]))
print("\nnode syntax check:")
