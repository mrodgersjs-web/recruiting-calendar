import re, sys, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
for f in ("fb-plain.py","wbb-plain.py"):
    t = pathlib.Path(f).read_text(encoding="utf-8")
    m = re.search(r'<div class="tmpl">(.*?)</div>', t, re.S)
    body = m.group(1)
    subj, rest = body.split("\n", 1)
    sig = rest.rsplit("Are you the coach", 1)
    words = len(re.findall(r"[A-Za-z0-9'%.]+", rest.split("Thank you for your time")[0]))
    print(f, "| subject letters:", len(re.sub(r"\s+", " ", subj).strip()), "| body words:", words)
    print("   ", re.sub(r"\s+", " ", subj).strip())
