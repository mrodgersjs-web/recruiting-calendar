"""W11-4 verification: site/segments/ against the W7/W6 markdown sources.
Run: python3 v3/W11-segments/test_segments.py   (or pytest)
"""
import json, pathlib, re, unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
SITE = ROOT / "site"
SEG = SITE / "segments"
DATA = json.loads((SEG / "segments.json").read_text())
HTML = (SEG / "index.html").read_text()
JS = (SEG / "segments.js").read_text()
CSS = (SEG / "segments.css").read_text()
TEN = (ROOT / "v3/W7-segments/TEN-LAYERS.md").read_text()
MARKET = (ROOT / "v3/W7-segments/MARKET.md").read_text()


def resolve(href):
    """Map a site URL to a file in site/. Returns the path or None."""
    p = href.split("#")[0].split("?")[0]
    if not p:
        return SEG / "index.html"
    rel = p.lstrip("/")
    for c in (SITE / rel, SITE / rel / "index.html", SITE / (rel + ".html")):
        if c.is_file():
            return c
    return None


class Files(unittest.TestCase):
    def test_four_files_exist(self):
        for n in ("index.html", "segments.js", "segments.css", "segments.json"):
            self.assertTrue((SEG / n).is_file(), n)

    def test_design_system(self):
        self.assertIn("/assets/tokens.css", HTML)
        # W2 build_site.py strips the commit.css <link> from every index.html, so segments.css must import it
        self.assertTrue("/assets/commit.css" in HTML or '@import url("/assets/commit.css")' in CSS)
        tokens = (SITE / "assets/tokens.css").read_text()
        for f in ("Anton", "Barlow Condensed", "Inter Tight", "JetBrains Mono"):
            self.assertIn(f, tokens, f)
        for c in ("#0a0a0a", "#f5f3ef", "#d2321e"):
            self.assertIn(c, CSS.lower(), c)
        self.assertIn("var(--font-condensed)", CSS)

    def test_three_views_and_a11y(self):
        for v in ("view-a", "view-b", "view-c"):
            self.assertIn('id="%s"' % v, HTML)
        self.assertEqual(HTML.count('role="tab"'), 3)
        self.assertIn('<html lang="en"', HTML)
        self.assertIn("prefers-reduced-motion", CSS)
        self.assertIn("aria-live", HTML)

    def test_only_allowed_scripts_and_no_tracking(self):
        for s in re.findall(r'<script[^>]+src="([^"]+)"', HTML):
            self.assertTrue(s.startswith("/segments/") or s.startswith("/assets/"), s)
        self.assertNotIn("localStorage", JS)
        self.assertNotIn("sendBeacon", JS)
        self.assertEqual(len(re.findall(r"fetch\(", JS)), 1)


class Segments(unittest.TestCase):
    def test_six_segments_in_order(self):
        segs = DATA["segments"]
        self.assertEqual([s["id"] for s in segs], [1, 2, 3, 4, 5, 6])
        names = " | ".join(s["name"] for s in segs).lower()
        for needle in ("9th/10th", "late-start", "burned", "high-academic", "clock/mark", "emerging sport"):
            self.assertIn(needle, names, needle)

    def test_each_segment_has_plan_story_and_chains(self):
        for s in DATA["segments"]:
            self.assertGreaterEqual(len(s["plan"]), 4, s["name"])
            hrefs = [p["href"] for p in s["plan"]]
            self.assertEqual(len(hrefs), len(set(hrefs)), "duplicate link in " + s["name"])
            self.assertTrue(s["story"]["href"].startswith("/athlete/"))
            self.assertTrue(s["chains"] and all(1 <= c <= 6 for c in s["chains"]))
            self.assertTrue(s["spend_note"])
            for p in s["plan"]:
                for k in ("step", "why", "tool", "href", "planned_route"):
                    self.assertTrue(p.get(k), (s["name"], k))

    def test_burned_segment_ranges_match_brief(self):
        s = DATA["segments"][2]
        self.assertIn("$1,500", s["name"] + s["tag"])
        self.assertIn("$4,200", s["name"] + s["tag"])


class Links(unittest.TestCase):
    def all_hrefs(self):
        out = []
        for s in DATA["segments"]:
            out.append(s["story"]["href"])
            out += [p["href"] for p in s["plan"]]
        return out

    def test_every_plan_and_story_link_resolves(self):
        bad = [h for h in self.all_hrefs() if not h.startswith("#") and resolve(h) is None]
        self.assertEqual(bad, [])

    def test_hash_links_target_real_views(self):
        for h in (x for x in self.all_hrefs() if x.startswith("#")):
            self.assertIn('id="%s"' % h[1:], HTML)

    def test_static_html_links_resolve(self):
        for h in re.findall(r'(?:href|src)="(/[^"#?]*)', HTML):
            if h.startswith("/segments/") and h.endswith((".js", ".css", ".json")):
                self.assertTrue((SITE / h.lstrip("/")).is_file(), h)
            elif h.startswith("/assets/"):
                self.assertTrue((SITE / h.lstrip("/")).is_file(), h)
            else:
                self.assertIsNotNone(resolve(h), h)

    def test_js_fallback_links_resolve(self):
        for h in ("/start/", "/calendar/", "/playbooks/"):
            self.assertIsNotNone(resolve(h), h)

    def test_brief_routes_status_is_explicit(self):
        """The brief names /access /recruitiq /personalize /emerging-sports. Record, don't hide, which exist."""
        planned = {p["planned_route"] for s in DATA["segments"] for p in s["plan"]}
        missing = sorted(r for r in planned if not r.startswith("#") and resolve(r) is None)
        print("\n  planned routes not yet in site/ (mapped to nearest real page):", missing)
        self.assertEqual(missing, [])

    def test_brief_tool_routes_are_linked_and_live(self):
        """Brief names /start /access /recruitiq /personalize /emerging-sports /playbooks: each must be linked from some plan and exist."""
        linked = {p["href"].rstrip("/") for s in DATA["segments"] for p in s["plan"]}
        for r in ("/start", "/access", "/recruitiq", "/personalize", "/emerging-sports", "/playbooks"):
            self.assertIn(r, linked, r)
            self.assertIsNotNone(resolve(r), r)

    def test_seg_links_only_use_existing_pages_even_for_missing_planned(self):
        for s in DATA["segments"]:
            for p in s["plan"]:
                if p["planned_route"] != p["href"] and not p["planned_route"].startswith("#"):
                    self.assertIsNotNone(resolve(p["href"]), p)


class Chains(unittest.TestCase):
    def test_six_chains_sixty_layers(self):
        ch = DATA["chains"]
        self.assertEqual(len(ch), 6)
        for c in ch:
            self.assertEqual([l["n"] for l in c["layers"]], list(range(1, 11)), c["title"])
        self.assertEqual(sum(len(c["layers"]) for c in ch), 60)

    def test_42_evidenced_18_inferred(self):
        ev = sum(l["status"] == "EVIDENCED" for c in DATA["chains"] for l in c["layers"])
        inf = sum(l["status"] == "INFERRED" for c in DATA["chains"] for l in c["layers"])
        self.assertEqual((ev, inf), (42, 18))
        self.assertEqual((DATA["honesty"]["evidenced"], DATA["honesty"]["inferred"]), (42, 18))
        # independently count from the markdown source
        self.assertEqual(len(re.findall(r"\|EVIDENCED\|", TEN)), 42)
        self.assertEqual(len(re.findall(r"\|INFERRED\|", TEN)), 18)

    def test_layer_text_matches_source_verbatim(self):
        for c in DATA["chains"]:
            for l in c["layers"]:
                self.assertIn("|%s|%s|%s|%s|" % (l["n"], l["name"], l["text"], l["status"]), TEN)

    def test_inferred_layers_carry_no_invented_source(self):
        for c in DATA["chains"]:
            for l in c["layers"]:
                self.assertTrue(l["source"], l)
                if l["status"] == "INFERRED" and l["source"] != "-":
                    # inferred layers may cite an existing page as context, never a raw/ social file as proof
                    self.assertNotIn("/raw/", l["source"], l)

    def test_evidenced_layers_have_a_source(self):
        for c in DATA["chains"]:
            for l in c["layers"]:
                if l["status"] == "EVIDENCED":
                    self.assertNotEqual(l["source"], "-", (c["id"], l["n"]))

    def test_badge_text_and_render_path(self):
        self.assertEqual(DATA["badges"]["EVIDENCED"], "EVIDENCED \u2014 Social Fetch / Primary Rule")
        self.assertEqual(DATA["badges"]["INFERRED"], "INFERRED \u2014 Working Hypothesis")
        self.assertIn("badge(L.status)", JS)
        self.assertIn("sg-badge", CSS)

    def test_layer_ten_routes_to_tools(self):
        for c in DATA["chains"]:
            hits = [s for s in DATA["segments"] if c["id"] in s["chains"]]
            self.assertTrue(hits, "chain %s has no segment pointing to a tool" % c["id"])


class Spending(unittest.TestCase):
    def test_aspen_benchmarks(self):
        S = DATA["spending"]
        by = {x["label"]: x["amt"] for x in S["by_income"]}
        self.assertEqual((by["$100K+"], by["Under $50K"]), (1591, 604))
        sp = {x["label"]: x["amt"] for x in S["by_sport_2024"]}
        self.assertEqual(sp["Baseball"], 1113)
        self.assertEqual(S["ncaa_cert_fee"], 110)
        self.assertIn("aspeninstitute.org", S["url"])
        for fig in ("$1,591", "$604", "$1,113", "$1,016"):
            self.assertIn(fig, MARKET)  # figures must appear in the sourced MARKET.md

    def test_sizing_labeled_as_model(self):
        Z = DATA["sizing"]
        self.assertIn("MODEL ASSUMPTION", Z["label"])
        self.assertIn("not a census", Z["label"].lower())
        self.assertIn("ESTIMATE", " ".join(Z["assumptions"]))
        self.assertEqual(Z["total_serviceable_families"], 496245)
        self.assertEqual(len(Z["rows"]), 32)
        self.assertIn("Z.LABEL.TOUPPERCASE()", JS.upper())  # label from JSON is rendered, uppercased
        self.assertIn("not a census", HTML.lower())

    def test_sizing_rows_match_market_md(self):
        for r in DATA["sizing"]["rows"]:
            self.assertIn("| %s | %s |" % (r["sport"], r["hs"]), MARKET)

    def test_calculator_math_in_js(self):
        for needle in ("ncaa_cert_fee", "in-show", "in-camps", "in-meets", "r-left"):
            self.assertIn(needle, JS)


if __name__ == "__main__":
    unittest.main(verbosity=2)
