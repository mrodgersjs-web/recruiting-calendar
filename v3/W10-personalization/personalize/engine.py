"""Rule-based personalization. Transparent, no paid placement, no outcome claims (PERSONALIZATION.md 6b).

Hard filters (not scores): past events, sport mismatch, grade mismatch, goal-type mismatch.
Scores: fit 0-40, geography 0-20, cost clarity 0-15, verifiability 0-15, freshness 0-10.
Unknown is flagged and scored low, never zero-by-fiat and never guessed upward.
Empty/absent data yields an explicit empty result with a reason, never a fabricated row.
"""
from datetime import date
from . import freshness, geo
from .intake import GOAL_TYPES, grade_for

LABEL_RANK = {"listed": 1, "observed": 2, "verified": 3, "vetted": 4, "endorsed": 5}
# The pilot may honestly claim only these (PERSONALIZATION.md 0). Anything else is downgraded.
PILOT_LABELS = {"listed", "observed", "verified"}
DISCLOSURE = ("Ranked by fit, location, cost clarity, checkability and freshness. "
              "Not by who pays us.")
STANDING_NOTES = ["Not medical advice.", "We have not verified safety.",
                  "Mental performance consulting is not a substitute for medical or mental-health care."]
BANNED_CLAIM_WORDS = ("safe", "medically supervised", "prevents injury", "injury prevention",
                      "treats", "cures", "guaranteed", "reduces anxiety", "improves mental health")
PROVIDER_TYPES = {"strength_conditioning", "mental_performance"}
SAFEGUARDING_QUESTIONS = [
    "Do all coaches get a background check from a consumer reporting agency?",
    "Is annual mandatory-reporter training completed this year?",
    "Is a written prohibited-conduct / one-on-one interaction policy available?",
    "Is a first-aid/CPR/AED-certified adult present?",
    "Which named coach will work with my child, and what credential number can I check?",
]


def highest_label(row):
    """Highest label we can actually support, capped to pilot-available labels."""
    labels = set((row.get("field_labels") or {}).values())
    labels &= PILOT_LABELS
    if not labels:
        return "listed"
    return max(labels, key=LABEL_RANK.get)


def _sport_match(row, sport):
    sports = [s.lower() for s in (row.get("sport") or [])]
    if sport in sports:
        return "exact"
    if "multi" in sports:
        return "multi"
    return None


def _grade_match(row, grade, class_year):
    ag = row.get("ages_or_grades")
    if not ag:
        return "unknown"
    if "grades" in ag:
        return "match" if grade in ag["grades"] else "mismatch"
    if "age_min" in ag:
        approx_age = grade + 5  # grade 12 ~ age 17-18; coarse by design, no birth date held
        return "match" if ag["age_min"] <= approx_age <= ag["age_max"] + 1 else "mismatch"
    if "birth_years" in ag:
        lo, hi = ag["birth_years"]
        by = class_year - 18  # class of 2027 ~ born 2009
        return "match" if lo <= by <= hi else "mismatch"
    return "unknown"


def _cost(row, budget_max):
    items = row.get("price_items") or []
    if not items:
        return "unknown", 4   # unknown scores low, not zero, and is flagged
    usd = min(i["usd"] for i in items)
    if budget_max is None or usd <= budget_max:
        return "within", 15
    return "over", 0


def _verif(row):
    checks = [c for c in row.get("credential_checks") or [] if c.get("status") == "verified"]
    if checks:
        return 15
    return 3 if row.get("field_labels", {}).get("overall") == "observed" else 2


def _fresh_score(row, today):
    ro = freshness._d(row.get("read_on"))
    if ro is None or ro > today:
        return 0
    age = (today - ro).days
    return 10 if age <= 7 else 7 if age <= 30 else 3


def _clean(text):
    """Defensive: never emit our own banned health/outcome words from row-derived text."""
    out = text or ""
    low = out.lower()
    for w in BANNED_CLAIM_WORDS:
        if w in low:
            return "[claim withheld: provider text contained a restricted health/outcome claim]"
    return out


def personalize(profile, rows, today=None, include_stale=False):
    """profile: output of parse_intake. rows: list of row dicts (may be empty/None)."""
    today = today or date.today()
    rows = rows or []
    grade = grade_for(profile["class_year"], (today.year, today.month))
    result = {"disclosure": DISCLOSURE, "standing_notes": STANDING_NOTES,
              "as_of": today.isoformat(), "ranked": [], "not_yet_announced": [],
              "hidden": {"past": 0, "stale": 0, "sport_mismatch": 0, "grade_mismatch": 0,
                         "goal_mismatch": 0, "malformed": 0},
              "stale_rows": [], "empty_reason": None, "profile_echo": {
                  "sport": profile["sport"], "class_year": profile["class_year"],
                  "area_zip3": profile["zip3"], "budget_band": profile["budget_band"],
                  "goal_level": profile["goal_level"]}}
    if not rows:
        result["empty_reason"] = "No rows loaded. Nothing is shown rather than guessing."
        return result
    allowed_types = GOAL_TYPES[profile["goal_level"]]
    for row in rows:
        if not isinstance(row, dict) or not row.get("entity_id") or not row.get("url") \
                or not row.get("read_on"):
            result["hidden"]["malformed"] += 1   # no provenance => cannot be shown
            continue
        state, why = freshness.row_state(row, today)
        if state == "past":
            result["hidden"]["past"] += 1
            continue
        if state == "stale":
            result["hidden"]["stale"] += 1
            if include_stale:
                result["stale_rows"].append({"entity_id": row["entity_id"], "reason": why})
            continue
        sm = _sport_match(row, profile["sport"])
        if sm is None:
            result["hidden"]["sport_mismatch"] += 1
            continue
        if row.get("type") not in allowed_types:
            result["hidden"]["goal_mismatch"] += 1
            continue
        gm = _grade_match(row, grade, profile["class_year"])
        if gm == "mismatch":
            result["hidden"]["grade_mismatch"] += 1
            continue
        miles = geo.miles(profile["zip3"], row.get("location_coarse", {}).get("zip3"))
        fit = (22 if sm == "exact" else 14) + (10 if gm == "match" else 4) + \
              (8 if row.get("type") in allowed_types else 0)
        geo_s = 0 if miles is None else 20 if miles <= 15 else 14 if miles <= 40 else 7 if miles <= 100 else 2
        cost_state, cost_s = _cost(row, profile["budget_max_usd"])
        if cost_state == "over":
            pass  # shown but flagged; budget is a score input, not a hard filter (spec 6b)
        verif = _verif(row)
        fresh = _fresh_score(row, today)
        total = min(40, fit) + geo_s + cost_s + verif + fresh
        primary_bonus = 0 if row.get("source_is_aggregator") else 1  # tie-breaker only
        item = {
            "entity_id": row["entity_id"], "name": _clean(row.get("name")), "type": row["type"],
            "score": total, "tiebreak": primary_bonus,
            "score_parts": {"fit": min(40, fit), "geography": geo_s, "cost_clarity": cost_s,
                            "verifiability": verif, "freshness": fresh},
            "reasons": ["sport: %s" % sm, "grade: %s" % gm,
                        "distance: %s" % ("unknown" if miles is None else "%s mi straight-line (%s)" % (miles, geo.band(miles))),
                        "cost: %s" % cost_state, "freshness: %s" % why],
            "highest_label": highest_label(row), "read_on": row["read_on"], "url": row["url"],
            "who_runs": row.get("who_runs"), "state": state, "flags": [],
            "dates": row.get("dates") or [],
            "safeguarding": ("questions_for_parent" if row.get("type") in PROVIDER_TYPES else None),
        }
        if row.get("type") in PROVIDER_TYPES:
            item["safeguarding_questions"] = SAFEGUARDING_QUESTIONS
            item["safeguarding_status"] = "not collected (no outreach); self-reported until a document is seen"
        if cost_state == "unknown":
            item["flags"].append("price unknown")
        if cost_state == "over":
            item["flags"].append("over budget band")
        if miles is None:
            item["flags"].append("distance unknown")
        if row.get("source_is_aggregator"):
            item["flags"].append("aggregator source: lead only, dates not verified")
        if any(d.get("is_window") for d in (row.get("dates") or [])):
            item["flags"].append("date is a window, not a confirmed day")
        (result["not_yet_announced"] if state == "tbd" else result["ranked"]).append(item)
    result["ranked"].sort(key=lambda r: (-r["score"], -r["tiebreak"], r["entity_id"]))
    result["not_yet_announced"].sort(key=lambda r: r["entity_id"])
    if not result["ranked"] and not result["not_yet_announced"]:
        result["empty_reason"] = ("No rows match this sport/grade/goal after the freshness gate. "
                                  "Nothing is invented to fill the list.")
    return result
