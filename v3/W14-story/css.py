import pathlib,sys,re
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
css={p.name:p.read_text(encoding="utf-8",errors="ignore") for p in pathlib.Path("site/assets").glob("*.css")}
print("css files:",{k:len(v) for k,v in css.items()})
for c in ["btn--primary","btn--ghost","pb-cell","pb-grid","dk-read","dk-pbs","dk-src","svc","cta-band","plans","notice"]:
    hits=[f"{n}:{len(re.findall(re.escape('.'+c),t))}" for n,t in css.items() if re.search(re.escape('.'+c),t)]
    print(f"  {c:14} {hits or 'MISSING'}")
t=css.get("commit.css","")
i=t.find(".pb-grid")
print("\n.pb-grid context:",re.sub(r"\s+"," ",t[i:i+260]) if i>0 else "(none)")
i=t.find(".btn")
print("\n.btn context:",re.sub(r"\s+"," ",t[i:i+300]) if i>0 else "(none)")
