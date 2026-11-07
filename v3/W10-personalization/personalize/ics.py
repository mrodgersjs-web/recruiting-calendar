"""ICS export of ranked, dated, bookable items only. No child identifiers, no TBD guesses."""
from datetime import date, timedelta


def _esc(s):
    return str(s).replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")


def to_ics(result):
    lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//W10 personalization prototype//EN"]
    for it in result.get("ranked", []):
        for i, d in enumerate(it.get("dates") or []):
            try:
                s = date.fromisoformat(d["start"])
                e = date.fromisoformat(d.get("end") or d["start"]) + timedelta(days=1)  # DTEND exclusive
            except (KeyError, ValueError):
                continue
            desc = "Label: %s. Read on %s. Source: %s" % (it["highest_label"], it["read_on"], it["url"])
            if d.get("is_window"):
                desc += ". Date is a window, not a confirmed day; confirm with the organizer."
            lines += ["BEGIN:VEVENT", "UID:%s-%d@w10.invalid" % (it["entity_id"], i),
                      "DTSTAMP:%sT000000Z" % result["as_of"].replace("-", ""),
                      "DTSTART;VALUE=DATE:%s" % s.strftime("%Y%m%d"),
                      "DTEND;VALUE=DATE:%s" % e.strftime("%Y%m%d"),
                      "SUMMARY:%s" % _esc(it["name"]), "DESCRIPTION:%s" % _esc(desc), "END:VEVENT"]
    lines.append("END:VCALENDAR")
    return "\r\n".join(lines) + "\r\n"
