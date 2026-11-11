import re, sys, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
for f in ("02-measurables-by-position.md","04-film-and-outreach.md","05-costs-and-value.md","06-paperwork-and-the-boys-lane.md"):
    print("\n##### " + f)
    for n, line in enumerate(pathlib.Path(f).read_text(encoding="utf-8").split("\n"), 1):
        if line.startswith("#"):
            print("%4d  %s" % (n, line.strip()))
