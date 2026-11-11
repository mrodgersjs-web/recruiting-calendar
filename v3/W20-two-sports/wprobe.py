import re, sys, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
s = pathlib.Path("wbb-plain.py").read_text(encoding="utf-8")
for pat in [r"[^<>]{0,120}settlement[^<>]{0,200}", r"Subject: [^<]{0,300}", r"ppg[^<>]{0,80}"]:
    ms = list(re.finditer(pat, s, re.I))
    print("== %s -> %d hits" % (pat, len(ms)))
    for m in ms[:4]:
        print("   ", re.sub(r"\s+", " ", m.group(0))[:330], "\n")
