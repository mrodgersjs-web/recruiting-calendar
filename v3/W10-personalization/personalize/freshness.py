"""Freshness gate (PERSONALIZATION.md 4 rule 4, 6a step 7, 6b hard filters).

States: bookable | past | tbd | stale | unknown_date.
  - past: every dated window ended before today. Hard-hidden.
  - tbd: provider says no date yet (status tbd or no dates). Shown separately, never guessed.
  - stale: row not re-read inside its window. Drops from default results.
  - A read_on date in the FUTURE or unparseable is treated as stale (cannot be trusted), never fresh.
"""
from datetime import date, timedelta

PRICE_RECHECK_DAYS = 90      # quarterly
EVENT_NEAR_DAYS = 60         # weekly re-read inside 60 days of the event
EVENT_FAR_RECHECK = 7        # weekly when near
EVENT_NEAR_WINDOW = 30       # monthly otherwise
PROVIDER_RECHECK_DAYS = 90


def _d(s):
    try:
        return date.fromisoformat(s)
    except (TypeError, ValueError):
        return None


def recheck_window_days(row, today):
    """Days a read stays valid. Events: 7 inside 60 days of start, else 30. Others: 90."""
    if row.get("type") in ("college_prospect_camp", "showcase", "camp", "recreational_league"):
        starts = [_d(x.get("start")) for x in row.get("dates", [])]
        starts = [s for s in starts if s]
        if starts and 0 <= (min(starts) - today).days <= EVENT_NEAR_DAYS:
            return EVENT_FAR_RECHECK
        return EVENT_NEAR_WINDOW
    return PROVIDER_RECHECK_DAYS


def row_state(row, today):
    """Return (state, reason). Order matters: past > stale > tbd > bookable."""
    dates = row.get("dates") or []
    ends = [_d(x.get("end") or x.get("start")) for x in dates]
    ends = [e for e in ends if e]
    if dates and ends and all(e < today for e in ends):
        return "past", "all dated windows ended before %s" % today.isoformat()
    if row.get("status") == "past":
        return "past", "row marked past"
    read_on = _d(row.get("read_on"))
    if read_on is None:
        return "stale", "read_on missing or unparseable"
    if read_on > today:
        return "stale", "read_on is in the future; cannot be trusted"
    age = (today - read_on).days
    window = recheck_window_days(row, today)
    if age > window:
        return "stale", "not recently checked (%d days old, window %d)" % (age, window)
    is_event = row.get("type") in ("college_prospect_camp", "showcase", "camp", "recreational_league")
    if row.get("status") == "tbd" or (is_event and not ends):
        return "tbd", "Not yet announced"
    if row.get("status") in ("stale",):
        return "stale", "row marked stale"
    return "bookable", "read %d days ago, window %d" % (age, window)
