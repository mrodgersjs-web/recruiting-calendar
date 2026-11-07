import os, sys, io, json, unittest, tempfile, contextlib, re, ast
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
import contact_kit as ck, kit_cli, build_worksheets

FIELDS = dict(coach_last="Reyes", athlete_name="Sam Lee", sport="Soccer", position="midfielder", team="Metro FC",
              class_year="2029", specific_reason="your program plays the possession style I train in",
              video_url="https://youtu.be/abc", stat_line="Goals: 9", questionnaire_date="2026-11-01",
              athlete_phone_or_email="sam@example.com", event_name="Summer ID Camp", takeaway="first-touch drills",
              last_touch_date="2026-11-01", own_coach_last="Park", list_size="10", three_sentences="He works hard.")

class Promise(unittest.TestCase):
    def test_bad(self):
        for s in ["We guarantee a scholarship", "we will introduce you to college coaches",
                  "access to 50,000 coaches", "we will email the coaches", "90% of athletes get offers", "gets you an offer"]:
            self.assertTrue(ck.promise_hits(s), s)
    def test_clean(self):
        self.assertEqual(ck.promise_hits("Here is a checklist you run yourself."), [])
    def test_all_templates_clean(self):
        for n in ck.TEMPLATES:
            r = ck.render_template(n, FIELDS)
            self.assertEqual(ck.promise_hits(r["subject"] + r["body"]), [], n)
    def test_user_text_with_promise_rejected(self):
        f = dict(FIELDS, specific_reason="we guarantee you will love me")
        with self.assertRaises(ValueError): ck.render_template("intro_email", f)

class Render(unittest.TestCase):
    def test_missing_fields_listed(self):
        f = dict(FIELDS); f["video_url"] = ""
        with self.assertRaises(ck.MissingField) as c: ck.render_template("dm_short", f)
        self.assertIn("video_url", str(c.exception))
    def test_parent_copied_line(self):
        self.assertIn("parent is copied", ck.render_template("intro_email", FIELDS)["body"])
    def test_no_unfilled_braces(self):
        for n in ck.TEMPLATES: self.assertNotRegex(ck.render_template(n, FIELDS)["body"], r"\{\w+\}")

class Window(unittest.TestCase):
    def test_d1_future(self):
        r = ck.send_window("D1", "2027-06-15", "2026-11-06"); self.assertEqual(r["status"], "coaches_may_not_reply_yet"); self.assertEqual(r["days"], 221)
    def test_d1_open(self):
        self.assertEqual(ck.send_window("d1", "2026-06-15", "2026-11-06")["status"], "coaches_may_reply")
    def test_d1_open_today(self):
        self.assertEqual(ck.send_window("D1", "2026-11-06", "2026-11-06")["status"], "coaches_may_reply")
    def test_d1_missing_date_never_invented(self):
        r = ck.send_window("D1", None, "2026-11-06"); self.assertEqual(r["status"], "date_missing"); self.assertIsNone(r["days"])
    def test_naia_no_calendar(self):
        r = ck.send_window("NAIA", None, "2026-11-06"); self.assertIn("No recruiting calendar", r["note"]); self.assertTrue(r["family_may_write"])
    def test_family_may_write_all(self):
        for d in ck.DIVISION_NOTES: self.assertTrue(ck.send_window(d, "2027-06-15", "2026-11-06")["family_may_write"])
    def test_stale(self):
        self.assertIsNotNone(ck.send_window("D1", "2027-06-15", "2026-11-06", "2026-06-01")["stale_warning"])
        self.assertIsNone(ck.send_window("D1", "2027-06-15", "2026-11-06", "2026-10-30")["stale_warning"])
    def test_bad_division(self):
        with self.assertRaises(ValueError): ck.send_window("D9", None, "2026-11-06")

class Link(unittest.TestCase):
    def test_good(self): self.assertTrue(ck.check_video_link("https://youtu.be/x", 4, "Sam Lee 2029 Soccer Mid", True, True)["ok"])
    def test_not_url(self): self.assertFalse(ck.check_video_link("watch my film")["ok"])
    def test_http(self): self.assertFalse(ck.check_video_link("http://vimeo.com/1")["ok"])
    def test_attachment(self): self.assertFalse(ck.check_video_link("https://x.com/clip.mp4")["ok"])
    def test_length(self): self.assertFalse(ck.check_video_link("https://vimeo.com/1", 9)["ok"])
    def test_title(self): self.assertFalse(ck.check_video_link("https://vimeo.com/1", None, "film")["ok"])
    def test_youtube_private_reminder(self): self.assertTrue(any("Private" in x for x in ck.check_video_link("https://youtube.com/watch?v=1")["reminders"]))
    def test_never_fetches(self):
        src = open(os.path.join(ROOT, "contact_kit.py")).read()
        tree = ast.parse(src); mods = {a.name for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names} | \
            {n.module for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)}
        self.assertNotIn(None, mods)
        for banned in ("socket", "requests", "urllib.request", "http.client", "smtplib", "subprocess"):
            self.assertNotIn(banned, mods)

class Cadence(unittest.TestCase):
    def test_four(self):
        c = ck.cadence("2026-11-10"); self.assertEqual([x["date"] for x in c], ["2026-11-10", "2026-11-20", "2026-12-04", "2026-12-25"])
    def test_cap(self):
        rows = [{"school": "S%d" % i, "coach_last": "x"} for i in range(31)]; self.assertFalse(ck.check_target_list(rows)["ok"])
        self.assertTrue(ck.check_target_list(rows[:30])["ok"])
    def test_dupes(self):
        self.assertFalse(ck.check_target_list([{"school": "A", "coach_last": "b"}, {"school": "a", "coach_last": "B"}])["ok"])

def row(**k):
    base = {c: "" for c in ck.LOG_COLUMNS}; base.update(k); return base
def to_csv(rows):
    import csv; b = io.StringIO(); w = csv.DictWriter(b, ck.LOG_COLUMNS, lineterminator="\n"); w.writeheader(); w.writerows(rows); return b.getvalue()

class Log(unittest.TestCase):
    T = "2026-11-06"
    def test_blank_valid(self):
        v = ck.validate_log(ck.blank_log_csv(), self.T); self.assertTrue(v["ok"]); self.assertEqual(v["rows"], [])
    def test_header_mismatch(self): self.assertFalse(ck.validate_log("a,b\n1,2\n", self.T)["ok"])
    def test_bad_enum_and_date(self):
        v = ck.validate_log(to_csv([row(school="A", channel="fax", touch_date="11/1/26")]), self.T)
        self.assertFalse(v["ok"]); self.assertEqual(len(v["errors"]), 2)
    def test_reply_before_touch(self):
        self.assertFalse(ck.validate_log(to_csv([row(school="A", touch_date="2026-11-05", reply_date="2026-11-01")]), self.T)["ok"])
    def test_future_touch(self):
        self.assertFalse(ck.validate_log(to_csv([row(school="A", touch_date="2026-12-01")]), self.T)["ok"])
    def test_school_required(self):
        self.assertFalse(ck.validate_log(to_csv([row(touch_date="2026-11-01")]), self.T)["ok"])
    def test_due(self):
        d = ck.due_actions([row(school="A", next_date="2026-11-05", next_action="nudge"), row(school="B", next_date="2026-12-01")], self.T)
        self.assertEqual([x["school"] for x in d], ["A"])
    def test_kpis(self):
        rows = [row(school="A", channel="email", touch_date="2026-11-01", parent_copied="yes", reply_type="coach_personal"),
                row(school="B", channel="dm", touch_date="2026-11-02", parent_copied="no", reply_type="none"),
                row(school="C", channel="email", touch_date="2026-09-01", parent_copied="yes", reply_type="staff_generic")]
        k = ck.kpis(rows, 14, self.T)
        self.assertEqual((k["emails_dms_in_window"], k["schools_tracked"], k["replies_any"], k["replies_personal"]), (2, 3, 2, 1))
        self.assertAlmostEqual(k["parent_copied_rate"], 0.667, places=3); self.assertIn("not an outcome", k["label"])
    def test_kpis_empty_no_divzero(self): self.assertEqual(ck.kpis([], 14, self.T)["parent_copied_rate"], 0)

class Deliverables(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp(); build_worksheets.OUT = cls.tmp; cls.files = build_worksheets.build()
    def test_six_worksheets(self):
        for p in "123456": self.assertTrue(any(f.startswith(p + "-") for f in self.files), p)
    def test_no_promise_language_in_any_deliverable(self):
        for f in self.files:
            txt = open(os.path.join(self.tmp, f)).read()
            self.assertEqual(ck.promise_hits(txt), [], f)
    def test_disclaimer_present(self):
        for f in self.files:
            if f.endswith(".md") and not f.startswith("6-follow-log-README"):
                self.assertIn("does not contact coaches", open(os.path.join(self.tmp, f)).read(), f)
    def test_readme_has_disclaimer(self): self.assertIn("does not contact coaches", open(os.path.join(self.tmp, "6-follow-log-README.md")).read())
    def test_csv_valid_blank(self): self.assertTrue(ck.validate_log(open(os.path.join(self.tmp, "6-follow-log.csv")).read(), "2026-11-06")["ok"])
    def test_deterministic(self):
        t2 = tempfile.mkdtemp(); build_worksheets.OUT = t2; build_worksheets.build()
        for f in self.files: self.assertEqual(open(os.path.join(self.tmp, f)).read(), open(os.path.join(t2, f)).read())
        build_worksheets.OUT = self.tmp
    def test_no_personal_data_in_deliverables(self):
        for f in self.files: self.assertNotRegex(open(os.path.join(self.tmp, f)).read(), r"[\w.]+@[\w.]+\.(com|edu)")

class CLI(unittest.TestCase):
    def run_cli(self, *a):
        o, e = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(o), contextlib.redirect_stderr(e): rc = kit_cli.main(list(a))
        return rc, o.getvalue(), e.getvalue()
    def test_script_ok(self):
        sets = []; [sets.extend(["--set", "%s=%s" % kv]) for kv in FIELDS.items()]
        rc, out, _ = self.run_cli("script", "dm_short", *sets); self.assertEqual(rc, 0); self.assertIn("DRAFT ONLY", out)
    def test_script_missing(self):
        rc, _, err = self.run_cli("script", "dm_short", "--set", "coach_last=X"); self.assertEqual(rc, 1); self.assertIn("fill these first", err)
    def test_unknown_template(self): self.assertEqual(self.run_cli("script", "nope")[0], 1)
    def test_link_bad_exit1(self): self.assertEqual(self.run_cli("link", "hello")[0], 1)
    def test_window(self):
        rc, out, _ = self.run_cli("window", "--division", "D1", "--open", "2027-06-15", "--today", "2026-11-06"); self.assertEqual(json.loads(out)["days"], 221)
    def test_logcheck_missing_file(self): self.assertEqual(self.run_cli("log-check", "/nonexistent.csv")[0], 2)
    def test_logcheck_ok(self):
        with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False) as f: f.write(to_csv([row(school="A", channel="email", touch_date="2026-11-01")]))
        rc, out, _ = self.run_cli("log-check", f.name, "--today", "2026-11-06"); self.assertEqual(rc, 0); self.assertIn("kpis", json.loads(out))

if __name__ == "__main__":
    unittest.main(verbosity=1)
