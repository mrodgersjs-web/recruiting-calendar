import json, re, sys, pathlib, urllib.request

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BASE = "http://127.0.0.1:8791"

for u in ["/sports/", "/sports/football/", "/sports/baseball/", "/sports/track-field/",
          "/sports/lacrosse/", "/sports/swimming/", "/sports/basketball/", "/story/hunter/",
          "/athlete/hunter/", "/playbooks/", "/"]:
    try:
        raw = urllib.request.urlopen(BASE + u, timeout=10).read().decode("utf-8", "ignore")
    except Exception as e:
        print(f"  {u:22} FAIL {e}")
        continue
    flags = []
    if re.search(r"\{[a-z_]", raw):
        flags.append("unrendered-brace")
    if ">None<" in raw or "TODO" in raw or "FIXME" in raw:
        flags.append("placeholder")
    if "/story/" not in raw and u.startswith("/sports/") and u != "/sports/":
        flags.append("no-proof-link")
    print(f"  {u:22} 200  len={len(raw):6,}  cells={raw.count('class=\"pb-cell\"'):2}  "
          f"rules={'/rules/' in raw}  story={'/story/' in raw}  {' '.join(flags)}")

js = pathlib.Path("site/assets/deck.js").read_text(encoding="utf-8")
i = js.find("dk-read")
print("\ndeck CTA now:", re.sub(r"\s+", " ", js[i - 60:i + 320]))
ring = pathlib.Path("site/assets/ring.js").read_text(encoding="utf-8")
print("\nring still links to /story/ anywhere:", bool(re.search(r"location\.href='/story/", ring)))
hub = pathlib.Path("site/sports/index.html").read_text(encoding="utf-8")
print("hub tiles:", len(re.findall(r'class="pb-cell"', hub)))
foot = pathlib.Path("site/sports/football/index.html").read_text(encoding="utf-8")
print("football page: nav label 'By sport' present:", "By sport" in foot,
      "| canonical:", re.search(r'rel="canonical" href="([^"]+)"', foot).group(1))
