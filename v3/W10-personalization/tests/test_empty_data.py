import unittest
from personalize import personalize, to_ics
from tests.helpers import *


class EmptyData(unittest.TestCase):
    def test_none_and_empty_list(self):
        for rows in (None, []):
            res = personalize(profile(), rows, TODAY)
            self.assertEqual(res["ranked"], [])
            self.assertEqual(res["not_yet_announced"], [])
            self.assertIn("No rows loaded", res["empty_reason"])
            self.assertEqual(res["disclosure"].startswith("Ranked by fit"), True)

    def test_everything_filtered_gives_reason_not_filler(self):
        # golf has no sport-specific seed rows; multi-sport providers legitimately remain
        res = personalize(profile(sport="golf"), seed_rows(), TODAY)
        shown = res["ranked"] + res["not_yet_announced"]
        self.assertTrue(all(r["type"] in ("strength_conditioning", "mental_performance") for r in shown))
        # all events filtered; with only events loaded the result is empty WITH a reason
        events = [r for r in seed_rows() if r["type"] not in ("strength_conditioning", "mental_performance")]
        res2 = personalize(profile(sport="golf"), events, TODAY)
        self.assertEqual(res2["ranked"] + res2["not_yet_announced"], [])
        self.assertIn("Nothing is invented", res2["empty_reason"])

    def test_empty_result_ics_is_valid_and_has_no_events(self):
        ics = to_ics(personalize(profile(), [], TODAY))
        self.assertTrue(ics.startswith("BEGIN:VCALENDAR"))
        self.assertTrue(ics.rstrip().endswith("END:VCALENDAR"))
        self.assertEqual(ics.count("VEVENT"), 0)

    def test_row_with_all_optional_fields_missing(self):
        minimal = {"entity_id": "m", "url": "https://example.invalid", "read_on": "2026-11-05",
                   "type": "camp", "sport": ["football"]}
        res = personalize(profile(), [minimal], TODAY)
        self.assertEqual(res["not_yet_announced"][0]["entity_id"], "m")  # no dates => tbd
        self.assertIn("price unknown", res["not_yet_announced"][0]["flags"])

    def test_disclosures_present_even_when_empty(self):
        res = personalize(profile(), [], TODAY)
        self.assertIn("Not medical advice.", res["standing_notes"])
        self.assertIn("We have not verified safety.", res["standing_notes"])

    def test_missing_dates_key_does_not_crash(self):
        r = row(); del r["dates"]
        personalize(profile(), [r], TODAY)

    def test_no_provider_names_when_data_empty(self):
        import json
        res = json.dumps(personalize(profile(), [], TODAY))
        for name in ("Redline", "SOMA", "Landow", "Gold Crown"):
            self.assertNotIn(name, res)


if __name__ == "__main__":
    unittest.main()
