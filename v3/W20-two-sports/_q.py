import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
src = open("readability.py", encoding="utf-8").read()
i = src.index('audit(r"')
open("readability.py", "w", encoding="utf-8").write(src[:i] + "\n")
tx = open("wbb-text.txt", encoding="utf-8").read()
print("--- how each page ends (footer check) ---")
for part in tx.split("===== PAGE ")[1:]:
    n = part.split("\n", 1)[0].strip(" =")
    body = part.split("\n", 1)[1].replace("\r", "").strip()
    tail = body[-70:].replace("\n", " | ")
    print("p%-3s ...%s" % (n, tail))
