import json, os, copy
from datetime import date
HERE = os.path.dirname(os.path.abspath(__file__))
SEED = os.path.join(HERE, "..", "data", "rows.seed.json")
TODAY = date(2026, 11, 6)


def seed_rows():
    with open(SEED) as f:
        return json.load(f)["rows"]


def profile(**kw):
    from personalize import parse_intake
    base = {"sport": "football", "class_year": 2028, "area": "802",
            "budget_band": "any", "goal_level": "college_prospect"}
    base.update(kw)
    return parse_intake(base)


def row(**kw):
    r = {"entity_id": "x1", "name": "Test Camp", "type": "camp", "sport": ["football"],
         "ages_or_grades": None, "location_coarse": {"zip3": "802"}, "who_runs": "college",
         "price_items": [], "dates": [{"start": "2027-03-01", "end": "2027-03-01"}],
         "url": "https://example.invalid/x", "read_on": "2026-11-05", "reader": "t",
         "field_labels": {"overall": "listed"}, "credential_checks": [], "status": "active"}
    r.update(kw)
    return copy.deepcopy(r)
