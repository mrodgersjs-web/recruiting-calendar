"""W10 personalization prototype. Isolated: stdlib only, no network, no shared-site imports."""
from .intake import parse_intake, IntakeError, ALLOWED_FIELDS
from .freshness import row_state, recheck_window_days
from .engine import personalize
from .ics import to_ics

__all__ = ["parse_intake", "IntakeError", "ALLOWED_FIELDS", "row_state",
           "recheck_window_days", "personalize", "to_ics"]
