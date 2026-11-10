import re,sys,pathlib
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
t=pathlib.Path("site/playbooks/index.html").read_text(encoding="utf-8")
for m in re.finditer(r"<article[^>]*data-slug=\"([\w-]+)\"[^>]*>(.{0,1400}?)</article>", t, re.S):
    slug, body = m.group(1), m.group(2)
    title = re.search(r"<h3[^>]*>(.*?)</h3>", body, re.S)
    pages = re.search(r"(\d+)\s*pages", body)
    price = re.search(r"\$(\d+)", body)
    flag = "verified-pending" if "Rules being verified" in body else ("free" if "Free" in body else "")
    print(f"{slug:30} claim={pages.group(1) if pages else '-':>3} price={price.group(1) if price else '-':>4} {flag:17} {re.sub(chr(60)+'[^'+chr(62)+']*'+chr(62),'',title.group(1)).strip() if title else ''}")
