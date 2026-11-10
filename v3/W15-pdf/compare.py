import re,sys,pathlib,html
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
PDFC={"football-junior-year":6,"eligibility-2-hard-deadlines":5,"baseball-showcase-to-signing":5,"track-field-marks":5,
"d3-academic-aid-first":4,"walk-on":4,"juco-to-d1":4,"late-bloomer":4,"highlight-reel-social":4,"camp-roi":4,
"nil-high-school":4,"offer-and-signing":4}
for d in sorted(pathlib.Path("site/playbooks").glob("*/index.html")):
    t=d.read_text(encoding="utf-8")
    body=re.sub(r"(?is)<(script|style|svg|nav|footer|header)[^>]*>.*?</\1>"," ",t)
    txt=html.unescape(re.sub(r"<[^>]+>"," ",body))
    txt=re.sub(r"\s+"," ",txt).strip()
    words=len(txt.split())
    slug=d.parent.name
    print(f"{slug:30} page words {words:5}   pdf pages {PDFC.get(slug,'?')}")
