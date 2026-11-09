#!/usr/bin/env python3
"""W13-copy: anonymize athletes and schools on the deployed surface, and in the
generator inputs that regenerate it. Deterministic and idempotent.

Why both: site/ is what ships, but build_pages.py and the W9/W2 inputs rewrite
those files, so an HTML-only scrub would be undone on the next build.

The real-name map lives in NAME-MAP.local.md, kept out of git on purpose: a
committed map would re-link each generic first name to a real athlete.

Run:  python v3/W13-copy/scrub.py [--dry]
"""
import json, re, shutil, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
DRY = "--dry" in sys.argv

DEPLOYED = ["site"]
GENERATORS = [
    "v3/W9-experiences/INPUT.json", "v3/W9-experiences/IMAGES.json",
    "v3/W9-experiences/build_pages.py",
    "v3/W1-stories/STORIES.json", "v3/W1-stories/STORIES.md",
    "v3/W2-site/data.json", "v3/W2-site/data_build.py",
    "v3/W2-seo/head-tags.json", "v3/W2-seo/jsonld/stories-articles.json",
    "v3/W2-scripts/SCRIPTS.json", "v3/W2-scripts/SCRIPTS.md",
    "v3/W2-video/manifest.json", "v3/W3-factcheck/CLAIMS.csv",
    "v3/W4-composites/make.py", "site/IMAGES.json", "site/sitemap.xml", "site/data.js",
]
EXTS = {".html", ".js", ".json", ".md", ".py", ".txt", ".xml", ".css", ".csv", ".sh"}

# surname -> (shown first name, new url slug)
PEOPLE = {
    "Butler": ("Jimmy", "jimmy"), "Coward": ("Cedric", "cedric"),
    "Groenewegen": ("Sara", "sara"), "Lowe": ("Karsta", "karsta"),
    "Marpet": ("Ali", "ali"), "Perez": ("Tori", "tori"),
    "Pichardo": ("Olivia", "olivia"), "Pirosko": ("Samantha", "samantha"),
    "Renfrow": ("Hunter", "hunter"), "Rodriguez": ("Cristelle", "cristelle"),
    "Rodenfels": ("Annie", "annie"), "White": ("Derrick", "derrick"),
    "Wondolowski": ("Chris", "chris"),
}
FIRST_FULL = {
    "Jimmy Butler": "Jimmy", "Cedric Coward": "Cedric", "Sara Groenewegen": "Sara",
    "Karsta Lowe": "Karsta", "Ali Marpet": "Ali", "Tori Perez": "Tori",
    "Olivia Pichardo": "Olivia", "Samantha Pirosko": "Samantha", "Hunter Renfrow": "Hunter",
    "Cristelle Rodriguez": "Cristelle", "Annie Rodenfels": "Annie", "Derrick White": "Derrick",
    "Chris Wondolowski": "Chris",
}
# Coaches and staff become roles, never names.
COACH = {
    "Minnesota coach Jessica Allister": "the D1 head coach",
    "coach Jessica Allister": "the head coach", "Jessica Allister": "the head coach",
    "Assistant Piper Ritter": "an assistant coach", "Piper Ritter": "an assistant coach",
    "then-coach Jim Brunelli": "then the head coach", "Jim Brunelli": "the head coach",
    "HS coach Paul Force": "his high school coach", "Paul Force": "his high school coach",
    "under Dana Vote": "under a new head coach", "Dana Vote": "the new head coach",
    "coach Lisa Owens": "her coach", "Lisa Owens": "her coach",
    "Buzz Williams first signee": "the first signee of a new head coach",
    "Buzz Williams": "a new head coach",
    "Culver: White was first recruit he brought for a camp":
        "a JUCO coach said Derrick was the first recruit he brought to a camp",
}
SCHOOL = {
    "Tyler JC then Marquette": "a JUCO program, then a D1 school",
    "Tyler JC": "a JUCO program", "Marquette": "a D1 school",
    "Clemson": "a Power 4 program", "Appalachian State": "a D1 program that offered aid",
    "vs Alabama": "against the top-ranked team", "Alabama": "the top-ranked team",
    "Tampa Bay": "an NFL team",
    "Willamette (D3) then Eastern Washington and Washington State":
        "a D3 school, then two D1 transfers",
    "Willamette": "a D3 school", "Eastern Washington": "a D1 school",
    "Washington State": "another D1 school",
    "UCLA top performers": "one of the best players on the roster",
    "walk on at UCLA": "walk on at a D1 program", "UCLA": "a D1 program",
    "Hobart": "a D3 program",
    "FCS interest (Fordham, Marist, Holy Cross)": "FCS interest",
    "Oglethorpe": "a D3 program", "Brown varsity": "the varsity roster",
    "Brown": "a D1 program", "Gannon": "a D2 program",
    "Doane University (NE)": "an NAIA program", "Doane": "an NAIA program",
    "Centre College": "a D3 program", "Centre": "a D3 program",
    "UCCS then Colorado": "a D2 school, then a D1 transfer",
    "UCCS": "a D2 school", "Colorado": "a D1 school",
    "Chico State": "a D2 program", "a junior college in Wyoming": "a JUCO program in another state",
    "Rutgers": "a D1 program", "Princeton": "an Ivy League D1 program",
    "Eastern Michigan": "a mid-major D1 program", "Oral Roberts": "a mid-major D1 program",
    "Socastee HS, Myrtle Beach, SC": "a suburban high school in South Carolina",
    "quarterback at Socastee": "quarterback at a suburban high school",
    "Socastee": "a suburban high school",
    "Tomball HS, Tomball, TX": "a large suburban high school in Texas",
    "Tomball HS": "a large suburban high school", "Tomball": "a large suburban high school",
    "Legend HS, Parker, CO (first graduating class)":
        "a suburban high school in Colorado, in its first graduating class",
    "Legend HS": "a new suburban high school",
    "De La Salle HS, Danville, CA": "a perennial powerhouse high school in Northern California",
    "De La Salle HS": "a perennial powerhouse high school",
    "De La Salle": "a perennial powerhouse high school",
    "La Costa Canyon HS, Carlsbad, CA": "a large high school in Southern California",
    "La Costa Canyon HS": "a large high school", "La Costa Canyon": "a large high school",
    "Hastings High School, Hastings-on-Hudson, NY": "a suburban high school in New York",
    "Hastings High School": "a suburban high school",
    "Hastings-on-Hudson": "in New York", "Hastings": "a suburban high school",
    "Eastlake North HS, Eastlake, OH": "a suburban high school in Ohio",
    "Eastlake North HS": "a suburban high school", "Eastlake": "a suburban high school",
    "Buchanan High School, Clovis, CA": "a large high school in California",
    "Buchanan High School": "a large high school", "Buchanan": "a large high school",
    "Dayton Christian, Centerville, OH": "a private high school in Ohio",
    "Dayton Christian": "a private high school",
    "Queens, NY (club: NY Crush, Next Level Baseball)": "national club baseball in New York",
    "club: NY Crush, Next Level Baseball": "national club teams",
    "NY Crush, Next Level Baseball": "national club teams",
    "NY Crush": "a national club team", "Next Level Baseball": "a national club team",
    "club tournaments in Seattle and Portland": "club tournaments outside the usual recruiting map",
    "a San Diego tournament": "an out-of-state club tournament",
    "White Rock, British Columbia (Canada)":
        "a club scene outside the usual recruiting map, in Canada",
    "Palm Beach Gardens, FL": "a suburban high school in Florida",
    "Fresno, CA": "a public high school in California",
    "Long Island": "the national club circuit",
    "NCAA Woman of the Year": "a national academic and athletic award",
    "WBCA D2 National Player of the Year": "the D2 national player of the year",
    "NJCAA honorable mention All-American": "an all-American mention at the JUCO level",
    "First NAIA champion in school history": "the first national champion in program history",
    "first NAIA champion in school history": "the first national champion in program history",
    "NCAA D3 steeplechase champion": "an NCAA D3 national champion",
    "Colombian national team": "a national team",
    # League names (NBA, MLS, NCAA, NAIA, NJCAA) stay: they are not a school or
    # an athlete, and the sport is already stated on the page.
}
# These single words are also ordinary English or place names, so they apply
# only inside story, athlete and story-data files.
STORY_ONLY = {"White", "Centre", "Colorado", "Alabama", "Minnesota",
              "Hastings", "Tomball", "Buchanan", "Eastlake", "Doane", "Lowe",
              "Butler", "Perez", "Rodriguez", "Marpet", "Coward", "Renfrow",
              "Pirosko", "Pichardo", "Rodenfels", "Groenewegen", "Wondolowski"}

DISCLAIMER = re.compile(r"Not affiliated with or endorsed by [^.<]{1,140}\. Facts from public sources\.")
DISCLAIMER_TO = ("Not affiliated with or endorsed by the athlete or any program in this story. "
                 "Facts are from public sources.")


def is_story_scope(p: pathlib.Path) -> bool:
    s = str(p).replace("\\", "/")
    return any(k in s for k in ("/story/", "/athlete/", "stor", "IMAGES.json", "INPUT.json",
                                "manifest.json", "head-tags", "jsonld", "CLAIMS.csv",
                                "SCRIPTS", "data.json", "data_build.py", "make.py",
                                "build_pages.py"))


def targets():
    seen = set()
    for base in DEPLOYED:
        for p in (ROOT / base).rglob("*"):
            if p.is_file() and p.suffix.lower() in EXTS:
                seen.add(p)
    for rel in GENERATORS:
        p = ROOT / rel
        if p.is_file():
            seen.add(p)
    return sorted(seen)


def write(p, txt):
    if not DRY:
        p.write_text(txt, encoding="utf-8")


# The RecruitIQ comparator names five real programs. Their published marks are
# the point of the table, so they become lettered programs with tier tags
# rather than disappearing.
TIERS = {"Big Ten": "Power 4", "Ivy": "private, high academic",
         "MAC": "mid-major", "Summit League": "mid-major", "": "D1"}
LETTER = "ABCDEFGH"


def anonymize_recruitiq():
    f = ROOT / "site" / "recruitiq" / "data.json"
    if not f.is_file():
        return 0
    d = json.loads(f.read_text(encoding="utf-8"))
    n = 0
    for i, p in enumerate(d.get("programs", [])):
        p["id"] = f"prog-{LETTER[i]}"
        p["name"] = f"Program {LETTER[i]}"
        p["conference"] = TIERS.get(str(p.get("conference", "")).strip(), "D1")
        note = str(p.get("label_note", ""))
        p["label_note"] = re.sub(r"^\w[\w .]{0,24}labels?:", "This program labels", note)
        p.pop("not", None)
        n += 1
    u = d.get("uno")
    if isinstance(u, dict) and u.get("name"):
        u["name"] = "One more D1 program"
    write(f, json.dumps(d, indent=1, ensure_ascii=False) + "\n")
    return n


def main():
    table = sorted(list(FIRST_FULL.items()) + list(COACH.items()) + list(SCHOOL.items())
                   + [(s, f) for s, (f, _) in PEOPLE.items()],
                   key=lambda kv: -len(kv[0]))
    changed = 0
    for p in targets():
        try:
            txt = p.read_text(encoding="utf-8")
        except Exception:
            continue
        story = is_story_scope(p)
        new = DISCLAIMER.sub(DISCLAIMER_TO, txt)
        for k, v in table:
            if k in STORY_ONLY and not story:
                continue
            new = re.sub(r"\b" + re.escape(k) + r"\b", v, new)
        if new != txt:
            write(p, new)
            changed += 1
    print(("would rewrite" if DRY else "files rewritten") + f": {changed}")

    # URL slugs: /story/<surname>/ -> /story/<first>/, same under /athlete/
    moved = []
    for kind in ("story", "athlete"):
        base = ROOT / "site" / kind
        if not base.is_dir():
            continue
        for sur, (_, slug) in PEOPLE.items():
            old, new = base / sur.lower(), base / slug
            if old.is_dir():
                if new.exists():
                    shutil.rmtree(new)
                if not DRY:
                    old.rename(new)
                moved.append((f"/{kind}/{sur.lower()}/", f"/{kind}/{slug}/"))
    for p in targets():
        try:
            txt = p.read_text(encoding="utf-8")
        except Exception:
            continue
        new = txt
        for o, n in moved:
            new = re.sub(r"(https://recruiting-calendar\.vercel\.app)?" + re.escape(o), n, new)
            new = new.replace(o[1:], n[1:])
            new = new.replace(o.strip("/"), n.strip("/"))
            new = new.replace("ax-" + o.split("/")[2] + "-", "ax-" + n.split("/")[2] + "-")
        if new != txt:
            write(p, new)
    print(f"url slugs moved: {len(moved)}")

    # keep already-shared surname URLs alive
    vc = ROOT / "vercel.json"
    cfg = json.loads(vc.read_text(encoding="utf-8"))
    red = {(r["source"], r["destination"]) for r in cfg.get("redirects", [])}
    red.update(moved)
    cfg["redirects"] = [{"source": s, "destination": d} for s, d in sorted(red)]
    if not DRY:
        vc.write_text(json.dumps(cfg, indent=2) + "\n", encoding="utf-8")
    print(f"redirects now in vercel.json: {len(cfg['redirects'])}")

    # asset file names must not carry surnames either, matched on name tokens
    # so that files like white-balance.png are not collaterally renamed.
    named = []
    for p in (ROOT / "site").rglob("*"):
        if not p.is_file():
            continue
        parts = re.split(r"[.\-_ ]+", p.name.lower())
        low = p.name.lower()
        for sur, (_, slug) in PEOPLE.items():
            if sur.lower() in parts and sur.lower() != slug:
                named.append((str(p.relative_to(ROOT)),
                              p.parent / low.replace(sur.lower(), slug)))
    for old, new in named:
        if not DRY:
            (ROOT / old).rename(new)
    print(f"asset files renamed: {len(named)}")

    n = anonymize_recruitiq()
    print(f"comparator programs relabeled: {n}")

    left = {}
    for p in (ROOT / "site").rglob("*"):
        if not (p.is_file() and p.suffix.lower() in EXTS):
            continue
        t = p.read_text(encoding="utf-8", errors="ignore")
        for k in list(PEOPLE) + list(SCHOOL) + list(COACH):
            if k in STORY_ONLY and not is_story_scope(p):
                continue
            if re.search(r"\b" + re.escape(k) + r"\b", t):
                left.setdefault(k, []).append(str(p.relative_to(ROOT)))
    if left:
        print("\nRESIDUAL")
        for k, v in sorted(left.items(), key=lambda kv: -len(kv[1])):
            print(f"  {k:<26} {len(v):>3} files  e.g. {v[0]}")
    else:
        print("\nresidual names on the deployed surface: none")


if __name__ == "__main__":
    main()
