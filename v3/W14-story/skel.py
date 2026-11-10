import re,pathlib,sys
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
t=pathlib.Path("site/playbooks/index.html").read_text(encoding="utf-8")
print("len",len(t))
for tag in ["<head>","</head>","<body","<header","</header>","<main","</main>","<footer","</footer>","</body>"]:
    print(f"  {tag:12} at {t.find(tag)}")
print("\n=== one product card, verbatim")
m=re.search(r'<article class="pb\b.*?</article>',t,re.S)
print(m.group(0)[:1400] if m else "(no article.pb)")
print("\n=== head/nav first 700 chars")
print(t[:400])
