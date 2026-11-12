import re,sys,pathlib
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
t=pathlib.Path("site/index.html").read_text(encoding="utf-8")
for m in re.finditer(r'(?i)(<svg.{0,400}?</svg>|class="[^"]*brand[^"]*"[^>]*>.{0,200}|<link rel="icon"[^>]*>|<meta property="og:image"[^>]*>)', t, re.S):
    print(re.sub(r"\s+"," ",m.group(0))[:260]); print("  --")
css=pathlib.Path("site/assets/commit.css")
if css.exists():
    c=css.read_text(encoding="utf-8")
    for m in re.finditer(r"(?i)\.?[a-z-]*(brand|logo|mast)[a-z-]*\s*\{[^}]{0,240}\}", c):
        print(re.sub(r"\s+"," ",m.group(0))[:260]); print("  --")
