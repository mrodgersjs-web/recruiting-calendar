import pathlib,sys,re
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
n=0
for f in pathlib.Path("site").rglob("*.html"):
    t0=t=f.read_text(encoding="utf-8")
    t=re.sub(r"Composite: \u0022([^\u0022<>]+?)\u0022 \(", lambda m: "Composite: \u201c"+m.group(1)+"\u201d (", t)
    if t!=t0: f.write_text(t,encoding="utf-8"); n+=1
print("html files updated:",n)
