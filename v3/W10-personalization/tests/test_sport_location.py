import unittest
from personalize import personalize
from tests.helpers import *


class SportLocation(unittest.TestCase):
    def ids(self, res):
        return [r["entity_id"] for r in res["ranked"] + res["not_yet_announced"]]

    def test_sport_mismatch_hidden(self):
        res = personalize(profile(sport="hockey"), [row(sport=["football"])], TODAY)
        self.assertEqual(self.ids(res), [])
        self.assertEqual(res["hidden"]["sport_mismatch"], 1)

    def test_exact_beats_multi(self):
        rows = [row(entity_id="multi", sport=["multi"], type="strength_conditioning"),
                row(entity_id="exact", sport=["football"], type="strength_conditioning")]
        res = personalize(profile(), rows, TODAY)
        self.assertEqual([r["entity_id"] for r in res["ranked"]], ["exact", "multi"])

    def test_nearer_ranks_higher_all_else_equal(self):
        rows = [row(entity_id="far", location_coarse={"zip3": "809"}),
                row(entity_id="near", location_coarse={"zip3": "802"})]
        res = personalize(profile(), rows, TODAY)
        self.assertEqual(res["ranked"][0]["entity_id"], "near")

    def test_unknown_zip3_flagged_not_invented(self):
        res = personalize(profile(area="999"), [row()], TODAY)
        it = res["ranked"][0]
        self.assertIn("distance unknown", it["flags"])
        self.assertEqual(it["score_parts"]["geography"], 0)

    def test_row_zip_missing_flagged(self):
        res = personalize(profile(), [row(location_coarse={})], TODAY)
        self.assertIn("distance unknown", res["ranked"][0]["flags"])

    def test_goal_level_filters_types(self):
        res = personalize(profile(goal_level="recreational"), [row(type="college_prospect_camp")], TODAY)
        self.assertEqual(self.ids(res), [])
        self.assertEqual(res["hidden"]["goal_mismatch"], 1)

    def test_grade_mismatch_hidden_and_unknown_kept(self):
        # class of 2028 in Nov 2026 = grade 11
        r1 = row(entity_id="g12only", ages_or_grades={"grades": [12]})
        r2 = row(entity_id="nogrades", ages_or_grades=None)
        res = personalize(profile(), [r1, r2], TODAY)
        self.assertEqual(self.ids(res), ["nogrades"])
        self.assertEqual(res["hidden"]["grade_mismatch"], 1)

    def test_over_budget_flagged_not_dropped(self):
        r = row(price_items=[{"label": "x", "usd": 900, "source_dated": True}])
        res = personalize(profile(budget_band="low"), [r], TODAY)
        self.assertIn("over budget band", res["ranked"][0]["flags"])

    def test_unknown_price_scores_low_but_not_zero(self):
        res = personalize(profile(), [row()], TODAY)
        self.assertEqual(res["ranked"][0]["score_parts"]["cost_clarity"], 4)
        self.assertIn("price unknown", res["ranked"][0]["flags"])

    def test_seed_football_denver_no_hockey(self):
        res = personalize(profile(), seed_rows(), TODAY)
        names = " ".join(r["name"] for r in res["ranked"] + res["not_yet_announced"])
        self.assertNotIn("Hockey", names)
        self.assertNotIn("softball", names.lower())


if __name__ == "__main__":
    unittest.main()
