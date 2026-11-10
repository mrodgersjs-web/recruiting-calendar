import pathlib,re,sys
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
for p in sorted(pathlib.Path("site/assets").glob("*.js"))+[pathlib.Path("site/index.html")]:
    t=p.read_text(encoding="utf-8",errors="ignore")
    for m in re.finditer(r"dk-read",t):
        s=max(0,m.start()-200); print(f"--- {p} @{m.start()}")
        print("   ",repr(t[s:m.start()+160]))
