import re, sys, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
for f in ("v3/W19-plain/customer-text.txt", "v3/W20-two-sports/wbb-text.txt"):
    raw = pathlib.Path(f).read_text(encoding="utf-8")
    parts = re.split(r"===== PAGE (\d+) =====", raw)
    print("\n===", f, "pages:", (len(parts) - 1) // 2)
    for i in range(1, len(parts) - 1, 2):
        t = parts[i + 1]
        flat = re.sub(r"\s+", "", t)
        head = "THECOMMITBOOK" in flat
        num = re.search(r"(\d+)/(\d+)$", flat)
        tail = re.sub(r"\s+", " ", t.strip())[-60:]
        print("p%-3s head %s footer %s pgno %s | %s" % (parts[i], "Y" if head else "-",
              "Y" if "EDUCATION,NOTLEGALADVICE" in flat.upper() or "EDUCATION,NOTLEGALADVICE" in flat else "-",
              (num.group(0) if num else "-"), tail))
