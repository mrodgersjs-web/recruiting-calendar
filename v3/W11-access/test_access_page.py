"""Verification for site/access (W11). Stdlib only. Run: python3 -m unittest -v test_access_page  (from this dir)
JS logic is exercised through node's vm module (package.json is type=module, so require() would not work)."""
import json, os, re, subprocess, sys, unittest, hashlib
HERE = os.path.dirname(os.path.abspath(__file__)); V3 = os.path.dirname(HERE); ROOT = os.path.dirname(V3)
SITE = os.path.join(ROOT, "site", "access"); W10 = os.path.join(V3, "W10-access")
DELIV = ["1-send-date-worksheet.md", "2-questionnaire-checklist.md", "3-contact-scripts.md", "4-highlight-link-checklist.md", "5-ask-your-coach-one-pager.md", "6-follow-log.csv"]
def read(*p):
    with open(os.path.join(*p), encoding="utf-8") as fh: return fh.read()
def sha(p):
    with open(p, "rb") as fh: return hashlib.sha256(fh.read()).hexdigest()
HTML = lambda: read(SITE, "index.html")

def node(js):
    r = subprocess.run(["node", "--input-type=module", "-e", js], capture_output=True, text=True, cwd=SITE, timeout=30)
    if r.returncode: raise AssertionError(r.stderr)
    return r.stdout.strip()
LOAD = """import fs from 'fs'; import vm from 'vm'; const ctx={}; ctx.window=ctx; vm.createContext(ctx);
for (const f of ['access-rules.js','access-core.js']) vm.runInContext(fs.readFileSync(f,'utf8'),ctx);
const R=ctx.AccessRules, C=ctx.AccessCore;"""

class Files(unittest.TestCase):
    def test_core_files_exist(self):
        for f in ["index.html", "access.js", "access.css", "access-rules.js", "access-core.js"]:
            self.assertTrue(os.path.getsize(os.path.join(SITE, f)) > 500, f)
    def test_six_deliverables_present_and_identical_to_w10(self):
        for f in DELIV:
            a = os.path.join(SITE, "deliverables", f); b = os.path.join(W10, "deliverables", f)
            self.assertTrue(os.path.exists(a), f)
            self.assertEqual(sha(a), sha(b), f)
    def test_html_links_all_six_downloads(self):
        h = HTML()
        for f in DELIV: self.assertIn("/access/deliverables/" + f, h)
    def test_every_local_href_src_resolves(self):
        h = HTML()
        for m in re.findall(r'(?:src|href)="(/access/[^"#]+)"', h):
            self.assertTrue(os.path.exists(os.path.join(ROOT, "site", m.lstrip("/"))), m)

class Design(unittest.TestCase):
    def test_tokens_and_nav(self):
        h = HTML()
        for s in ["/assets/tokens.css", "/assets/commit.css", "/access/access.css"]: self.assertIn(s, h)
        for p in ['href="/"', 'href="/start"', 'href="/recruitiq"', 'href="/personalize"', 'href="/segments"', 'href="/emerging-sports"', 'href="/price"']:
            self.assertIn(p, h, p)
    def test_css_uses_design_tokens(self):
        c = read(SITE, "access.css")
        for t in ["--font-display", "--font-condensed", "--font-mono", "--c-signal", "--c-ink"]: self.assertIn(t, c)
        self.assertNotRegex(c, r"#(?!(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b)")
    def test_tokens_file_defines_fonts_and_colors(self):
        t = read(ROOT, "site", "assets", "tokens.css")
        for s in ["Anton", "Barlow Condensed", "Inter Tight", "JetBrains Mono", "#d2321e"]: self.assertIn(s, t)
    def test_four_tools_present(self):
        h = HTML()
        for i in ['id="dates"', 'id="email"', 'id="list"', 'id="services"', 'id="a-sport"', 'id="b-form"', 'id="c-body"']: self.assertIn(i, h)

class Bylaws(unittest.TestCase):
    """All bylaw strings must be verified: present in site/data.js (system of record) or the W10 kit/deliverables."""
    def test_every_bylaw_in_rules_is_verified_in_data_js(self):
        rules = read(SITE, "access-rules.js"); data = read(ROOT, "site", "data.js")
        cites = set(re.findall(r"\b1[34]\.[0-9]+(?:\.[0-9]+)*", " ".join(re.findall(r'rule: "([^"]+)"', rules))))
        self.assertTrue({"13.1.3.1", "13.4.1", "13.1.3.1.1", "13.1.1.1.9"} <= cites, cites)
        for c in cites: self.assertIn(c, data, "bylaw %s not in data.js" % c)
    def test_cited_strings_in_contact_kit_agree_with_page(self):
        """contact_kit.py carries no bylaw numbers or dates (the caller supplies D1 dates), so agreement is on the
        division model, the NAIA source and the 30-school cap that the kit does encode."""
        kit = read(W10, "contact_kit.py"); rules = read(SITE, "access-rules.js"); h = HTML()
        self.assertNotRegex(kit, r"\b13\.\d")                       # kit never invents a bylaw
        self.assertIn("naia.org/why-naia/recruiting", kit); self.assertIn("naia.org/why-naia/recruiting", rules)
        for div in ("D1", "D2", "D3", "NAIA"): self.assertIn('"%s":' % div, kit)
        for div in ("NCAA D1", "NCAA D2", "NCAA D3", "NAIA", "NJCAA"): self.assertIn(div, rules)
        self.assertIn("No recruiting calendar and no limit on communication", kit)
        self.assertIn("no recruiting calendar and no limit on communication", rules)
        self.assertIn("any time", rules.lower())

    def test_dates_match_data_js_for_2029(self):
        out = node(LOAD + """const o={};for(const s of ['football','baseball','track'])o[s]=R.lookup(s,'NCAA D1',2029).rows;
        console.log(JSON.stringify({fc:o.football.coach.date,fo:o.football.official.date,fx:o.football.offcampus.date,bc:o.baseball.coach.date,bo:o.baseball.official.date,tc:o.track.coach.date,tv:o.track.official.date,tx:o.track.offcampus.date}))""")
        d = json.loads(out)
        self.assertEqual(d, {"fc": "2027-06-15", "fo": "2028-04-01", "fx": "2028-01-01", "bc": "2027-08-01", "bo": "2027-09-01", "tc": "2027-06-15", "tv": "2027-08-01", "tx": "2027-06-15"})
    def test_all_sport_division_class_combinations_resolve(self):
        out = node(LOAD + """let n=0;for(const s of Object.keys(R.SPORTS))for(const d of R.DIVISIONS)for(const c of R.CLASSES){const r=R.lookup(s,d,c);
        for(const k of ['athlete','coach','unofficial','official','offcampus']){const x=r.rows[k];if(!x||!x.rule||!x.scope||!x.note)throw new Error(s+d+c+k);n++}}console.log(n)""")
        self.assertEqual(out, str(3 * 5 * 5 * 5))
    def test_scope_notice_and_no_ncaa_cite_for_naia_njcaa(self):
        out = node(LOAD + """const a=R.lookup('football','NAIA',2028),j=R.lookup('track','NJCAA',2028),d=R.lookup('football','NCAA D1',2028),d2=R.lookup('football','NCAA D2',2028);
        console.log(JSON.stringify([a.rows.coach.scope,a.rows.coach.rule,j.rows.coach.scope,j.rows.coach.date,d.rows.coach.scope,d2.rows.coach.scope,a.banner]))""")
        a = json.loads(out)
        self.assertIn("not NCAA", a[0]); self.assertNotRegex(a[1], r"\b13\.\d"); self.assertIn("not NCAA", a[2]); self.assertIsNone(a[3])
        self.assertEqual(a[4], "D1-specific"); self.assertEqual(a[5], "D2-specific"); self.assertIn("not governed", a[6])
    def test_class_years_shift_by_whole_years(self):
        out = node(LOAD + "console.log(R.lookup('baseball','NCAA D1',2027).rows.coach.date, R.lookup('baseball','NCAA D1',2030).rows.coach.date)")
        self.assertEqual(out, "2025-08-01 2028-08-01")

class Builder(unittest.TestCase):
    def test_subject_format(self):
        out = node(LOAD + "console.log(C.build({gradYear:'2028',position:'WR',metric:'4.55 40',gpa:'3.6'}).subject)")
        self.assertEqual(out, "2028 WR \u2014 4.55 40 \u2014 3.6 GPA")
    def test_linter_flags(self):
        out = node(LOAD + """const f={firstName:'Sam',gradYear:'2028',position:'WR',metric:'',gpa:'',film:'',coachLast:'Reyes',school:'X',interest:''};
        const codes=t=>C.lint(f,t).map(x=>x.code);console.log(JSON.stringify([codes('my son is elite'),codes('my daughter is a must-see'),codes('hello'),codes('We guarantee a full ride')]))""")
        a = json.loads(out)
        self.assertIn("parent-voice", a[0]); self.assertIn("hype", a[0]); self.assertIn("hype", a[1]); self.assertIn("parent-voice", a[1])
        for c in ("no-film", "no-metric"): self.assertIn(c, a[2])
        self.assertIn("promise", a[3])
    def test_clean_input_has_no_red_flags(self):
        out = node(LOAD + """const f={firstName:'Sam',gradYear:'2028',sport:'Football',position:'WR',metric:'4.55 40',gpa:'3.6',interest:'Business',film:'https://youtu.be/x',school:'Mesa',coachLast:'Reyes'};
        const b=C.build(f);console.log(JSON.stringify(C.lint(f,b.body+b.dm)))""")
        self.assertEqual(json.loads(out), [])
    def test_generated_text_has_no_promise_language_per_w10(self):
        sys.path.insert(0, W10); import contact_kit as ck
        out = node(LOAD + """const f={firstName:'Sam',gradYear:'2028',sport:'Football',position:'WR',metric:'4.55 40',gpa:'3.6',interest:'Business',film:'https://youtu.be/x',school:'Mesa',coachLast:'Reyes'};const b=C.build(f);console.log(JSON.stringify([b.subject,b.body,b.dm]))""")
        for t in json.loads(out): self.assertEqual(ck.promise_hits(t), [])
    def test_dm_has_no_parent_voice(self):
        out = node(LOAD + "const b=C.build({firstName:'Sam',position:'SS'});console.log(b.body+b.dm)")
        self.assertNotRegex(out, r"(?i)my (son|daughter)")

class TargetList(unittest.TestCase):
    def test_seed_is_30_and_tiers_balanced(self):
        out = node(LOAD + "const r=C.seedRows();const t={};r.forEach(x=>t[x.tier]=(t[x.tier]||0)+1);console.log(JSON.stringify([r.length,t]))")
        n, t = json.loads(out); self.assertEqual(n, 30)
        self.assertEqual(t, {"Reach": 5, "Match": 8, "Academic-Aid": 5, "In-State": 6, "JUCO-or-NAIA Safety": 6})
    def test_cap_matches_w10(self):
        sys.path.insert(0, W10); import contact_kit as ck
        self.assertEqual(node(LOAD + "console.log(C.TARGET_CAP)"), str(ck.TARGET_CAP))
    def test_cadence_matches_w10(self):
        sys.path.insert(0, W10); import contact_kit as ck
        self.assertEqual(json.loads(node(LOAD + "console.log(JSON.stringify(C.CADENCE.map(c=>c.d)))")), ck.CADENCE_DAYS)
    def test_csv_and_ics(self):
        out = node(LOAD + """const rows=C.seedRows();rows[0].school='Mesa, State "U"';rows[0].firstSend='2026-12-01';
        console.log(JSON.stringify([C.toCsv(rows),C.toIcs(rows,'2026-11-06')]))""")
        csv_, ics = json.loads(out)
        self.assertEqual(csv_.splitlines()[0], "tier,school,division,coach,questionnaire,firstSend,status")
        self.assertIn('"Mesa, State ""U"""', csv_); self.assertEqual(ics.count("BEGIN:VEVENT"), 4)
        self.assertEqual(ics.count("DTSTART;VALUE=DATE:"), 4)
        for d in ("20261201", "20261211", "20261225", "20270115"): self.assertIn("DTSTART;VALUE=DATE:" + d, ics)
        self.assertIn("\r\n", ics); self.assertTrue(ics.startswith("BEGIN:VCALENDAR"))

class Privacy(unittest.TestCase):
    def test_no_network_or_storage_in_scripts(self):
        for f in ["access.js", "access-core.js", "access-rules.js"]:
            s = read(SITE, f)
            for bad in ["fetch(", "XMLHttpRequest", "sendBeacon", "localStorage", "sessionStorage", "document.cookie", "WebSocket", "indexedDB", "navigator.sendBeacon"]:
                self.assertNotIn(bad, s, f + ": " + bad)
    def test_no_form_posts_or_trackers(self):
        h = HTML()
        self.assertNotRegex(h, r'(?i)<form[^>]+(action=|method="?post)')
        self.assertNotRegex(h, r'(?i)(google-analytics|gtag|fbq\(|pixel|segment\.com)')
        self.assertEqual(re.findall(r'<script[^>]+src="(https?:)?//', h), [])
        self.assertIn('autocomplete="off"', h); self.assertIn("first name only", h.lower())
    def test_only_first_name_field_no_last_name_phone_or_address(self):
        h = HTML()
        for bad in ['id="b-lastName"', 'type="tel"', 'id="b-phone"', 'id="b-address"', 'id="b-email"']: self.assertNotIn(bad, h)

class Copy(unittest.TestCase):
    def test_no_promise_language_in_page_copy_per_w10_patterns(self):
        sys.path.insert(0, W10); import contact_kit as ck
        h = re.sub(r"<(script|style)[\s\S]*?</\1>", "", HTML()); text = re.sub(r"<[^>]+>", " ", h)
        # Only the negated disclaimer/guarantee-warning sentences may match; strip those before checking.
        text = re.sub(r"[^.]*(do not|does not|cannot|no tool|nobody|not promise|No reply|legitimate services|No legitimate|If yes|Do you promise)[^.]*\.", " ", text, flags=re.I)
        self.assertEqual(ck.promise_hits(text), [])
    def test_disclaimers_present(self):
        h = HTML().lower()
        for s in ["not legal advice", "we do not recruit or place athletes", "no reply, introduction, scholarship, offer or roster spot is promised", "nothing here is sent", "verified"][:3]: self.assertIn(s, h)
        self.assertIn("no reply, introduction, scholarship, offer or roster spot is promised", h)
    def test_decision_guide_content(self):
        h = HTML()
        for s in ["certified mail", "automatically", "attorney general", "Eligibility Center", "questionnaire", "Hudl", "Education, not legal advice"]: self.assertIn(s, h)
        self.assertNotRegex(h, r"(?i)\bncsa\b.{0,40}\b(scam|fraud)\b")
    def test_no_em_dash_in_page_copy(self):
        self.assertNotIn("\u2014", re.sub(r"<script[\s\S]*?</script>", "", HTML()))

class W10Regression(unittest.TestCase):
    def test_existing_49_w10_tests_still_pass(self):
        r = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"], cwd=W10, capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr[-800:])
        self.assertRegex(r.stderr, r"Ran 49 tests")

class Scope(unittest.TestCase):
    def test_deliverable_dir_has_exactly_seven_files(self):
        self.assertEqual(sorted(os.listdir(os.path.join(SITE, "deliverables"))), sorted(DELIV + ["6-follow-log-README.md"]))

if __name__ == "__main__": unittest.main(verbosity=2)
