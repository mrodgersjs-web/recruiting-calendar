import re,pathlib,sys
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
pat=re.compile(r"Not affiliated with or endorsed by [^<]{0,140}?(?:program|school|team|club|rankings|league)[^<]{0,40}?\.")
n=0
for p in pathlib.Path("site").rglob("*.html"):
    t=p.read_text(encoding="utf-8",errors="ignore")
    m=pat.search(t)
    if m and m.group(0)!="Not affiliated with or endorsed by the athlete or any program in this story.":
        t=t[:m.start()]+"Not affiliated with or endorsed by the athlete or any program in this story."+t[m.end():]
        p.write_text(t,encoding="utf-8"); n+=1
print("disclaimers normalized:",n)
