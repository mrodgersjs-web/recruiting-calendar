# -*- coding: utf-8 -*-
"""Inventory every state-specific or place-specific token in the four customer decks, with
the sentence around each hit, so the national rework can be planned from a list and not
from memory. Decks scanned: men's basketball (W19), football and girls' basketball (W20),
women's volleyball (W24)."""
import re, sys, pathlib, html
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = pathlib.Path(r"C:\Users\Jloeh\Developer\recruiting-calendar\v3")
DECKS = {
    "mens-basketball": list((ROOT / "W19-plain").glob("*-plain.html")),
    "football": list((ROOT / "W20-two-sports").glob("fb-playbook-plain.html")),
    "girls-basketball": list((ROOT / "W20-two-sports").glob("wbb-playbook-plain.html")),
    "volleyball": list((ROOT / "W24-volleyball").glob("vb-playbook-plain.html")),
}
# state / region / city / association / program tokens that make a book local
TOKENS = [
    "wisconsin", "wiaa", "badger", "marquette", " uw-", "uwg", "uwb", "uww", "uwl", "uw-stevens",
    "oshkosh", "eau claire", "whitewater", "la crosse", "stevens point", "platteville",
    "green bay", "milwaukee", "manitowoc", "appleton", "geneva", "anytown", "waukesha",
    "wisconsin-born", "gopher", "packers", "brewers", "bucks",
    "illinois", "iowa", "michigan", "minnesota", "nebraska", "kansas", "texas", "oklahoma",
    "california", "hawaii", "brazilian", "charlotte", "hartford", "orlando", "las vegas",
    "anaheim", "indianapolis", "louisville", "pennsylvania", "atlantic", "midwest",
    "big ten", "horizon league", "summit league", "mvc", "big east", "atlantic 10", "northern",
    "d1central", "wells challenge", "hoist", "clemson", "georgia", "lsu", "uconn", "duke",
    "kentucky", "north carolina", "ucla", "stanford", "gonzaga", "butler", "creighton",
    "de paul", "notre dame", "cincinnati", "memphis", "st. john", "providence", "seton hall",
    "rutgers", "maryland", "virginia", "florida", "alabama", "auburn", "ohio state",
    "iowa state", "purdue", "indiana", "northwestern", "michigan state", "illinois state",
    "loyola", "bradley", "marquette", "wv", "ncaa region",
]


def clean(h):
    h = re.sub(r"<style>.*?</style>", " ", h, flags=re.S)
    h = html.unescape(re.sub(r"<[^>]+>", " ", h))
    return re.sub(r"\s+", " ", h)


for label, files in DECKS.items():
    for f in files:
        doc = clean(f.read_text(encoding="utf-8"))
        low = doc.lower()
        print("\n########## %s  (%s)  %d chars" % (label, f.name, len(doc)))
        hits = {}
        for t in TOKENS:
            for m in re.finditer(re.escape(t.strip()), low):
                a = max(0, m.start() - 70)
                b = min(len(doc), m.end() + 90)
                snip = doc[a:b].strip()
                hits.setdefault(t.strip(), []).append(snip)
        for t in sorted(hits, key=lambda k: -len(hits[k])):
            print("  %-16s %3d" % (t, len(hits[t])))
        print("  --- contexts for the top tokens ---")
        for t in sorted(hits, key=lambda k: -len(hits[k]))[:14]:
            for s in hits[t][:6]:
                print("   %s :: ...%s..." % (t, s[:150]))
