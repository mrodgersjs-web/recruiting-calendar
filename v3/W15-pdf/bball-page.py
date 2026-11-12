"""House style: what a playbook PDF actually contains, page by page."""
import sys
import pathlib

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p = pathlib.Path(__file__).resolve().parents[2] / "v3/W2-playbooks/eligibility-2-hard-deadlines.pdf"
print("reference file:", p.name, p.stat().st_size, "bytes")
h = pathlib.Path(__file__).resolve().parents[2] / "site/sports/basketball/index.html"
t = h.read_text(encoding="utf-8")
import re
import html as H
body = re.sub(r"(?is)<(script|style|svg|nav|footer|header)[^>]*>.*?</\1>", " ", t)
txt = re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", " ", body))).strip()
print("live basketball page:", len(txt.split()), "words")
print(txt[:900])
