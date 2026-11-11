import pathlib, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
want = {
 "03-club-season-and-events.md": ["camp", "94", "96", "invite"],
 "04-film-and-outreach.md": ["camp", "invite", "August 1", "Aug. 1"],
 "06-paperwork-and-the-boys-lane.md": ["age", "guarantee", "five-year", "5-year", "agreement", "settlement", "NJCAA", "NAIA", "Division 3"],
}
for f, keys in want.items():
    t = pathlib.Path(f).read_text(encoding="utf-8").split("\n")
    print("#" * 24, f)
    seen = set()
    for i, ln in enumerate(t):
        low = ln.lower()
        if any(k.lower() in low for k in keys) and i not in seen:
            seen.add(i)
            print(ln.strip()[:400]); print("-" * 40)
