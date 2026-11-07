#!/usr/bin/env python3
"""Coach Contact Kit core (W10-access). Stdlib only. NO network, NO sending.

Everything here is local text/date logic a family runs itself. Nothing in this
module contacts a coach, fetches a URL, or stores an athlete's personal data.
Source: v3/W7-access/ACCESS.md (sections 2a, 2c, 2d, 4, 8, 9).
"""
import csv, datetime as dt, io, json, re, sys
from urllib.parse import urlparse

# ---- Banned promise language (ACCESS.md section 7, risk 1) -------------------
PROMISE_PATTERNS = [
    r"\bguarantee[sd]?\b", r"\bguaranteed\b", r"\bwe (will )?(get|land|secure)\b",
    r"\bintroduc(e|tion)s? (you )?to (college )?coaches\b", r"\baccess to \d[\d,]* coaches\b",
    r"\bget(s)? you (a |an )?(offer|scholarship|reply|spot)\b", r"\b\d{2,3}% of (athletes|prospects)\b",
    r"\b(we|our team) (will )?(contact|email|message|dm) (the )?coaches?\b",
    r"\bfull[- ]ride\b", r"\bplaced? (at|with|on)\b",
]
_PROMISE_RE = [re.compile(p, re.I) for p in PROMISE_PATTERNS]

def promise_hits(text):
    """Return list of matched banned-promise phrases in text (empty = clean)."""
    hits = []
    for rx in _PROMISE_RE:
        m = rx.search(text or "")
        if m:
            hits.append(m.group(0))
    return hits

# ---- Division contact rules (generic; dates come from the family's own sheet) --
DIVISION_NOTES = {
    "D1": "Family may write any time. Coach replies/calls/DMs are limited by the NCAA sport calendar; read the date for your sport and class year.",
    "D2": "Coaches may call, text and email any time per the sources in ACCESS.md 2a; verify with the NCAA page.",
    "D3": "Almost no timing limits per ACCESS.md 2a; verify with the NCAA page.",
    "NAIA": "No recruiting calendar and no limit on communication (naia.org/why-naia/recruiting).",
}

def parse_date(s):
    return dt.date.fromisoformat(s)

def send_window(division, class_year_open_iso, today_iso, verified_on_iso=None, max_age_days=60):
    """Tell a family where they stand relative to a coach-reply date THEY entered.

    class_year_open_iso: the first date coaches may reply for the family's sport,
    copied by the family from the NCAA sport calendar (or None for D2/D3/NAIA).
    Returns dict(status, days, note, stale_warning). Never invents a date.
    """
    division = (division or "").upper()
    if division not in DIVISION_NOTES:
        raise ValueError("division must be one of %s" % sorted(DIVISION_NOTES))
    today = parse_date(today_iso)
    out = {"division": division, "note": DIVISION_NOTES[division], "family_may_write": True,
           "status": "no_calendar_date_needed", "days": None, "stale_warning": None}
    if verified_on_iso:
        age = (today - parse_date(verified_on_iso)).days
        if age > max_age_days:
            out["stale_warning"] = "Your date was checked %d days ago. Re-read the NCAA sport calendar." % age
    if division == "D1":
        if not class_year_open_iso:
            out["status"] = "date_missing"
            out["note"] += " You have not entered the date yet: copy it from the NCAA sport calendar."
            return out
        opened = parse_date(class_year_open_iso)
        out["days"] = (opened - today).days
        out["status"] = "coaches_may_reply" if out["days"] <= 0 else "coaches_may_not_reply_yet"
    return out

# ---- Highlight link checklist (offline: shape checks only, no fetching) -----
HOSTS_OK = {"youtube.com": "youtube", "www.youtube.com": "youtube", "m.youtube.com": "youtube",
            "youtu.be": "youtube", "vimeo.com": "vimeo", "www.vimeo.com": "vimeo",
            "hudl.com": "hudl", "www.hudl.com": "hudl", "fan.hudl.com": "hudl"}

def check_video_link(url, minutes=None, title=None, first_30_best=None, tested_private_window=None):
    """Offline checklist. Returns dict(ok, host, problems[], reminders[]).
    Does NOT fetch the URL (ACCESS.md section 8 item 4: client-side first)."""
    problems, reminders = [], []
    u = urlparse((url or "").strip())
    if u.scheme not in ("http", "https") or not u.netloc:
        return {"ok": False, "host": None, "problems": ["Not a web link (needs https://...)"], "reminders": []}
    if u.scheme == "http":
        problems.append("Use https:// not http://")
    host = u.netloc.lower().split(":")[0]
    kind = HOSTS_OK.get(host)
    if not kind:
        reminders.append("Host not YouTube/Vimeo/Hudl: make sure a coach can click it with no login.")
    if kind == "youtube":
        reminders.append("Visibility must be Unlisted or Public. 'Private' does not open for coaches.")
        reminders.append("Choose 'No, it's not made for kids' in YouTube settings; see YouTube help 9632097.")
    if kind == "hudl":
        reminders.append("Hudl share links must be public: open it in a private window.")
    if kind == "vimeo":
        reminders.append("Check Vimeo privacy lets anyone with the link view; test on a phone.")
    if re.search(r"\.(mp4|mov|avi|zip)$", u.path, re.I):
        problems.append("Looks like a file, not a link. Coaches do not open attachments.")
    if minutes is not None and not (3 <= minutes <= 5):
        problems.append("Length %s min: aim for 3 to 5 minutes." % minutes)
    if first_30_best is False:
        problems.append("Put your best clips in the first 30 seconds.")
    if tested_private_window is False:
        problems.append("Open the link in a private/incognito window to confirm it plays without login.")
    if title is not None:
        if not re.search(r"(19|20)\d{2}|class of", title, re.I) or len(title.split()) < 3:
            problems.append("Title should carry name, class year, sport and position.")
    return {"ok": not problems, "host": host, "problems": problems, "reminders": reminders}

# ---- Script templates (athlete voice; parent copied; NEVER sent by us) -------
# Each template is a draft the athlete edits and sends from their own account.
TEMPLATES = {
    "intro_email": {
        "subject": "{sport} {position}, Class of {class_year}: {athlete_name}",
        "body": ("Coach {coach_last},\n\n"
                 "My name is {athlete_name}. I play {position} for {team} and I am in the Class of {class_year}. "
                 "I am writing because {specific_reason}.\n\n"
                 "My highlight link: {video_url}\n"
                 "{stat_line}\n"
                 "I filled out your recruiting questionnaire on {questionnaire_date}. "
                 "If there is anything else you would like from me, I will send it.\n\n"
                 "Thank you for your time.\n{athlete_name}\n{athlete_phone_or_email}\n"
                 "(My parent is copied on this email.)"),
        "needs": ["coach_last", "athlete_name", "sport", "position", "team", "class_year",
                  "specific_reason", "video_url", "stat_line", "questionnaire_date", "athlete_phone_or_email"],
    },
    "dm_short": {
        "subject": "",
        "body": ("Coach {coach_last}, I am {athlete_name}, {position}, Class of {class_year}. "
                 "{specific_reason}. Highlights: {video_url}. Thank you for your time."),
        "needs": ["coach_last", "athlete_name", "position", "class_year", "specific_reason", "video_url"],
    },
    "post_camp_followup": {
        "subject": "Thank you from {athlete_name} after {event_name}",
        "body": ("Coach {coach_last},\n\nThank you for running {event_name}. "
                 "One thing I took from it: {takeaway}. "
                 "Here is my updated film: {video_url}.\n"
                 "Are you recruiting my position for the Class of {class_year}? "
                 "I understand if the answer is not yet.\n\n{athlete_name}"),
        "needs": ["coach_last", "athlete_name", "event_name", "takeaway", "video_url", "class_year"],
    },
    "still_recruiting_nudge": {
        "subject": "Quick question, {athlete_name} Class of {class_year}",
        "body": ("Coach {coach_last},\n\nI wanted to follow up on my note from {last_touch_date}. "
                 "Are you still recruiting {position} in the Class of {class_year}? "
                 "A short answer either way helps me plan. Thank you.\n\n{athlete_name}"),
        "needs": ["coach_last", "athlete_name", "position", "class_year", "last_touch_date"],
    },
    "reference_request_to_own_coach": {
        "subject": "Could you vouch for me with a few programs?",
        "body": ("Coach {own_coach_last},\n\nI am building a list of {list_size} programs. "
                 "Would you be willing to (1) send film to them or (2) take a short call? "
                 "My list and highlight link: {video_url}. "
                 "Here are three sentences you could say: {three_sentences}\n\nThank you,\n{athlete_name}"),
        "needs": ["own_coach_last", "list_size", "video_url", "three_sentences", "athlete_name"],
    },
}

class MissingField(ValueError):
    pass

def render_template(name, fields):
    """Fill a template. Raises MissingField listing every blank field; refuses
    output that contains promise language. Returns dict(subject, body)."""
    t = TEMPLATES[name]
    blanks = [k for k in t["needs"] if not str(fields.get(k, "")).strip()]
    if blanks:
        raise MissingField("fill these first: " + ", ".join(blanks))
    sub = t["subject"].format(**fields)
    body = t["body"].format(**{**{k: "" for k in ("stat_line", "athlete_phone_or_email")}, **fields})
    hits = promise_hits(sub + "\n" + body)
    if hits:
        raise ValueError("promise language in your text: " + ", ".join(hits))
    return {"subject": sub, "body": body}

# ---- 4-touch cadence + target-list cap ---------------------------------------
TARGET_CAP = 30            # ACCESS.md section 7 risk 5 / SOLUTIONS "30-school list"
CADENCE_DAYS = [0, 10, 24, 45]   # touch 1..4, days after first send; hypothesis spacing
CADENCE_LABELS = ["intro_email", "still_recruiting_nudge", "post_camp_followup", "still_recruiting_nudge"]

def cadence(first_send_iso):
    """Planned touch dates. These are reminders for the family, not scheduled sends."""
    d0 = parse_date(first_send_iso)
    return [{"touch": i + 1, "template": CADENCE_LABELS[i],
             "date": (d0 + dt.timedelta(days=n)).isoformat()} for i, n in enumerate(CADENCE_DAYS)]

def check_target_list(rows):
    """rows: list of dicts with 'school','coach_last'. Enforces cap and duplicates."""
    problems = []
    if len(rows) > TARGET_CAP:
        problems.append("%d schools exceeds the %d cap: personalize fewer." % (len(rows), TARGET_CAP))
    seen = set()
    for r in rows:
        k = (r.get("school", "").strip().lower(), r.get("coach_last", "").strip().lower())
        if not k[0]:
            problems.append("row missing school")
        elif k in seen:
            problems.append("duplicate: %s / %s" % k)
        seen.add(k)
    return {"ok": not problems, "count": len(rows), "problems": problems}

# ---- Follow log (manual entry) -----------------------------------------------
LOG_COLUMNS = ["school", "division", "sport", "coach_last", "questionnaire_url", "questionnaire_done_date",
               "touch_no", "touch_date", "channel", "parent_copied", "reply_received", "reply_date",
               "reply_type", "next_action", "next_date", "notes"]
REPLY_TYPES = ["", "none", "form_auto", "staff_generic", "coach_personal", "film_request", "visit_invite", "not_recruiting"]
CHANNELS = ["email", "dm", "questionnaire", "camp_in_person", "call", "own_coach_intro"]

def blank_log_csv(rows=30):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(LOG_COLUMNS)
    for _ in range(rows):
        w.writerow([""] * len(LOG_COLUMNS))
    return buf.getvalue()

def validate_log(csv_text, today_iso):
    """Return dict(ok, errors[], rows). Catches bad enums, bad dates, reply-before-touch."""
    rd = csv.DictReader(io.StringIO(csv_text))
    errors, rows = [], []
    if rd.fieldnames != LOG_COLUMNS:
        return {"ok": False, "errors": ["header mismatch"], "rows": []}
    today = parse_date(today_iso)
    for i, r in enumerate(rd, start=2):
        if not any((v or "").strip() for v in r.values()):
            continue
        if not r["school"].strip():
            errors.append("line %d: school required" % i)
        if r["channel"] and r["channel"] not in CHANNELS:
            errors.append("line %d: channel %r" % (i, r["channel"]))
        if r["reply_type"] not in REPLY_TYPES:
            errors.append("line %d: reply_type %r" % (i, r["reply_type"]))
        for col in ("touch_date", "reply_date", "next_date", "questionnaire_done_date"):
            if r[col]:
                try:
                    d = parse_date(r[col])
                    if col in ("touch_date", "reply_date") and d > today:
                        errors.append("line %d: %s is in the future" % (i, col))
                except ValueError:
                    errors.append("line %d: %s not YYYY-MM-DD" % (i, col))
        if r["reply_date"] and r["touch_date"]:
            try:
                if parse_date(r["reply_date"]) < parse_date(r["touch_date"]):
                    errors.append("line %d: reply before touch" % i)
            except ValueError:
                pass
        if r["parent_copied"] not in ("", "yes", "no"):
            errors.append("line %d: parent_copied yes/no" % i)
        rows.append(r)
    return {"ok": not errors, "errors": errors, "rows": rows}

def due_actions(rows, today_iso):
    today = parse_date(today_iso)
    out = []
    for r in rows:
        if r.get("next_date"):
            try:
                if parse_date(r["next_date"]) <= today:
                    out.append({"school": r["school"], "next_action": r["next_action"], "next_date": r["next_date"]})
            except ValueError:
                pass
    return sorted(out, key=lambda x: x["next_date"])

# ---- KPI math (self-reported; never an outcome claim) -------------------------
def kpis(rows, window_days=14, today_iso=None):
    """Self-reported tracker KPIs from a validated log. Counts only; no outcome claims."""
    today = parse_date(today_iso) if today_iso else dt.date.today()
    cutoff = today - dt.timedelta(days=window_days)
    sent = [r for r in rows if r.get("touch_date") and r.get("channel") in ("email", "dm")
            and parse_date(r["touch_date"]) >= cutoff]
    replies = [r for r in rows if r.get("reply_type") in ("staff_generic", "coach_personal", "film_request", "visit_invite")]
    personal = [r for r in rows if r.get("reply_type") in ("coach_personal", "film_request", "visit_invite")]
    schools = {r["school"].strip().lower() for r in rows if r.get("school")}
    n_touch = len([r for r in rows if r.get("touch_date")])
    return {"window_days": window_days, "emails_dms_in_window": len(sent), "schools_tracked": len(schools),
            "touches_logged": n_touch, "replies_any": len(replies), "replies_personal": len(personal),
            "parent_copied_rate": (round(sum(1 for r in rows if r.get("parent_copied") == "yes") /
                                         max(1, len([r for r in rows if r.get("touch_date")])), 3)),
            "label": "self-reported; not an outcome claim"}
