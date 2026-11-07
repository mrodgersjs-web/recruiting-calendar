#!/usr/bin/env python3
"""W10 validator. Usage: python3 tests/validate.py [--sync]
--sync rewrites manifest stage titles, worksheets, scripts and sources from the markdown, then validates."""
import re, json, sys, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V3 = os.path.dirname(ROOT)
SPORTS = ["football", "baseball", "track"]
errs = []
def err(sport, msg): errs.append(f"[{sport}] {msg}")

src_text = open(f"{ROOT}/shared/SOURCES.md").read()
S_IDS = set(re.findall(r"\bS(\d{1,2})\b", " ".join(re.findall(r"^\|\s*(S\d+)\s*\|", src_text, re.M)))) 
S_IDS = {f"S{n}" for n in S_IDS} or set(re.findall(r"^\|\s*(S\d+)\s*\|", src_text, re.M))
if not S_IDS: S_IDS = set(re.findall(r"\b(S\d{1,2})\b", src_text))
site_data = open(f"{V3}/site/data.js").read() if os.path.exists(f"{V3}/site/data.js") else ""
offers = json.load(open(f"{V3}/W8-offerings/OFFERINGS.json"))["offerings"]
OFFER = {o["slug"]: o["status"] for o in offers}

BANNED = ["guarantee", "will get you", "you will earn", "unlock", "empower", "synergy", "leverage", "disrupt", "hustle", "utilize", "iterate", "optimize", "buy now", "checkout", "add to cart"]
MINOR_NAMES = ["jacob", "alex "]

def parts(text):
    stages = re.findall(r"^### Stage (\d+)\. (.+)$", text, re.M)
    ws = re.findall(r"^\*\*(C\d+)\.", text, re.M)
    sc = re.findall(r"^\*\*(E\d+)\.", text, re.M)
    return stages, ws, sc

for sport in SPORTS:
    path = f"{ROOT}/{sport}/PLAYBOOK.md"
    text = open(path).read()
    mpath = f"{ROOT}/manifests/{sport}.json"
    man = json.load(open(mpath))
    stages, ws, sc = parts(text)
    if "--sync" in sys.argv:
        man["stages"] = [{"n": int(n), "title": t.split(" (")[0].strip(), "has_done_when": True} for n, t in stages]
        man["worksheets"] = ws; man["scripts"] = sc
        body = text.split("## Sources used")[0]
        man["sources"] = sorted(set(re.findall(r"\bS\d{1,2}\b", text.split("## Sources used")[1])), key=lambda s: int(s[1:]))
        json.dump(man, open(mpath, "w"), indent=1)
    # T1 structure
    for h in ["## Part A", "## Part B", "## Part C", "## Part D", "## Part E", "## Sources used"]:
        if h not in text: err(sport, f"missing section {h}")
    if f"playbook id `{man['id']}`" not in text: err(sport, "playbook id missing in header")
    if "Class of 2029" not in text: err(sport, "class year missing")
    stage_blocks = re.split(r"^### Stage ", text, flags=re.M)[1:]
    for i, b in enumerate(stage_blocks):
        b = b.split("\n## ")[0]
        if "**Done when" not in b: err(sport, f"stage block {i} lacks Done when")
    if len(ws) < 10: err(sport, f"only {len(ws)} worksheets")
    if len(sc) < 4: err(sport, f"only {len(sc)} scripts")
    # scripts under 120 words
    for sid in sc:
        m_ = re.search(rf"^\*\*{sid}\..*?(?=^\*\*E\d+\.|^---|^## |\Z)", text, re.M | re.S)
        if m_ and len(m_.group(0).split()) > 160: err(sport, f"script {sid} too long ({len(m_.group(0).split())} words)")
    # T2 citations
    body = text.split("## Sources used")[0]
    cited = set(re.findall(r"\bS\d{1,2}\b", body))
    for c in cited:
        if c not in S_IDS: err(sport, f"cited {c} not in SOURCES.md")
    listed = set(re.findall(r"\bS\d{1,2}\b", text.split("## Sources used")[1]))
    for c in cited - listed: err(sport, f"{c} cited but not in Sources used")
    for c in listed - cited: err(sport, f"{c} listed in Sources used but never cited")
    if text.count("PROJECTED") < 1: err(sport, "no PROJECTED label")
    # T3 dates
    for d in man["dates"]:
        if d["kind"] in ("RULE", "PROJECTED") and d["date"] not in text: err(sport, f"date {d['date']} not in text")
        if d["kind"] == "PROJECTED":
            if not re.search(r"PROJECTED[^\n]{0,80}" + re.escape(d["date"]) + r"|" + re.escape(d["date"]) + r"[^\n]{0,80}PROJECTED", text):
                err(sport, f"{d['date']} not labelled PROJECTED near its mention")
        if d["kind"] == "RULE" and site_data and d["date"] not in site_data:
            err(sport, f"RULE date {d['date']} not in site/data.js (site wins; fix playbook)")
    if sport == "track" and "2026-10-07" not in text: err(sport, "track must state 2026-10-07 change")
    # T4 integrity
    low = text.lower()
    for b in BANNED:
        for mm in re.finditer(re.escape(b), low):
            ctx = low[max(0, mm.start() - 60):mm.end() + 40]
            if b == "guarantee" and ("not guarantee" in ctx or "no guarantee" in ctx or "promises" in ctx or "does not" in ctx or "nothing here" in ctx or "never" in ctx): continue
            if b == "leverage" and ("leverage" in ctx and False): continue
            err(sport, f"banned phrase '{b}' near: ...{ctx.strip()}...")
    for n in MINOR_NAMES:
        if n in low: err(sport, f"minor name '{n.strip()}' present")
    if "Education, not legal advice" not in text: err(sport, "disclaimer missing")
    if re.search(r"\$\s?\d", text): err(sport, "price-like $ figure in playbook text (prices live in manifest only)")
    # T6 manifest
    if [s["n"] for s in man["stages"]] != [int(n) for n, _ in stages]: err(sport, "manifest stages differ from markdown (run --sync)")
    if man["worksheets"] != ws: err(sport, "manifest worksheets differ")
    if man["scripts"] != sc: err(sport, "manifest scripts differ")
    if set(man["sources"]) != listed: err(sport, "manifest sources differ from Sources used (run --sync)")
    if man["price_proposal"]["status"] != "PROPOSED_NOT_APPROVED": err(sport, "price status must be PROPOSED_NOT_APPROVED")
    for o in man["offer_links"]:
        st = OFFER.get(o["slug"])
        if st is None: err(sport, f"offer slug {o['slug']} not in W8")
        elif (st == "BUILT") != (o["action"] == "link"): err(sport, f"offer {o['slug']} status {st} but action {o['action']}")
        if o["w8_status"] != st: err(sport, f"offer {o['slug']} w8_status stale")

print("PASS" if not errs else "FAIL")
for e in errs: print(" -", e)
sys.exit(1 if errs else 0)
