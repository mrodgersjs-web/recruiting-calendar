import unittest
from datetime import date
from personalize import personalize, row_state, recheck_window_days, to_ics
from tests.helpers import *


class Provenance(unittest.TestCase):
    def test_missing_url_or_read_on_never_shown(self):
        for bad in (row(url=""), row(read_on=""), row(entity_id="")):
            res = personalize(profile(), [bad], TODAY)
            self.assertEqual(res["ranked"] + res["not_yet_announced"], [])
            self.assertEqual(res["hidden"]["malformed"], 1)

    def test_non_dict_rows_do_not_crash(self):
        res = personalize(profile(), [None, "x", 3], TODAY)
        self.assertEqual(res["hidden"]["malformed"], 3)

    def test_every_shown_row_has_label_url_readon(self):
        res = personalize(profile(), seed_rows(), TODAY)
        for it in res["ranked"] + res["not_yet_announced"]:
            self.assertTrue(it["url"].startswith("http"))
            self.assertRegex(it["read_on"], r"^\d{4}-\d{2}-\d{2}$")
            self.assertIn(it["highest_label"], {"listed", "observed", "verified"})

    def test_vetted_and_endorsed_downgraded_in_pilot(self):
        r = row(field_labels={"overall": "endorsed", "x": "vetted"})
        res = personalize(profile(), [r], TODAY)
        self.assertEqual(res["ranked"][0]["highest_label"], "listed")

    def test_verified_requires_credential_check_for_score(self):
        plain = personalize(profile(), [row(type="mental_performance", field_labels={"overall": "verified"})], TODAY)
        chk = row(type="mental_performance", field_labels={"overall": "verified"},
                  credential_checks=[{"person": "p", "issuer": "AASP", "credential": "CMPC", "status": "verified"}])
        withc = personalize(profile(), [chk], TODAY)
        self.assertLess(plain["ranked"][0]["score_parts"]["verifiability"],
                        withc["ranked"][0]["score_parts"]["verifiability"])

    def test_aggregator_flagged_and_loses_tiebreak(self):
        a = row(entity_id="agg", source_is_aggregator=True)
        b = row(entity_id="prim")
        res = personalize(profile(), [a, b], TODAY)
        self.assertEqual(res["ranked"][0]["entity_id"], "prim")
        agg = [r for r in res["ranked"] if r["entity_id"] == "agg"][0]
        self.assertIn("aggregator source: lead only, dates not verified", agg["flags"])

    def test_banned_health_claims_withheld(self):
        r = row(name="Injury prevention and safe medically supervised training")
        res = personalize(profile(), [r], TODAY)
        self.assertIn("claim withheld", res["ranked"][0]["name"])

    def test_provider_rows_carry_safeguarding_questions_not_answers(self):
        r = row(type="strength_conditioning", sport=["multi"])
        res = personalize(profile(goal_level="development"), [r], TODAY)
        it = res["ranked"][0]
        self.assertEqual(len(it["safeguarding_questions"]), 5)
        self.assertIn("not collected", it["safeguarding_status"])
        self.assertNotIn("safe", it["safeguarding_status"].replace("safeguarding", ""))


class Freshness(unittest.TestCase):
    def test_past_event_hidden(self):
        res = personalize(profile(), [row(dates=[{"start": "2026-06-30", "end": "2026-06-30"}])], TODAY)
        self.assertEqual(res["hidden"]["past"], 1)
        self.assertEqual(res["ranked"], [])

    def test_event_ending_today_is_not_past(self):
        s, _ = row_state(row(dates=[{"start": "2026-11-06", "end": "2026-11-06"}]), TODAY)
        self.assertEqual(s, "bookable")

    def test_status_past_without_dates_hidden(self):
        s, _ = row_state(row(dates=[], status="past"), TODAY)
        self.assertEqual(s, "past")

    def test_no_date_event_goes_to_tbd_never_ranked(self):
        res = personalize(profile(), [row(dates=[], status="tbd")], TODAY)
        self.assertEqual(res["ranked"], [])
        self.assertEqual(res["not_yet_announced"][0]["entity_id"], "x1")

    def test_event_without_dates_but_active_is_still_tbd(self):
        s, why = row_state(row(dates=[], status="active"), TODAY)
        self.assertEqual((s, why), ("tbd", "Not yet announced"))

    def test_stale_event_near_date_weekly_window(self):
        r = row(dates=[{"start": "2026-12-15", "end": "2026-12-15"}], read_on="2026-10-20")  # 17d old, window 7
        s, why = row_state(r, TODAY)
        self.assertEqual(s, "stale")
        self.assertIn("not recently checked", why)
        self.assertEqual(recheck_window_days(r, TODAY), 7)

    def test_far_event_monthly_window(self):
        r = row(dates=[{"start": "2027-08-01", "end": "2027-08-01"}], read_on="2026-10-20")
        self.assertEqual(row_state(r, TODAY)[0], "bookable")
        self.assertEqual(recheck_window_days(r, TODAY), 30)

    def test_provider_quarterly(self):
        r = row(type="strength_conditioning", dates=[], read_on="2026-08-10")  # 88d
        self.assertEqual(row_state(r, TODAY)[0], "bookable")
        r2 = row(type="strength_conditioning", dates=[], read_on="2026-07-01")  # 128d
        self.assertEqual(row_state(r2, TODAY)[0], "stale")

    def test_future_or_garbage_read_on_is_stale(self):
        self.assertEqual(row_state(row(read_on="2027-01-01"), TODAY)[0], "stale")
        self.assertEqual(row_state(row(read_on="yesterday"), TODAY)[0], "stale")

    def test_stale_hidden_by_default_listed_when_asked(self):
        r = row(read_on="2026-01-01")
        self.assertEqual(personalize(profile(), [r], TODAY)["ranked"], [])
        res = personalize(profile(), [r], TODAY, include_stale=True)
        self.assertEqual(res["stale_rows"][0]["entity_id"], "x1")
        self.assertEqual(res["ranked"], [])

    def test_window_dates_flagged(self):
        r = row(dates=[{"start": "2027-06-01", "end": "2027-06-29", "is_window": True}])
        self.assertIn("date is a window, not a confirmed day", personalize(profile(), [r], TODAY)["ranked"][0]["flags"])

    def test_seed_freshness_matches_w7_finding(self):
        # W7: past/tbd rows must not be bookable. Junior Day (past) hidden; Mines (tbd) separated.
        res = personalize(profile(), seed_rows(), TODAY)
        ranked = {r["entity_id"] for r in res["ranked"]}
        tbd = {r["entity_id"] for r in res["not_yet_announced"]}
        self.assertNotIn("event-juniorday-ponderosa-2026", ranked | tbd)
        self.assertIn("event-mines-camps", tbd)
        self.assertNotIn("event-mines-camps", ranked)
        self.assertGreaterEqual(res["hidden"]["past"], 1)

    def test_seed_goes_stale_a_month_later(self):
        res = personalize(profile(), seed_rows(), date(2027, 3, 1))
        self.assertEqual(res["ranked"], [])
        self.assertEqual(res["not_yet_announced"], [])
        self.assertGreater(res["hidden"]["stale"], 0)

    def test_ics_only_ranked_dated_items(self):
        r1 = row(entity_id="a", dates=[{"start": "2027-03-01", "end": "2027-03-02"}])
        r2 = row(entity_id="b", dates=[], status="tbd")
        ics = to_ics(personalize(profile(), [r1, r2], TODAY))
        self.assertEqual(ics.count("BEGIN:VEVENT"), 1)
        self.assertIn("DTEND;VALUE=DATE:20270303", ics)
        self.assertIn("UID:a-0@w10.invalid", ics)
        self.assertNotIn("UID:b", ics)


if __name__ == "__main__":
    unittest.main()
