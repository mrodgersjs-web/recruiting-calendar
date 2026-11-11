import re, sys, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
CLA = " Keep the body near 180 words, which is what fits one phone screen. The sample below is 182."
jobs = {
 "fb-plain.py":  [("then it stops.</p>", "then it stops." + CLA + "</p>")],
 "wbb-plain.py": [("without a reply, then\n  stop.", "without a reply, then\n  stop." + CLA)],
}
for f, pairs in jobs.items():
    p = pathlib.Path(f); t = p.read_text(encoding="utf-8")
    for a, b in pairs:
        t, n = re.subn(re.escape(a), b.replace("\\n","\n"), t, count=1)
        print(f, "->", n)
    p.write_text(t, encoding="utf-8")
u = pathlib.Path("../W19-plain/bball-plain.py").read_text(encoding="utf-8")
i = u.find("Stay near 70 letters")
print("MENS PARA:", re.sub(r"\s+"," ", u[max(0,i-320):i+520]))
