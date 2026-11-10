import pathlib,re,sys
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
n=0
for p in pathlib.Path("site").rglob("*.html"):
    t0=t=p.read_text(encoding="utf-8")
    for u in ["/answers/","/library/","/price/","/recruitiq/","/rules/","/sports/","/store/","/playbooks/","/tools/"]:
        t=t.replace(f'href="{u}"', f'href="{u.rstrip("/")}"')
    if t!=t0: p.write_text(t,encoding="utf-8"); n+=1
print("files fixed:",n)
