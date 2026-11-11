import re, sys, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
t = pathlib.Path("05-costs-and-value.md").read_text(encoding="utf-8").split("\n")
keep = []
for n, line in enumerate(t, 1):
    if line.startswith("#"):
        keep.append("%4d %s" % (n, line.strip()))
    elif re.search(r"\$\d", line):
        s = re.sub(r"\s+", " ", line)
        s = re.sub(r"https?://\S+", "", s)
        keep.append("%4d   %s" % (n, s[:230]))
print("\n".join(keep))
