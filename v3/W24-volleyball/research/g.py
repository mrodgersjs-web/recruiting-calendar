import pathlib, re, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
keys = ["dead period", "quiet period", "contact period", "evaluation period", "recruiting conversation", "camp", "five official", "official visit", "unofficial"]
for f in ["04-film-and-outreach.md", "06-paperwork-and-the-boys-lane.md"]:
    t = pathlib.Path(f).read_text(encoding="utf-8").split("\n")
    print("#" * 30, f)
    for i, ln in enumerate(t):
        low = ln.lower()
        if any(k in low for k in ["dead period", "quiet period", "contact period", "evaluation period", "recruiting conversation", "official visit"]):
            print("\n".join(t[max(0,i-2):i+4])); print("-" * 60)
