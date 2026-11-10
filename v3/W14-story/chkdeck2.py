import pathlib,sys,re
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
t=pathlib.Path("site/assets/deck.js").read_text(encoding="utf-8")
print([m for m in re.findall(r"href=\\?'[^']*playbooks[^']*\\?'", t)])
print([m for m in re.findall(r"/playbooks/[^\"']{0,40}", t)][:6])
