"""W11-3 verification: the live page (site/personalize) must agree with the W10 Python engine.

Run: python3 -m unittest v3/W11-personalization/test_personalize_page.py  (or `python3 test_personalize_page.py`)
Parity tests execute site/personalize/personalize.js under Node and compare to the Python engine on the
same seed, same intake, same fixed `today`. Skipped (not passed) if Node is missing.
"""
import json, os, re, shutil, subprocess, sys, unittest
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
W10 = os.path.join(ROOT, "v3", "W10-personalization")
SITE = os.path.join(ROOT, "site", "personalize")
sys.path.insert(0, W10)
from personalize import parse_intake, personalize, to_ics, IntakeError  # noqa: E402

NODE = shutil.which("node")
TODAY = date(2026, 11, 6)
def _text(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


HTML = _text(os.path.join(SITE, "index.html"))
JS = _text(os.path.join(SITE, "personalize.js"))
UI = _text(os.path.join(SITE, "personalize.ui.js"))
SEED_W10 = os.path.join(W10, "data", "rows.seed.json")
SEED_SITE = os.path.join(SITE, "seed.json")


def _read(path, mode="rb"):
    with open(path, mode) as f:
        return f.read()


def _json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def node_run(script):
    p = subprocess.run([NODE, "-e", script], capture_output=True, text=True, timeout=60, cwd=SITE)
    if p.returncode != 0:
        raise AssertionError("node failed: " + p.stderr)
    return p.stdout


def js_personalize(intake, today_iso, include_stale=False):
    script = """
const P=require('./personalize.js');
const rows=JSON.parse(require('fs').readFileSync('./seed.json','utf8')).rows;
const intake=%s; const t=P.parseD(%s);
const prof=P.parseIntake(intake, new Date(t).getUTCFullYear());
const res=P.personalize(prof, rows, t, %s);
process.stdout.write(JSON.stringify({res, ics:P.toIcs(res)}));
""" % (json.dumps(intake), json.dumps(today_iso), "true" if include_stale else "false")
    return json.loads(node_run(script))


class SeedParity(unittest.TestCase):
    def test_seed_is_byte_identical_to_w10(self):
        self.assertEqual(_read(SEED_W10), _read(SEED_SITE))

    def test_seed_row_count_and_ids(self):
        rows = _json(SEED_SITE)["rows"]
        self.assertEqual(len(rows), 12)
        self.assertEqual(len({r["entity_id"] for r in rows}), 12)


class W10StillPasses(unittest.TestCase):
    def test_all_54_w10_tests_pass(self):
        p = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-t", ".", "-v"],
                           capture_output=True, text=True, cwd=W10, timeout=120)
        out = p.stderr + p.stdout
        m = re.search(r"Ran (\d+) tests?", out)
        self.assertIsNotNone(m, out[-500:])
        self.assertEqual(int(m.group(1)), 54, out[-500:])
        self.assertEqual(p.returncode, 0, out[-800:])
        self.assertIn("OK", out.splitlines()[-1])


@unittest.skipUnless(NODE, "node not installed; JS/Python parity cannot be checked")
class EngineParity(unittest.TestCase):
    INTAKES = [
        {"sport": "football", "class_year": 2028, "area": "802", "budget_band": "any", "goal_level": "college_prospect"},
        {"sport": "football", "class_year": 2027, "area": "80202", "budget_band": "low", "goal_level": "college_prospect"},
        {"sport": "baseball", "class_year": 2029, "area": "801", "budget_band": "mid", "goal_level": "college_prospect"},
        {"sport": "track", "class_year": 2030, "area": "809", "budget_band": "free", "goal_level": "development"},
        {"sport": "football", "class_year": 2026 + 5, "area": "999", "budget_band": "high", "goal_level": "recreational"},
        {"sport": "basketball", "class_year": 2028, "area": "804", "budget_band": "any", "goal_level": "development"},
        {"sport": "hockey", "class_year": 2028, "area": "803", "budget_band": "any", "goal_level": "college_prospect"},
    ]

    def _py(self, intake, today=TODAY, stale=False):
        rows = _json(SEED_W10)["rows"]
        return personalize(parse_intake(intake, today_year=today.year), rows, today, include_stale=stale)

    def test_ranked_order_scores_flags_match(self):
        for intake in self.INTAKES:
            py = self._py(intake)
            js = js_personalize(intake, TODAY.isoformat())["res"]
            for key in ("ranked", "not_yet_announced"):
                self.assertEqual([i["entity_id"] for i in py[key]], [i["entity_id"] for i in js[key]], (key, intake))
                for a, b in zip(py[key], js[key]):
                    for f in ("score", "score_parts", "reasons", "highest_label", "flags", "read_on", "url", "state"):
                        self.assertEqual(a[f], b[f], (a["entity_id"], f, intake))
            self.assertEqual(py["hidden"], js["hidden"], intake)
            self.assertEqual(py["empty_reason"], js["empty_reason"], intake)
            self.assertEqual(py["profile_echo"], js["profile_echo"], intake)

    def test_past_and_undated_hidden_by_default_on_both_sides(self):
        intake = self.INTAKES[0]
        js = js_personalize(intake, TODAY.isoformat())["res"]
        ids = [i["entity_id"] for i in js["ranked"] + js["not_yet_announced"]]
        self.assertNotIn("event-juniorday-ponderosa-2026", ids)   # status past + dated 2026-06-30
        self.assertEqual(js["hidden"]["past"], 1)
        # undated event rows are never in `ranked`; they only surface as "not yet announced"
        self.assertIn("event-mines-camps", [i["entity_id"] for i in js["not_yet_announced"]])
        self.assertNotIn("event-mines-camps", [i["entity_id"] for i in js["ranked"]])

    def test_future_today_makes_rows_stale_like_python(self):
        far = date(2027, 3, 1)  # read_on 2026-11-06 is >30/90 days old
        for intake in self.INTAKES[:3]:
            py = self._py(intake, far, True)
            js = js_personalize({**intake, "class_year": max(intake["class_year"], 2027)}, far.isoformat(), True)["res"]
            py = self._py({**intake, "class_year": max(intake["class_year"], 2027)}, far, True)
            self.assertEqual(py["hidden"], js["hidden"])
            self.assertEqual(py["stale_rows"], js["stale_rows"])
            self.assertEqual([i["entity_id"] for i in py["ranked"]], [i["entity_id"] for i in js["ranked"]])

    def test_ics_is_byte_identical_to_python(self):
        for intake in self.INTAKES:
            py = to_ics(self._py(intake))
            js = js_personalize(intake, TODAY.isoformat())["ics"]
            self.assertEqual(py, js, intake)

    def test_ics_rfc5545_crlf_rules(self):
        ics = js_personalize(self.INTAKES[0], TODAY.isoformat())["ics"]
        self.assertTrue(ics.startswith("BEGIN:VCALENDAR\r\nVERSION:2.0\r\n"))
        self.assertTrue(ics.endswith("END:VCALENDAR\r\n"))
        self.assertIsNone(re.search(r"(?<!\r)\n", ics), "bare LF found")
        self.assertIn("DTEND;VALUE=DATE:20270630", ics)            # exclusive end: window ends 06-29
        self.assertIn("window\\, not a confirmed day\\; confirm", ics)  # escaped , and ;
        self.assertNotIn("event-mines-camps", ics)                 # undated/tbd never exported
        self.assertNotIn("juniorday", ics)                         # past never exported

    def test_intake_rejects_same_inputs_as_python(self):
        cases = [{**self.INTAKES[0], "child_name": "x"}, {**self.INTAKES[0], "dob": "2010-01-01"},
                 {**self.INTAKES[0], "area": "123 Main St"}, {**self.INTAKES[0], "area": "80202-1234"},
                 {**self.INTAKES[0], "class_year": "2010-05-04"}, {**self.INTAKES[0], "class_year": 1999},
                 {**self.INTAKES[0], "sport": "curling"}, {**self.INTAKES[0], "budget_band": "ludicrous"},
                 {k: v for k, v in self.INTAKES[0].items() if k != "sport"}]
        for c in cases:
            with self.assertRaises(IntakeError, msg=str(c)):
                parse_intake(c)
            out = node_run("const P=require('./personalize.js');try{P.parseIntake(%s,2026);console.log('ACCEPTED')}"
                           "catch(e){console.log('REJECTED:'+e.name)}" % json.dumps(c))
            self.assertTrue(out.startswith("REJECTED:IntakeError"), (c, out))

    def test_full_zip_truncated_in_js(self):
        out = node_run("const P=require('./personalize.js');console.log(JSON.stringify(P.parseIntake("
                       "{sport:'football',class_year:2028,area:'80202',budget_band:'any',goal_level:'college_prospect'},2026)))")
        self.assertEqual(json.loads(out)["zip3"], "802")
        self.assertNotIn("80202", out)

    def test_geo_table_matches_python(self):
        from personalize import geo
        out = json.loads(node_run("const P=require('./personalize.js');const z=Object.keys(P.ZIP3).concat(['999']);"
                                  "const r={};z.forEach(a=>z.forEach(b=>r[a+'-'+b]=P.miles(a,b)));console.log(JSON.stringify(r))"))
        for k, v in out.items():
            a, b = k.split("-")
            self.assertEqual(geo.miles(a, b), v, k)


    def test_future_read_on_and_vetted_label_handled_like_python(self):
        """Synthetic rows: a read_on in the future must be stale; vetted/endorsed must be downgraded."""
        base = _json(SEED_W10)["rows"]
        fut = dict(base[0]); fut.update(entity_id="fut-1", read_on="2027-01-01")
        vet = dict(base[1]); vet.update(entity_id="vet-1", field_labels={"overall": "vetted", "x": "endorsed"})
        rows = [fut, vet]
        intake = self.INTAKES[0]
        py = personalize(parse_intake(intake, today_year=2026), rows, TODAY, include_stale=True)
        script = ("const P=require('./personalize.js');const rows=%s;const t=P.parseD('2026-11-06');"
                  "const r=P.personalize(P.parseIntake(%s,2026),rows,t,true);process.stdout.write(JSON.stringify(r))"
                  % (json.dumps(rows), json.dumps(intake)))
        js = json.loads(node_run(script))
        self.assertEqual(py["hidden"], js["hidden"])
        self.assertEqual(py["stale_rows"], js["stale_rows"])
        self.assertIn("fut-1", [r["entity_id"] for r in js["stale_rows"]])
        self.assertEqual([i["highest_label"] for i in py["ranked"]], [i["highest_label"] for i in js["ranked"]])
        self.assertEqual([i["highest_label"] for i in js["ranked"]], ["listed"])

    def test_vetted_and_endorsed_never_emitted(self):
        for intake in self.INTAKES:
            res = js_personalize(intake, TODAY.isoformat())["res"]
            for it in res["ranked"] + res["not_yet_announced"]:
                self.assertIn(it["highest_label"], ("listed", "observed", "verified"))


class PageContract(unittest.TestCase):
    def test_design_system_loaded(self):
        for needle in ("/assets/tokens.css", "/assets/commit.css", "personalize.css", "personalize.js"):
            self.assertIn(needle, HTML)
        css = _text(os.path.join(SITE, "personalize.css")).lower()
        for hex_ in ("#0a0a0a", "#f5f3ef", "#d2321e"):
            self.assertIn(hex_, css)
        tokens = _text(os.path.join(ROOT, "site", "assets", "tokens.css"))
        for font in ("Anton", "Barlow Condensed", "Inter Tight", "JetBrains Mono"):
            self.assertIn(font, tokens)

    def test_required_filters_present(self):
        for opt in ("Football", "Baseball", "Track &amp; Field", "Multi-sport",
                    "Mental Performance / CMPC", "Speed &amp; Strength", "Governing body / CHSAA calendar",
                    "College ID Camp / Showcase", "Verified (registry row)", "Listed (directory entry)",
                    "Within 15 miles", "Monthly budget cap", "Show historical/undated reference rows"):
            self.assertIn(opt, HTML, opt)

    def test_sections_a_b_c_d_present(self):
        for sid in ("sec-intake", "sec-results", "sec-checklist", "sec-ics", "btn-ics", "btn-print", "btn-ck-dl"):
            self.assertIn('id="%s"' % sid, HTML)

    def test_no_vetted_claim_anywhere_in_ui_output(self):
        # "Vetted" may appear only in the sentence explaining why we do NOT show it.
        for name, text in (("html", HTML), ("ui", UI)):
            for m in re.finditer(r"vetted", text, re.I):
                ctx = text[max(0, m.start() - 80): m.end() + 80].lower()
                self.assertTrue("do not show" in ctx or "never shows" in ctx or "never show" in ctx
                                or "vetting checklist" in ctx or "parent vetting" in ctx or "vetted" not in text[m.start():m.end()].lower() or "vetting" in ctx,
                                (name, ctx))
        badge_logic = re.search(r"function badgeFor\(it\)\s*\{[^}]*\}", UI).group(0)
        self.assertIn('"Verified"', badge_logic)
        self.assertIn('"Listed"', badge_logic)
        self.assertNotIn("Vetted", badge_logic)

    def test_card_fields_rendered(self):
        for field in ('"Distance"', '"Checked on"', '"Source"', "badgeFor(it)", "it.url", "it.read_on", "it.miles"):
            self.assertIn(field, UI)

    def test_checklist_questions_cover_required_topics(self):
        ck = UI[UI.index("var CHECKLIST"): UI.index("function renderChecklist")].lower()
        for topic in ("sb24-113", "background check", "insurance", "one-on-one", "refund", "cmpc", "cscs",
                      "mandatory-reporter", "safesport", "consumer reporting agency"):
            self.assertIn(topic, ck, topic)
        self.assertGreaterEqual(ck.count('["'), 12)
        for title in ('"background check"', '"insurance"', '"one-on-one observation"', '"refund and cancellation policy"',
                      '"verifiable credentials"', '"mandatory-reporter training"', '"safesport / abuse prevention"'):
            self.assertIn(title, ck, title)

    def test_no_sb26_100_cited_as_law(self):
        # SB26-100 was postponed indefinitely; the page may not call AED/CPR a legal requirement.
        ck = (UI + HTML).lower()
        self.assertNotIn("sb26-100", ck)
        self.assertIn("not currently required by colorado law", ck)

    def test_no_banned_health_or_outcome_claims_in_own_voice(self):
        voice = re.sub(r"<script.*?</script>", "", HTML, flags=re.S | re.I)
        for w in ("prevents injury", "injury prevention", "medically supervised", "reduces anxiety",
                  "improves mental health", "guaranteed", "treats anxiety", "cures"):
            self.assertNotIn(w, voice.lower(), w)


class ZeroMinorPII(unittest.TestCase):
    BAD_NAMES = ("child_name", "childname", "first_name", "last_name", "full_name", "birth", "dob", "birthday",
                 "phone", "tel", "mobile", "email", "school", "schedule", "address", "street", "photo", "gpa",
                 "jersey", "stats", "ssn", "age")

    def test_form_controls_are_only_the_allowed_set(self):
        ids = set(re.findall(r'<(?:input|select|textarea)\b[^>]*\bid="([^"]+)"', HTML))
        self.assertEqual(ids, {"f-sport", "f-category", "f-verif", "f-class", "f-zip", "f-radius", "f-budget", "f-hist"})

    def test_no_pii_input_attributes(self):
        for tag in re.findall(r"<(?:input|select|textarea)\b[^>]*>", HTML, re.I):
            low = tag.lower()
            for bad in self.BAD_NAMES:
                for attr in ("name", "id", "autocomplete", "placeholder", "type"):
                    for m in re.finditer(r'\b%s="([^"]*)"' % attr, low):
                        val = m.group(1)
                        if attr == "type":
                            self.assertNotIn(val, ("email", "tel", "date", "datetime-local", "file", "password"), tag)
                        elif attr == "autocomplete":
                            self.assertIn(val, ("off",), tag)
                        else:
                            self.assertFalse(re.search(r"(^|[-_])%s($|[-_])" % re.escape(bad), val), (bad, tag))

    def test_form_does_not_post_or_send_anything(self):
        self.assertIsNone(re.search(r"<form\b[^>]*\b(action|method)=", HTML, re.I))
        allcode = JS + UI
        for bad in ("XMLHttpRequest", "sendBeacon", "localStorage", "sessionStorage", "document.cookie",
                    "indexedDB", "method:", "POST"):
            self.assertNotIn(bad, allcode, bad)
        fetches = re.findall(r"fetch\(([^)]*)\)", allcode)
        self.assertEqual(len(fetches), 1, fetches)
        self.assertIn('"/personalize/seed.json"', fetches[0])
        self.assertIn('credentials: "omit"', fetches[0])

    def test_no_third_party_scripts_or_trackers(self):
        for src in re.findall(r'<script[^>]+src="([^"]+)"', HTML):
            self.assertTrue(src.startswith("/"), src)
        for dom in ("google-analytics", "googletagmanager", "facebook", "segment", "hotjar", "doubleclick"):
            self.assertNotIn(dom, HTML.lower())

    def test_engine_input_is_exactly_the_five_allowed_fields(self):
        m = re.search(r"P\.parseIntake\(\{(.*?)\}, new Date", UI, re.S)
        keys = set(re.findall(r"(\w+):", m.group(1)))
        self.assertEqual(keys, {"sport", "class_year", "area", "budget_band", "goal_level"})

    def test_page_states_the_privacy_contract(self):
        low = HTML.lower()
        for phrase in ("never asks for a child's name", "birth date", "phone", "school", "practice schedule"):
            self.assertIn(phrase, low)

    def test_seed_has_no_minor_pii_fields(self):
        rows = _json(SEED_SITE)["rows"]
        banned = {"child", "minor", "athlete_name", "dob", "birth_date", "phone", "email", "school", "schedule"}
        for r in rows:
            self.assertFalse(banned & set(r), r["entity_id"])
            for c in r.get("credential_checks", []):
                self.assertFalse({"email", "phone"} & set(c), r["entity_id"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
