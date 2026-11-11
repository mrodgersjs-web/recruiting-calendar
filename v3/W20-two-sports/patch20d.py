import re, sys, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

def flex(t):
    return re.compile(r"\s+".join(re.escape(x) for x in re.split(r"\s+", t.strip())))

WBB = [("at the schools using the new settlement rules (Bylaw 17.2, live since 1 July 2025)",
        "at the schools that signed the NCAA settlement, the 2025 deal that set team-size limits and ended the old letter of intent (Bylaw 17.2, live since 1 July 2025)"),
       ("2029 PG, Geneva Township, 14.2 GPA, 22 ppg",
        "2029 PG, Geneva Township, 14.2 GPA, 22 points a game")]

p = pathlib.Path("wbb-plain.py"); s = p.read_text(encoding="utf-8")
for old, new in WBB:
    m = list(flex(old).finditer(s))
    print("WBB", len(m), "match(es):", old[:60])
    if len(m) == 1:
        s = s[:m[0].start()] + new + s[m[0].end():]
p.write_text(s, encoding="utf-8")

t = pathlib.Path("../W19-plain/bball-plain.py").read_text(encoding="utf-8")
for m in list(re.finditer(r"[^<>]{0,90}settlement[^<>]{0,140}", t, re.I))[:4]:
    print("MENS>", re.sub(r"\s+", " ", m.group(0))[:250])
