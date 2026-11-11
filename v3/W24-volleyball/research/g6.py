import pathlib, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
t = pathlib.Path("04-film-and-outreach.md").read_text(encoding="utf-8").split("\n")
for ln in t:
    low = ln.lower()
    if any(k in low for k in ["reel", "minutes", "second", "clip", "login", "youtube", "otto", "university athlete", "hudl", "balltime", "perfect", "2.2", "reception error", "46", "23.7", "reply", "respond"]):
        print(ln.strip()[:300]); print("-" * 26)
