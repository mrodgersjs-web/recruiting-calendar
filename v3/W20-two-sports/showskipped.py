import sys, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
keys = ["FBS AND FCS", "ROSTER CAP", "walk\ufffeon", "JUNIOR COLLEGE (NJCAA)", "all in one 15-day", "the NAIA and junior college", "July 2027", "One look per player", "COMBINES", "one\ufffepage sheet"]
for line in pathlib.Path("fb-fixes.txt").read_text(encoding="utf-8").splitlines():
    if "|||" not in line: continue
    f, r = line.split("|||", 1)
    if any(k in f for k in keys):
        print("FIND:", f.replace("\ufffe", "[X]"))
        print("REPL:", r.replace("\ufffe", "[X]"), "\n")
