import json, re, sys, pathlib, urllib.request

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

home = urllib.request.urlopen("https://recruiting-calendar.vercel.app/", timeout=20).read().decode("utf-8", "ignore")
print("PRODUCTION has /sports nav:", "/sports" in home, "| By sport:", "By sport" in home)
for u in ["/sports/", "/sports/football/", "/sports/basketball/"]:
    try:
        r = urllib.request.urlopen("https://recruiting-calendar.vercel.app" + u, timeout=20)
        print(f"  {u:22} {r.status}  {len(r.read()):,} bytes")
    except Exception as e:
        print(f"  {u:22} FAIL {e}")

print("\n== what a real bio actually contains (structure worth preserving)")
js = pathlib.Path("site/assets/stories.js").read_text(encoding="utf-8")
data = json.JSONDecoder().raw_decode(js[js.index("{"):])[0]
real = [a for a in data["athletes"] if not a.get("composite")]
comp = [a for a in data["athletes"] if a.get("composite")]
print(f"   real={len(real)}  composite={len(comp)}")
a = real[0]
for k, v in sorted(a.items()):
    s = json.dumps(v) if not isinstance(v, str) else v
    print(f"   {k:12} {str(s)[:150]}")

print("\n== citation links on that bio page")
p = pathlib.Path("site") / "story" / a["id"] / "index.html"
t = p.read_text(encoding="utf-8")
ext = re.findall(r'<a[^>]+href="(https?://[^"]+)"[^>]*>(.{0,60}?)</a>', t, re.S)
print(f"   {len(ext)} external links, first 6:")
for h, label in ext[:6]:
    print(f"     {re.sub(chr(60)+'[^>]+'+chr(62), ' ', label).strip()[:36]:38} {h[:96]}")

print("\n== does vercel.json already exist?")
vj = pathlib.Path("site/vercel.json")
if vj.exists():
    print(vj.read_text(encoding="utf-8")[:600])
else:
    for cand in ["vercel.json", "site/_redirects", "site/netlify.toml"]:
        f = pathlib.Path(cand)
        print(f"   {cand}: exists={f.exists()}", f.read_text(encoding='utf-8')[:200] if f.exists() else "")
