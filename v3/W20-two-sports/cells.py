import re, sys, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
s = pathlib.Path("fb-plain.py").read_text(encoding="utf-8")
for pat in [r'class="d">FBS and FCS[^<]{0,240}', r'class="d">Roster cap[^<]{0,260}', r'class="d">Junior college \(NJCAA\)[^<]{0,200}',
            r'class="d">Combines[^<]{0,220}', r'One look per player.{0,220}', r'ratify it.{0,120}',
            r'small-school[^<]{0,120}', r'per-game[^<]{0,140}', r'one-page sheet[^<]{0,60}',
            r'8\.1%.{0,160}', r'lifted the old cap.{0,200}']:
    ms = list(re.finditer(pat, s, re.I))
    print("== %s -> %d" % (pat, len(ms)))
    for m in ms[:2]:
        print("   ", re.sub(r"\s+", " ", s[m.start():m.end()])[:300])
