import re, sys, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
for f in ("wbb-text.txt", "fb-text.txt"):
    raw = pathlib.Path(f).read_text(encoding="utf-8")
    parts = re.split(r"===== PAGE (\d+) =====", raw)
    tot = (len(parts) - 1) // 2
    print("\n=== %s: %d pages ===" % (f, tot))
    miss = []
    for i in range(1, len(parts) - 1, 2):
        t = parts[i + 1]; flat = re.sub(r"\s+", "", t)
        head = "THECOMMITBOOK" in flat
        foot = "EDUCATION,NOTLEGALADVICE" in flat
        num = re.search(r"(\d+)/(\d+)$", flat)
        ok = head and foot and num and num.group(1) == parts[i] and int(num.group(2)) == tot
        if not ok: miss.append((parts[i], head, foot, num.group(0) if num else None))
        body = re.sub(r"\s+", " ", t.strip())
        print("p%-3s %5d ch  head %s foot %s pg %s" % (parts[i], len(body), "Y" if head else "n", "Y" if foot else "n", num.group(0) if num else "-"))
    print("pages failing the check:", miss if miss else "none")
