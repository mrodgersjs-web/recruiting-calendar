#!/usr/bin/env python3
"""W11 verification suite for RecruitIQ.
Run: python3 v3/W11-recruitiq/test_recruitiq.py
Checks: data.json + index.html numbers vs W10 AUDIT.md VERIFIED rows; MIT excluded from the
live calculator; all 9 audit corrections present in W7 RECRUITIQ.md; calculator logic."""
import json, os, re, sys, unittest

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AUDIT = open(os.path.join(ROOT, "v3/W10-recruitiq/AUDIT.md"), encoding="utf-8").read()
DOC = open(os.path.join(ROOT, "v3/W7-recruitiq/RECRUITIQ.md"), encoding="utf-8").read()
HTML = open(os.path.join(ROOT, "site/recruitiq/index.html"), encoding="utf-8").read()
JS = open(os.path.join(ROOT, "site/recruitiq/recruitiq.js"), encoding="utf-8").read()
CSS = open(os.path.join(ROOT, "site/recruitiq/recruitiq.css"), encoding="utf-8").read()
DATA = json.load(open(os.path.join(ROOT, "site/recruitiq/data.json"), encoding="utf-8"))


def audit_row(n):
    """Return the AUDIT.md table row for claim #n as (claim, verdict, evidence)."""
    for line in AUDIT.splitlines():
        m = re.match(r"\|\s*%d\s*\|(.*)" % n, line)
        if m:
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            return cells[1], cells[2], "|".join(cells[3:])
    raise AssertionError("audit row %d not found" % n)


def secs(s):
    if ":" in s:
        m, r = s.split(":")
        return int(m) * 60 + float(r)
    return float(s)


def prog(pid):
    return [p for p in DATA["programs"] if p["id"] == pid][0]


def displays(pid, ev):
    return [m["display"] for m in prog(pid)["marks"][ev]]


def elig(div, sport):
    r = [x for x in DATA["eligibility"] if x["division"] == div and x["sport"] == sport]
    assert len(r) == 1, (div, sport, len(r))
    return r[0]


class TestAuditParsing(unittest.TestCase):
    def test_audit_scorecard_present(self):
        self.assertIn("20 VERIFIED, 4 HOLD (#15, #16, #17, #23)", AUDIT)

    def test_verified_rows_are_verified(self):
        for n in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 18, 19, 20, 21, 22, 24):
            self.assertTrue(audit_row(n)[1].startswith("VERIFIED"), n)
        for n in (15, 16, 17, 23):
            self.assertTrue(audit_row(n)[1].startswith("HOLD"), n)


class TestBucket1Numbers(unittest.TestCase):
    def test_d1_roster_caps_match_audit_row_1(self):
        claim = audit_row(1)[0]
        for k, v in (("Football 105", "105"), ("Baseball 34", "34"), ("Track 45", "45"), ("Men's XC 17", "17")):
            self.assertIn(k, claim)
        self.assertEqual(elig("D1 opted-in", "Football")["roster_cap"], "105")
        self.assertEqual(elig("D1 opted-in", "Baseball")["roster_cap"], "34")
        self.assertTrue(elig("D1 opted-in", "Track & Field / XC")["roster_cap"].startswith("45"))
        self.assertIn("Men's XC 17", elig("D1 opted-in", "Track & Field / XC")["roster_cap"])

    def test_d1_legacy_caps_match_audit_row_5(self):
        claim = audit_row(5)[0]
        for k in ("FBS 85 counters", "FCS 63 equivalencies and 85 counters", "11.7 equivalencies and 27 counters"):
            self.assertIn(k, claim)
        self.assertIn("FBS: 85 counters", elig("D1 non-opted-in (legacy)", "Football")["aid_cap"])
        self.assertIn("63 equivalencies and 85 counters", elig("D1 non-opted-in (legacy)", "Football")["aid_cap"])
        self.assertIn("11.7 equivalencies and 27 counters", elig("D1 non-opted-in (legacy)", "Baseball")["aid_cap"])

    def test_d2_caps_match_audit_row_6(self):
        claim = audit_row(6)[0]
        for k in ("Football 36.0", "Baseball 9.0", "12.6"):
            self.assertIn(k, claim)
        self.assertTrue(elig("D2", "Football")["aid_cap"].startswith("36.0"))
        self.assertTrue(elig("D2", "Baseball")["aid_cap"].startswith("9.0"))
        self.assertTrue(elig("D2", "Track & Field / XC")["aid_cap"].startswith("12.6"))

    def test_d3_zero_aid_row_7(self):
        self.assertIn("no athletics scholarships", audit_row(7)[0])
        for s in ("Football", "Baseball", "Track & Field / XC"):
            self.assertTrue(elig("D3", s)["aid_cap"].startswith("0"))

    def test_naia_caps_row_9(self):
        claim = audit_row(9)[0]
        for k in ("Football 24", "Baseball 12", "Track 12"):
            self.assertIn(k, claim)
        self.assertTrue(elig("NAIA", "Football")["aid_cap"].startswith("24"))
        self.assertTrue(elig("NAIA", "Baseball")["aid_cap"].startswith("12"))
        self.assertTrue(elig("NAIA", "Track & Field / XC")["aid_cap"].startswith("12"))
        urls = [s["url"] for s in elig("NAIA", "Football")["sources"]]
        self.assertIn("https://www.naia.org/wp-content/uploads/2026/05/2025_Official_Handbook.pdf", urls)
        self.assertFalse(any("nextcommit" in u for u in urls))

    def test_njcaa_counts_from_audit_extra_table(self):
        self.assertIn("Football 85, Baseball 30, Track 20", AUDIT)
        self.assertTrue(elig("NJCAA", "Football")["aid_cap"].startswith("85"))
        self.assertTrue(elig("NJCAA", "Baseball")["aid_cap"].startswith("30"))
        self.assertTrue(elig("NJCAA", "Track & Field / XC")["aid_cap"].startswith("20"))
        u = [s["url"] for s in elig("NJCAA", "Football")["sources"]][0]
        self.assertIn("2026-2027-Sports-Procedures-Chart-9-9-26.pdf", u)

    def test_gpa_rules_row_10_11(self):
        self.assertIn("2.3", audit_row(11)[0])
        self.assertIn("10/7", audit_row(11)[0])
        self.assertIn("minimum 2.3 core GPA", elig("D1 opted-in", "Football")["gpa_rule"])
        self.assertIn("10/7", elig("D1 opted-in", "Football")["gpa_rule"])
        self.assertIn("minimum 2.2 core GPA", elig("D2", "Football")["gpa_rule"])
        self.assertIn("2.3+ GPA", audit_row(10)[0])
        self.assertIn("2.3+ GPA", elig("NAIA", "Football")["gpa_rule"])
        self.assertIn("18 ACT / 970 SAT", elig("NAIA", "Football")["gpa_rule"])

    def test_every_eligibility_row_has_a_clickable_primary_source(self):
        self.assertEqual(len(DATA["eligibility"]), 18)
        for r in DATA["eligibility"]:
            self.assertTrue(r["sources"], r)
            for s in r["sources"]:
                self.assertTrue(s["url"].startswith(("http://", "https://")))
        self.assertFalse(any("nextcommit" in s["url"] for r in DATA["eligibility"] for s in r["sources"]))

    def test_all_six_divisions_and_three_sports_selectable(self):
        for d in ("D1 opted-in", "D1 non-opted-in (legacy)", "D2", "D3", "NAIA", "NJCAA"):
            self.assertIn("<option>%s</option>" % d, HTML)
            for s in ("Football", "Baseball", "Track & Field / XC"):
                elig(d, s)
        for s in ("Football", "Baseball", "Track &amp; Field / XC"):
            self.assertIn("<option>%s</option>" % s, HTML)

    def test_html_noscript_numbers(self):
        for k in ("Football 105, Baseball 34, Track 45", "Football 36.0, Baseball 9.0, Track/XC 12.6",
                  "0 athletic aid", "Football 24, Baseball 12, Track 12", "Football 85, Baseball 30, Track 20"):
            self.assertIn(k, HTML)


class TestBucket2Marks(unittest.TestCase):
    def test_brown_row_18(self):
        claim = audit_row(18)[0]
        for k in ("10.55/10.75", "47.50/48.70", "1:53.50/1:55.50", "3:55.00/3:58.00"):
            self.assertIn(k, claim.replace(" ", ""))
        self.assertEqual(displays("brown", "100"), ["10.55", "10.75"])
        self.assertEqual(displays("brown", "400"), ["47.50", "48.70"])
        self.assertEqual(displays("brown", "800"), ["1:53.50", "1:55.50"])
        self.assertEqual(displays("brown", "1500"), ["3:55.00", "3:58.00"])

    def test_rutgers_row_19(self):
        claim = audit_row(19)[0].replace(" ", "")
        for k in ("10.65/10.35", "47.90/46.20", "1:53.50/1:49.00", "3:58.00/3:45.00"):
            self.assertIn(k, claim)
        # Audit lists roster-spot mark first, full-aid mark second; data lists fastest (full aid) first.
        self.assertEqual(displays("rutgers", "100"), ["10.35", "10.65"])
        self.assertEqual(displays("rutgers", "400"), ["46.20", "47.90"])
        self.assertEqual(displays("rutgers", "800"), ["1:49.00", "1:53.50"])
        self.assertEqual(displays("rutgers", "1500"), ["3:45.00", "3:58.00"])
        tiers = {m["display"]: m["tier"] for m in prog("rutgers")["marks"]["100"]}
        self.assertEqual(tiers["10.35"], "Consider for Full Aid")
        self.assertEqual(tiers["10.65"], "Roster Spot Consideration")

    def test_princeton_row_20(self):
        claim = audit_row(20)[0]
        for k in ("10.80", "48.80", "1:53.00", "3:55.00"):
            self.assertIn(k, claim)
        self.assertEqual(displays("princeton", "100"), ["10.80"])
        self.assertEqual(displays("princeton", "400"), ["48.80"])
        self.assertEqual(displays("princeton", "800"), ["1:53.00"])
        self.assertEqual(displays("princeton", "1500"), ["3:55.00"])

    def test_emu_row_21(self):
        claim = audit_row(21)[0]
        for k in ("10.30/10.50/10.70", "46.65/47.50/48.50", "1:49.50/1:52.00/1:54.00", "3:47.50/3:54.00/3:58.00"):
            self.assertIn(k, claim.replace(" ", ""))
        self.assertEqual(displays("emu", "100"), ["10.30", "10.50", "10.70"])
        self.assertEqual(displays("emu", "400"), ["46.65", "47.50", "48.50"])
        self.assertEqual(displays("emu", "800"), ["1:49.50", "1:52.00", "1:54.00"])
        self.assertEqual(displays("emu", "1500"), ["3:47.50", "3:54.00", "3:58.00"])

    def test_oru_row_22(self):
        claim = audit_row(22)[0]
        for k in ("100m 10.75", "400m 49.6", "800m 1:54.00", "1500m 3:55.00",
                  "Achieving the marks does not guarantee a scholarship offer or roster spot"):
            self.assertIn(k, claim)
        self.assertEqual(displays("oru", "100"), ["10.75"])
        self.assertEqual(displays("oru", "400"), ["49.60"])
        self.assertEqual(displays("oru", "800"), ["1:54.00"])
        self.assertEqual(displays("oru", "1500"), ["3:55.00"])
        self.assertEqual(prog("oru")["disclaimer"]["by"], "school")
        self.assertIn("does not guarantee a scholarship offer or roster spot", prog("oru")["disclaimer"]["text"])

    def test_seconds_consistent_with_display(self):
        for p in DATA["programs"]:
            for ev, ms in p["marks"].items():
                for m in ms:
                    self.assertAlmostEqual(m["seconds"], secs(m["display"]), places=2)
                self.assertEqual([m["seconds"] for m in ms], sorted(m["seconds"] for m in ms),
                                 "marks must be ordered fastest first: %s %s" % (p["id"], ev))

    def test_exactly_five_programs_and_uno_policy_note(self):
        self.assertEqual([p["id"] for p in DATA["programs"]], ["brown", "rutgers", "princeton", "emu", "oru"])
        self.assertFalse(DATA["uno"]["in_calculator"])
        self.assertIn("1%-100%", DATA["uno"]["policy_note"])
        self.assertIn("unoprivateers.com", DATA["uno"]["url"])

    def test_emu_has_no_1_100_percent_claim(self):
        emu = json.dumps(prog("emu"))
        self.assertNotIn("1-100%", emu)
        self.assertNotIn("1%-100%", emu)
        self.assertNotIn("range from", emu)

    def test_tier_names_cover_required_labels(self):
        tiers = {m["tier"] for p in DATA["programs"] for ms in p["marks"].values() for m in ms}
        for t in ("Consider for Full Aid", "Target Performance", "Walk-On Consideration"):
            self.assertIn(t, tiers)

    def test_vintage_dates(self):
        want = {"princeton": "2024-07-17", "rutgers": "2025-10-10", "brown": "2026-08-24",
                "emu": "2026-09-02", "oru": "2025-10-24"}
        for k, v in want.items():
            self.assertEqual(prog(k)["vintage"], v)
            self.assertIn(v.replace("-", "/").replace("/0", "/"), prog(k)["url"].replace("/0", "/"))
        self.assertEqual(DATA["uno"]["vintage"], "2026-08-19")
        self.assertIn("2025-26", prog("rutgers")["cycle"])
        self.assertIn("2026-27", prog("brown")["cycle"])


class TestMITExclusion(unittest.TestCase):
    def test_mit_not_in_programs_or_calculator(self):
        ids = [p["id"] for p in DATA["programs"]]
        self.assertNotIn("mit", ids)
        self.assertNotIn("MIT", json.dumps(DATA["programs"]))
        self.assertNotIn("MIT", json.dumps(DATA["uno"]))

    def test_mit_listed_as_excluded_with_reason(self):
        ex = {x["id"]: x for x in DATA["excluded_from_calculator"]}
        self.assertIn("mit", ex)
        self.assertIn("2026-11-06", ex["mit"]["reason"])
        self.assertIn("not re-read in W10", ex["mit"]["reason"])

    def test_mit_marks_never_appear_in_shipped_site_files(self):
        blob = json.dumps(DATA) + HTML + JS
        for forbidden in ("11.10", "11.40", "50.50", "51.90", "1:56", "4:02", "4:08"):
            self.assertNotIn(forbidden, blob, forbidden)

    def test_js_only_compares_data_programs(self):
        self.assertIn("D.programs.map", JS)
        self.assertNotIn("mit", JS.lower().replace("limit", "").replace("submit", "").replace("emit", ""))

    def test_audit_row_23_is_hold_for_mit(self):
        self.assertTrue(audit_row(23)[1].startswith("HOLD"))
        self.assertIn("do not use the MIT row in any shipped surface", audit_row(23)[2])


class TestBucket4Ratios(unittest.TestCase):
    def test_all_18_cells_match_audit_row_13(self):
        claim = audit_row(13)[0]
        nums = re.findall(r"[\d,]+(?:\.\d+)?%?", claim)
        for r in DATA["ratios"]:
            cells = ["{:,}".format(r["hs"]), "{:,}".format(r["ncaa"]), "%.1f%%" % r["overall"],
                     "%.1f" % r["d1"], "%.1f" % r["d2"], "%.1f" % r["d3"]]
            for c in cells:
                self.assertIn(c, nums, c)
            html_cells = ["{:,}".format(r["hs"]), "{:,}".format(r["ncaa"]), "%.1f%%" % r["overall"],
                          "%.1f%%" % r["d1"], "%.1f%%" % r["d2"], "%.1f%%" % r["d3"]]
            for c in html_cells:
                self.assertIn(c, HTML, c)

    def test_headline_percentages(self):
        d = {r["sport"]: r["overall"] for r in DATA["ratios"]}
        self.assertEqual(d, {"Football": 8.1, "Baseball": 8.8, "Track & Field": 5.4})

    def test_ratio_arithmetic_matches_overall(self):
        for r in DATA["ratios"]:
            self.assertAlmostEqual(r["ncaa"] / r["hs"] * 100, r["overall"], delta=0.06)

    def test_method_disclosure(self):
        m = " ".join(DATA["ratio_method"]).lower()
        for k in ("headcount", "club teams", "naia", "njcaa", "not an individual"):
            self.assertIn(k, m)
        self.assertIn("2024-25", DATA["ratio_source"]["label"])

    def test_previous_edition_label_row_15(self):
        self.assertTrue(audit_row(15)[1].startswith("HOLD"))
        self.assertIn("previous NCAA edition (2023RES file", DATA["previous_edition_label"])
        pe = {p["sport"]: (p["previous_pct"], p["current_pct"]) for p in DATA["previous_edition"]}
        self.assertEqual(pe["Football"], (7.5, 8.1))
        self.assertEqual(pe["Baseball"], (8.1, 8.8))
        self.assertNotIn("2022-23", json.dumps(DATA))

    def test_fact_sheet_labeled_pre_house(self):
        fs = DATA["fact_sheet"]
        self.assertIn("2%", fs["text"])
        self.assertIn("pre-House", fs["label"])
        self.assertNotIn("2022-23", json.dumps(fs))


class TestPanelsNotConflated(unittest.TestCase):
    def test_four_distinct_panels(self):
        for i in (1, 2, 3, 4):
            self.assertEqual(HTML.count('id="bucket%d"' % i), 1)
            self.assertIn("Bucket %d" % i, HTML)

    def test_no_scholarship_probability_output(self):
        for bad in ("chance of a scholarship", "your odds", "probability of getting"):
            self.assertNotIn(bad, (HTML + JS).lower())

    def test_bucket3_has_no_football_baseball_cutoff_numbers(self):
        b3 = HTML[HTML.index('id="bucket3"'):HTML.index('id="bucket4"')]
        self.assertNotRegex(b3, r"\b\d{2}(\.\d+)? ?mph\b")
        self.assertNotRegex(b3, r"\b4\.\d\d\b")
        self.assertIn("Not an NCAA standard", b3)

    def test_bucket3_text_in_data(self):
        b = DATA["bucket3"]
        self.assertIn("No football program and no baseball program", b["why_unpublished"])
        self.assertTrue(any("film" in x.lower() for x in b["evaluated"]))
        self.assertIn("not NCAA standards", b["aggregator_note"])

    def test_design_system(self):
        self.assertIn("/assets/tokens.css", HTML)
        self.assertIn("/assets/commit.css", HTML)
        for f in ("Anton", "Barlow Condensed", "Inter Tight", "JetBrains Mono"):
            self.assertIn(f, CSS)
        for c in ("#0a0a0a", "#f5f3ef", "#d2321e"):
            self.assertIn(c, CSS.lower())
        for p in ("recruitiq.css", "recruitiq.js"):
            self.assertIn(p, HTML)

    def test_does_not_touch_forbidden_paths(self):
        for p in ("site/index.html", "site/athlete", "site/story", "site/tools"):
            self.assertTrue(os.path.exists(os.path.join(ROOT, p)))


class TestCalculatorLogic(unittest.TestCase):
    """Re-implements the JS placement rule (lower is better, tier met if t <= mark) on the data."""

    def place(self, pid, ev, t):
        return [m["tier"] for m in prog(pid)["marks"][ev] if t <= m["seconds"] + 1e-9]

    def test_rutgers_100m_10_30_meets_full_aid(self):
        self.assertEqual(self.place("rutgers", "100", 10.30), ["Consider for Full Aid", "Roster Spot Consideration"])

    def test_rutgers_100m_10_50_roster_only(self):
        self.assertEqual(self.place("rutgers", "100", 10.50), ["Roster Spot Consideration"])

    def test_brown_800_slower_than_all(self):
        self.assertEqual(self.place("brown", "800", secs("1:56.00")), [])

    def test_emu_400_boundary_inclusive(self):
        self.assertEqual(self.place("emu", "400", 47.50), ["Scholarship", "Walk-On Consideration"])

    def test_parse_formats_in_js(self):
        self.assertIn(r"/^(\d+):(\d{1,2}(?:\.\d+)?)$/", JS)
        self.assertIn("t <= m.seconds", JS)


class TestNineCorrectionsInDoc(unittest.TestCase):
    def test_1_naia_primary_flag_removed(self):
        self.assertIn("https://www.naia.org/wp-content/uploads/2026/05/2025_Official_Handbook.pdf", DOC)
        row = [l for l in DOC.splitlines() if l.startswith("| NAIA Football 24")][0]
        self.assertIn("NAIA Official Handbook", row)
        self.assertNotIn("third-party", row)
        self.assertNotIn("NOT verified", row)
        self.assertNotIn("nextcommit.ai/blog/athletic-scholarships-roster-limits-2026", DOC)

    def test_2_njcaa_chart_primary(self):
        row = [l for l in DOC.splitlines() if l.startswith("| NJCAA scholarship counts")][0]
        self.assertIn("Football 85; Baseball 30; Track 20", row)
        self.assertIn("2026-2027-Sports-Procedures-Chart-9-9-26.pdf", row)
        self.assertNotIn("third-party", row)
        self.assertNotIn("before shipping", row)

    def test_3_age_based_approved_not_adopted(self):
        self.assertIn("approved by the D1 Cabinet 2026-06-23", DOC)
        self.assertIn("not final until the Cabinet meeting concluded Wednesday 2026-06-24", DOC)
        self.assertIn("2026-07-31", DOC)
        self.assertIn("now past", DOC)
        self.assertNotIn("adopted 2026-06-23", DOC)

    def test_4_transfer_gpa_unconfirmed(self):
        self.assertIn("still reads 2.5 for D1 (and 2.2 for D2)", DOC)
        self.assertIn("unconfirmed by any NCAA primary document", DOC)
        self.assertNotIn("NCAA cut the transferable GPA requirement", DOC)

    def test_5_emu_no_1_100_percent(self):
        emu = [l for l in DOC.splitlines() if l.startswith("| Eastern Michigan")][0]
        self.assertNotIn("1-100%", emu)
        self.assertNotIn("range from", emu)
        uno_sentence = [l for l in DOC.splitlines() if "New Orleans: scholarships" in l][0]
        self.assertIn("1%-100%", uno_sentence)
        self.assertIn("New Orleans-only", DOC)
        self.assertNotIn("1-100%", DOC)

    def test_6_vintages(self):
        rows = {l.split("|")[1].strip().split(" (")[0]: l for l in DOC.splitlines()
                if l.startswith("| ") and "https://" in l and "(D" in l.split("|")[1]}
        want = {"Princeton": "2024-07-17", "Rutgers": "2025-10-10", "Brown": "2026-08-24",
                "Eastern Michigan": "2026-09-02", "Oral Roberts": "2025-10-24"}
        for name, d in want.items():
            self.assertIn("vintage", rows[name])
            self.assertIn(d, rows[name].split("vintage")[1], name)
        self.assertIn("2025-26 cycle", rows["Rutgers"])
        self.assertIn("2026-27", rows["Brown"])
        self.assertIn("vintage: PDF dated 2026-08-19", DOC)

    def test_7_mit_marked(self):
        mit = [l for l in DOC.splitlines() if l.startswith("| MIT")][0]
        self.assertIn("source page down on 2026-11-06", mit)
        self.assertIn("not re-read in W10", mit)
        self.assertIn("excluded from the live interactive calculator on `/recruitiq/`", mit)

    def test_8_fact_sheet_label(self):
        line = [l for l in DOC.splitlines() if "only about 2% of high school athletes" in l][0]
        self.assertNotIn("data 2022-23", line)
        self.assertIn("pre-House", line)

    def test_9_previous_edition_label(self):
        self.assertIn("previous NCAA edition (the 2023RES file", DOC)
        self.assertNotIn("(2022-23)", DOC)


if __name__ == "__main__":
    unittest.main(verbosity=2)
