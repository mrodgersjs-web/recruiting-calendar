import re, sys, pathlib
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

html = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8", errors="ignore")
m = re.search(r"(?is)<main[^>]*>(.*?)</main>", html)
t = m.group(1) if m else html
t = re.sub(r"(?is)<(script|style|svg|noscript)[^>]*>.*?</\1>", " ", t)
# show structure, not just a blob: headings get markers
t = re.sub(r"(?is)<h1[^>]*>", "\n# ", t)
t = re.sub(r"(?is)<h2[^>]*>", "\n## ", t)
t = re.sub(r"(?is)<h3[^>]*>", "\n### ", t)
t = re.sub(r"(?is)<(li|p|div|tr|section)[^>]*>", "\n", t)
t = re.sub(r"<[^>]+>", " | ", t)
t = re.sub(r"[ \t]+", " ", t)
t = re.sub(r"\n\s*\|(\s*\|)+", "\n", t)
t = re.sub(r"\n{2,}", "\n", t)
print(t.strip()[: int(sys.argv[2]) if len(sys.argv) > 2 else 2600])
