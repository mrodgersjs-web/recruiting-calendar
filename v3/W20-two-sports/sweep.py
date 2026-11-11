import re, sys, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BRIT = r"(?i)\b(programme|defence|counsellor|centre|behaviour|organis\w+|recognis\w+|analyse\w*|licence|labour|colour|travelling|judgement|prioritis\w+|realis\w+|utilis\w+|favour\w*|whilst|holiday)\b"
JARG = r"(?i)\b(roster math|bandwidth|leverage|touch base|low-hanging|on the board|equivalenc\w+|permissible|nonqualifier|grassroots|institutional money event|currency|diagnosing|ppg|mlb)\b"
for f in ("wbb-playbook-plain.html", "fb-playbook-plain.html"):
    h = pathlib.Path(f).read_text(encoding="utf-8")
    print("\n===", f)
    print(" british/spelling:", sorted(set(re.findall(BRIT, h))) or "none")
    for t in sorted(set(re.findall(JARG, h))):
        m = re.search(r"(?i)[^<>]{0,110}\b%s\b[^<>]{0,110}" % re.escape(t), h)
        print("  term %-26s -> %s" % (t.lower(), re.sub(r"\s+", " ", m.group(0))[:190]))
