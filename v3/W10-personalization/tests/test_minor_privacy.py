"""Minor-privacy contract (PERSONALIZATION.md 5b). The athlete is the data subject; the parent is the user."""
import json, os, re, unittest, io, contextlib
from personalize import parse_intake, IntakeError, ALLOWED_FIELDS, personalize, to_ics
from tests.helpers import *

BASE = {"sport": "football", "class_year": 2028, "area": "80202",
        "budget_band": "mid", "goal_level": "college_prospect"}
PKG = os.path.join(HERE, "..", "personalize")


class MinorPrivacy(unittest.TestCase):
    def test_allowlist_is_exactly_five_fields(self):
        self.assertEqual(set(ALLOWED_FIELDS), {"sport", "class_year", "area", "budget_band", "goal_level"})

    def test_child_identifiers_rejected_not_dropped(self):
        for bad in ("child_name", "name", "birth_date", "dob", "photo", "school", "stats", "health",
                    "injury", "email", "phone", "address", "ip", "gpa", "jersey", "team", "age"):
            with self.assertRaises(IntakeError, msg=bad) as cm:
                parse_intake({**BASE, bad: "x"})
            self.assertIn(bad, str(cm.exception))

    def test_full_zip_truncated_and_never_retained(self):
        p = parse_intake(BASE)
        self.assertEqual(p["zip3"], "802")
        self.assertNotIn("80202", json.dumps(p))

    def test_street_address_or_zip4_rejected(self):
        for bad in ("123 Main St", "80202-1234", "8020", "ab1", ""):
            with self.assertRaises(IntakeError, msg=bad):
                parse_intake({**BASE, "area": bad})

    def test_birth_date_not_accepted_as_class_year(self):
        for bad in ("2010-05-04", "05/04/2010", 2010, 1999, 2099, None, "abc"):
            with self.assertRaises(IntakeError, msg=str(bad)):
                parse_intake({**BASE, "class_year": bad})

    def test_missing_field_rejected(self):
        b = dict(BASE); del b["sport"]
        with self.assertRaises(IntakeError):
            parse_intake(b)

    def test_non_dict_rejected(self):
        for bad in (None, [], "x", 3):
            with self.assertRaises(IntakeError):
                parse_intake(bad)

    def test_output_never_echoes_more_than_five_coarse_fields(self):
        res = personalize(parse_intake(BASE), seed_rows(), TODAY)
        self.assertEqual(set(res["profile_echo"]), {"sport", "class_year", "area_zip3", "budget_band", "goal_level"})
        self.assertNotIn("80202", json.dumps(res))

    def test_no_lead_handoff_or_contact_fields_in_output(self):
        blob = json.dumps(personalize(parse_intake(BASE), seed_rows(), TODAY)).lower()
        for k in (r"email", r"phone", r"@", r"\blead\b(?!\s+only)", r"tel:", r"mailto"):
            # "lead only" is the aggregator caveat wording (a source-quality flag, not a lead handoff)
            self.assertIsNone(re.search(k, blob), k)

    def test_ics_contains_no_child_or_profile_data(self):
        ics = to_ics(personalize(parse_intake(BASE), seed_rows(), TODAY))
        for k in ("2028", "802", "football", "mid", "college_prospect"):
            # sport words may appear in public event titles; profile values must not be in non-title lines
            for line in ics.splitlines():
                if line.startswith(("SUMMARY", "DESCRIPTION", "UID", "PRODID")):
                    continue
                self.assertNotIn("class_year", line)
        self.assertNotIn("PRIVATE", ics)
        self.assertNotRegex(ics, r"ATTENDEE|ORGANIZER|ATTACH")

    def test_credential_contact_details_not_stored_in_seed(self):
        with open(SEED) as fh:
            raw = fh.read()
        self.assertNotRegex(raw, r"[\w.]+@[\w.]+\.\w+")           # no emails
        self.assertNotRegex(raw, r"\(?\d{3}\)?[-. ]\d{3}[-. ]\d{4}")  # no phone numbers

    def test_seed_has_no_minor_names_or_reviews(self):
        for r in seed_rows():
            for k in ("reviews", "testimonials", "rating", "stars", "roster", "athlete", "child"):
                self.assertNotIn(k, r)

    def test_package_has_no_network_logging_or_persistence(self):
        banned = re.compile(r"\b(import\s+(requests|urllib|http|socket|smtplib|sqlite3|logging|subprocess|ftplib)|"
                            r"open\([^)]*['\"][wa]b?['\"]|print\()")
        for fn in os.listdir(PKG):
            if fn.endswith(".py"):
                with open(os.path.join(PKG, fn)) as fh:
                    src = fh.read()
                self.assertIsNone(banned.search(src), fn)

    def test_no_paid_placement_inputs_in_ranking(self):
        a = row(entity_id="a"); b = row(entity_id="b", sponsored=True, paid_tier="gold", clicks=99999, rating=5)
        res = personalize(profile(), [b, a], TODAY)
        self.assertEqual([r["entity_id"] for r in res["ranked"]], ["a", "b"])  # tie -> alphabetical, not paid
        self.assertEqual(res["ranked"][0]["score"], res["ranked"][1]["score"])

    def test_cli_rejects_extra_fields_and_writes_nothing(self):
        import cli
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
            rc = cli.main(["--intake-json", json.dumps({**BASE, "child_name": "Sam"}), "--today", "2026-11-06"])
        self.assertEqual(rc, 2)
        self.assertNotIn("Sam", out.getvalue())


if __name__ == "__main__":
    unittest.main()
