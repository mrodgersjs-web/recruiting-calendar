import re, html, pathlib, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
for n in ("fb-playbook-plain.html", "wbb-playbook-plain.html"):
    t = pathlib.Path(n).read_text(encoding="utf-8")
    print("\n########", n)
    for m in re.finditer(r'<div class="tmpl">(.*?)</div>', t, re.S):
        print("--- EMAIL TEMPLATE ---")
        print(html.unescape(re.sub(r"<br\s*/?>", "\n", m.group(1))).strip())
    for m in re.finditer(r"<h3>(What goes on the one page[^<]*|The one page[^<]*)</h3>(.{0,2200})", t, re.S):
        print("--- ONE PAGE TABLE ---")
        seg = re.sub(r"</t[dr]>", " | ", m.group(2))
        seg = re.sub(r"<[^>]+>", " ", seg)
        print(re.sub(r"\s+", " ", html.unescape(seg)).strip()[:1400])
