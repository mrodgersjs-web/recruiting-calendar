"""Intake: the ONLY place parent input enters. Allowlist of five fields (PERSONALIZATION.md 5b, 8).

Privacy contract (minors): no child name, birth date, photo, school, stats, health data, street
address, or full ZIP. Any extra key is REJECTED (not silently dropped) so a caller bug can never
smuggle child identifiers into storage or logs.
"""
import re

ALLOWED_FIELDS = ("sport", "class_year", "area", "budget_band", "goal_level")
SPORTS = {"football", "basketball", "baseball", "softball", "hockey", "volleyball",
          "soccer", "lacrosse", "track", "wrestling", "swimming", "tennis", "golf"}
BUDGET_BANDS = {"free": 0, "low": 150, "mid": 400, "high": 1000, "any": None}  # max usd per item
GOAL_LEVELS = {"recreational", "development", "college_prospect"}
# Types allowed per goal level (hard filter, not a score).
GOAL_TYPES = {
    "recreational": {"recreational_league", "camp"},
    "development": {"recreational_league", "camp", "strength_conditioning", "mental_performance"},
    "college_prospect": {"college_prospect_camp", "showcase", "camp", "strength_conditioning",
                         "mental_performance"},
}


class IntakeError(ValueError):
    pass


def _zip3(area):
    """Accept ONLY a 3-digit prefix, or a 5-digit ZIP which is immediately truncated to 3."""
    s = str(area).strip()
    if re.fullmatch(r"\d{3}", s):
        return s
    if re.fullmatch(r"\d{5}", s):
        return s[:3]  # full ZIP is never retained
    raise IntakeError("area must be a 3-digit ZIP prefix (a 5-digit ZIP is truncated to 3)")


def parse_intake(raw, today_year=2026):
    if not isinstance(raw, dict):
        raise IntakeError("intake must be an object")
    extra = sorted(set(raw) - set(ALLOWED_FIELDS))
    if extra:
        raise IntakeError("disallowed intake field(s): %s (minimum-data rule: only %s)"
                          % (", ".join(extra), ", ".join(ALLOWED_FIELDS)))
    missing = [f for f in ALLOWED_FIELDS if f not in raw]
    if missing:
        raise IntakeError("missing intake field(s): %s" % ", ".join(missing))
    sport = str(raw["sport"]).strip().lower()
    if sport not in SPORTS:
        raise IntakeError("unsupported sport %r" % sport)
    try:
        cy = int(raw["class_year"])
    except (TypeError, ValueError):
        raise IntakeError("class_year must be a graduation year (not a birth date)")
    if not (today_year <= cy <= today_year + 12):
        raise IntakeError("class_year out of range (%d..%d)" % (today_year, today_year + 12))
    band = str(raw["budget_band"]).strip().lower()
    if band not in BUDGET_BANDS:
        raise IntakeError("budget_band must be one of %s" % sorted(BUDGET_BANDS))
    goal = str(raw["goal_level"]).strip().lower()
    if goal not in GOAL_LEVELS:
        raise IntakeError("goal_level must be one of %s" % sorted(GOAL_LEVELS))
    return {"sport": sport, "class_year": cy, "zip3": _zip3(raw["area"]),
            "budget_band": band, "budget_max_usd": BUDGET_BANDS[band], "goal_level": goal}


def grade_for(class_year, today=(2026, 11)):
    """Approx. current grade from graduation year. Nov 2026: class of 2027 = grade 12."""
    school_year_end = today[0] + (1 if today[1] >= 8 else 0)
    g = 12 - (class_year - school_year_end)
    return g
