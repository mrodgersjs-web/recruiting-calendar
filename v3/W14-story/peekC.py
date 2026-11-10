import pathlib,sys,re
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
subs=[("what Derrick&#x27;s family did in basketball","what a basketball family in the same spot did"),
      ("Like Derrick&#x27;s family in basketball, ","Like a family in the same spot, "),
      ("Maya&#x27;s","Maya&#x27;s")]
n=0
for f in pathlib.Path("site").rglob("*.html"):
    t0=t=f.read_text(encoding="utf-8"); 
    for a,b in subs[:2]: t=t.replace(a,b)
    if t!=t0: f.write_text(t,encoding="utf-8"); n+=1
print("edited",n)
for f in pathlib.Path("site").rglob("*.html"):
    t=f.read_text(encoding="utf-8")
    for m in re.finditer(r"(?i)derrick",t):
        print(f, "->", repr(t[max(0,m.start()-60):m.start()+60]))
