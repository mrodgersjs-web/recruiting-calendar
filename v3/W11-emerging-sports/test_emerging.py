"""W11 emerging-sports hub verification. Run: python3 -m unittest v3/W11-emerging-sports/test_emerging.py -v
(or: python3 v3/W11-emerging-sports/test_emerging.py)

NFHS numbers are checked against the page, data.json and the repo's MARKET.md. The overall total is the
NFHS-printed 8,266,244. The brief's 8,215,882 is NOT in any NFHS document; the tests assert it is not shown
as a fact and that the correction is disclosed."""
import json
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT / "site"
HUB = SITE / "emerging-sports"
HTML = (HUB / "index.html").read_text()
JS = (HUB / "emerging.js").read_text()
CSS = (HUB / "emerging.css").read_text()
DATA = json.loads((HUB / "data.json").read_text())
MARKET = (ROOT / "v3/W7-segments/MARKET.md").read_text()
STORIES = json.loads((ROOT / "v3/W1-stories/STORIES.json").read_text())["stories"]
NFHS_PDF = "a-us.storyblok.com/f/1022696/x/85a6414d04/2024-25-nfhs-high-school-athletics-participation-survey.pdf"


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs, self.ids, self.srcs = [], [], []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "href" in a:
            self.hrefs.append(a["href"])
        if "src" in a:
            self.srcs.append(a["src"])
        if "id" in a:
            self.ids.append(a["id"])


P = Links()
P.feed(HTML)


def sport(i):
    return next(s for s in DATA["sports"] if s["id"] == i)


class TestNFHSNumbers(unittest.TestCase):
    def test_page_has_all_four_numbers(self):
        for n in ("68,847", "74,064", "95,972", "8,266,244"):
            self.assertIn(n, HTML, n)

    def test_data_json_numbers(self):
        self.assertEqual(sport("flag-football")["participants"], 68847)
        self.assertEqual(sport("girls-wrestling")["participants"], 74064)
        self.assertEqual(sport("boys-volleyball")["participants"], 95972)
        self.assertEqual(DATA["overall"]["total"], 8266244)
        self.assertEqual(DATA["overall"]["boys"] + DATA["overall"]["girls"], DATA["overall"]["total"])
        self.assertEqual(DATA["overall"]["total"] - DATA["overall"]["prior_year"], DATA["overall"]["delta"])

    def test_numbers_match_repo_market_file(self):
        for n in ("68,847", "74,064", "95,972", "8,266,244"):
            self.assertIn(n, MARKET, f"{n} not in MARKET.md")

    def test_growth_figures(self):
        self.assertEqual(sport("flag-football")["growth_display"], "+60%")
        self.assertEqual(sport("girls-wrestling")["growth_display"], "+15%")
        self.assertEqual(sport("boys-volleyball")["growth_display"], "+24.2%")
        for g in ("+60%", "+15%", "+24.2%"):
            self.assertIn(g, HTML)

    def test_nfhs_school_counts_from_table(self):
        self.assertEqual(sport("flag-football")["schools"], 2736)
        self.assertEqual(sport("girls-wrestling")["schools"], 8100)
        self.assertEqual(sport("boys-volleyball")["schools"], 4303)

    def test_wrestling_more_than_doubled_since_2021_22(self):
        self.assertGreater(74064, 2 * 31654)
        self.assertIn("31,654", HTML)

    def test_requested_but_unverified_figures_not_asserted(self):
        # 8,215,882, 1,781 schools and 2,900+ schools are not in the NFHS table; page must disclose, not assert.
        self.assertIn("8,215,882", HTML)  # only inside the correction notice
        notice = re.search(r'id="correction">(.*?)</div>', HTML, re.S).group(1)
        for bad in ("8,215,882", "1,781", "2,900"):
            self.assertIn(bad, notice, f"{bad} must appear only in the correction notice")
            self.assertEqual(HTML.count(bad), notice.count(bad), f"{bad} used outside correction notice")
        self.assertNotIn("8,215,882", json.dumps(DATA["overall"]["total"]))
        self.assertIn("correction", DATA["overall"])


class TestSourceCitations(unittest.TestCase):
    def test_nfhs_survey_cited(self):
        self.assertIn("NFHS 2024-25 High School Athletics Participation Survey", HTML)
        self.assertIn(NFHS_PDF, HTML)
        self.assertIn("nfhs.org/stories/participation-in-high-school-sports-hits-record-high", HTML)

    def test_each_sport_has_nfhs_and_pathway_sources(self):
        for s in DATA["sports"]:
            self.assertIn(NFHS_PDF, s["nfhs_url"])
            self.assertIn("NFHS 2024-25", s["nfhs_source"])
            for body in ("ncaa", "naia", "njcaa"):
                p = s["pathway"][body]
                self.assertTrue(p["url"].startswith("https://"), (s["id"], body))
                self.assertTrue(p["status"] and p["detail"])

    def test_primary_domains_only(self):
        allowed = ("ncaa.org", "naia.org", "njcaa.org", "nfhs.org", "a-us.storyblok.com", "avca.org",
                   "nwcaonline.com", "ncvf.org", "ncaaorg.s3.amazonaws.com", "web3.ncaa.org")
        urls = []
        for s in DATA["sports"]:
            urls.append(s["nfhs_url"])
            urls += [s["pathway"][b]["url"] for b in ("ncaa", "naia", "njcaa")]
        urls += [r["url"] for r in DATA["aid_rules"]]
        for u in urls:
            self.assertTrue(any(d in u for d in allowed), u)

    def test_flag_football_pathway_claims(self):
        p = sport("flag-football")["pathway"]
        self.assertIn("Emerging", p["ncaa"]["status"])
        self.assertIn("January 2026", p["ncaa"]["detail"])
        self.assertIn("2026-27", p["naia"]["status"])
        self.assertIn("2027-28", p["njcaa"]["status"])
        self.assertIn("Emerging Sports for Women", HTML)

    def test_wrestling_pathway_claims(self):
        p = sport("girls-wrestling")["pathway"]
        self.assertIn("championship", p["ncaa"]["status"].lower())
        self.assertIn("2026", p["ncaa"]["detail"])
        self.assertIn("91st", p["ncaa"]["detail"])
        self.assertIn("NAIA Bylaws Article V Section C", p["naia"]["detail"])
        self.assertIn("Article V Section C", HTML)
        self.assertIn("National Collegiate Women's Wrestling Championships", HTML)

    def test_volleyball_pathway_claims(self):
        p = sport("boys-volleyball")["pathway"]
        self.assertIn("D1 and D2", p["ncaa"]["status"])
        self.assertIn("Division III", p["ncaa"]["status"])
        self.assertIn("NAIA", p["naia"]["status"])
        self.assertIn("NJCAA", p["njcaa"]["detail"] + "NJCAA")
        self.assertIn("2026", p["njcaa"]["detail"])

    def test_aid_rules_cover_all_levels(self):
        levels = {r["level"] for r in DATA["aid_rules"]}
        self.assertEqual(levels, {"NAIA", "NCAA Division I", "NCAA Division II", "NCAA Division III", "NJCAA"})
        self.assertIn("NAIA Official Handbook", json.dumps(DATA["aid_rules"]) + HTML)
        d3 = next(r for r in DATA["aid_rules"] if r["id"] == "d3")
        self.assertIn("No athletic scholarships", d3["text"])


class TestStoryAndToolLinks(unittest.TestCase):
    def test_required_links_on_page(self):
        for h in ("/story/rodriguez", "/story/composite-volleyball", "/story/composite-wrestling", "/story/perez",
                  "/access", "/recruitiq"):
            self.assertIn(h, P.hrefs, h)

    def test_story_pages_exist(self):
        for slug in ("rodriguez", "composite-volleyball", "composite-wrestling", "perez"):
            self.assertTrue((SITE / "story" / slug / "index.html").exists(), slug)

    def test_story_ids_exist_in_stories_json_or_composites(self):
        ids = {s["id"] for s in STORIES}
        comps = {c["id"] for c in json.loads((ROOT / "v3/W4-composites/COMPOSITES.json").read_text())["stories"]}
        self.assertIn("rodriguez", ids)
        self.assertIn("perez", ids)
        self.assertIn("composite-volleyball", comps)
        self.assertIn("composite-wrestling", comps)

    def test_rodriguez_story_facts(self):
        r = next(s for s in STORIES if s["id"] == "rodriguez")
        self.assertEqual(r["division"], "NAIA")
        self.assertIn("Doane", r["college"])
        self.assertEqual(r["sport"], "Wrestling")

    def test_data_json_links_match_page(self):
        for l in DATA["links"]["stories"] + DATA["links"]["tools"]:
            self.assertIn(l["href"], P.hrefs)
        self.assertEqual(sport("girls-wrestling")["story"], "/story/rodriguez")
        self.assertEqual(sport("boys-volleyball")["story"], "/story/composite-volleyball")

    def test_composites_labelled_not_real(self):
        self.assertIn("Composite built from sourced paths. Not a real person.", HTML)


class TestChecklistAndStructure(unittest.TestCase):
    def test_checklist_has_ten_questions_and_levels(self):
        self.assertEqual(len(re.findall(r'\{id: "', JS)), 10)
        for label in ("NCAA Varsity (Championship)", "NCAA Emerging Sport", "NAIA Varsity", "NJCAA Varsity",
                      "Club (ACHA / NCVF / school club)"):
            self.assertIn(label, HTML)
        self.assertIn("deposit", JS.lower())

    def test_interactive_hooks(self):
        for i in ("sport-tabs", "sport-panels", "checklist", "progress-bar", "reset-checklist", "aid-rows"):
            self.assertIn(i, P.ids, i)
        self.assertIn("localStorage", JS)
        self.assertIn("role", JS)
        self.assertIn("/emerging-sports/data.json", JS)

    def test_assets_referenced_exist(self):
        self.assertIn("/emerging-sports/emerging.css", HTML)
        self.assertIn("/emerging-sports/emerging.js", HTML)
        for f in ("emerging.css", "emerging.js", "data.json", "index.html"):
            self.assertTrue((HUB / f).exists(), f)

    def test_basic_a11y_and_seo(self):
        self.assertIn('<html lang="en">', HTML)
        self.assertEqual(HTML.count("<h1"), 1)
        self.assertIn('rel="canonical"', HTML)
        self.assertIn("prefers-reduced-motion", CSS)
        self.assertIn(":focus-visible", CSS)

    def test_no_prohibited_claims_or_dashes(self):
        for bad in ("guarantee", "scholarship probability"):
            self.assertNotIn(bad + "d", HTML.lower().replace("guarantee ", "guarantee"))
        self.assertNotIn("\u2014", HTML)
        self.assertNotIn("\u2014", JS)

    def test_scope_of_files(self):
        self.assertEqual(sorted(p.name for p in HUB.iterdir()),
                         ["data.json", "emerging.css", "emerging.js", "index.html"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
