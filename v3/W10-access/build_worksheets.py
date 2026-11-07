#!/usr/bin/env python3
"""Generate the printable/fillable worksheets into deliverables/. Deterministic, offline."""
import os, csv
import contact_kit as ck
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "deliverables")
NOTE = ("*Rules and scripts for families to use themselves. The Commit Book does not contact coaches, place "
        "athletes or promise introductions, replies or offers. Verify every date on the NCAA page for your sport.*\n")

def w(name, text):
    with open(os.path.join(OUT, name), "w") as f: f.write(text)

def build():
    os.makedirs(OUT, exist_ok=True)
    # 1 send-date worksheet
    w("1-send-date-worksheet.md", "# Worksheet 1: When may this coach answer?\n\n" + NOTE + """
Families may always write first. The date limits what the coach may send or say back.

| Division | What to know |
|---|---|
""" + "".join("| %s | %s |\n" % (d, n) for d, n in ck.DIVISION_NOTES.items()) + """
## Fill in (one row per sport)
| Sport | Division | Class year | First date coaches may reply (copy from NCAA sport calendar) | NCAA page / bylaw I read | Date I checked it |
|---|---|---|---|---|---|
| | | | | | |
| | | | | | |

Rule: if you cannot fill the "date I checked it" box, do not rely on the date. Re-check every 60 days.
Conflict flag: older blogs give different DM dates than 2026 sources. The NCAA sport calendar wins.
""")
    # 2 questionnaire checklist
    w("2-questionnaire-checklist.md", "# Worksheet 2: Questionnaire checklist\n\n" + NOTE + """
A questionnaire is interest data you give a program. It is not an offer and not a sign the coach is interested.
We link to public forms only. We never fill or submit one for you.

## Have ready before you open the form
- [ ] NCAA ID (needed for D1 and D2 forms; D3 and NAIA usually differ)
- [ ] Highlight link (passes Worksheet 4)
- [ ] Current transcript and test scores, if the form asks
- [ ] Your own coach's name and phone/email
- [ ] Stats, measurables, club/HS team, graduation year
- [ ] A parent email to copy on follow-up

## For each program
| School | Where I found the form (program site > recruiting) | Software (ARMS, Front Rush, custom) | Date submitted | Confirmation seen? | Logged in follow log? |
|---|---|---|---|---|---|
| | | | | | |
| | | | | | |

Note: D1 rule text on questionnaire timing changed around 2024 and sources conflict by date. Ask the program's compliance office if the form is not offered to you.
""")
    # 3 scripts
    parts = ["# Worksheet 3: Contact scripts (athlete's voice, parent copied)\n\n" + NOTE,
             "Draft in your own words. Keep each note short, specific to ONE program, and send from the athlete's own account. "
             "Parents organize; athletes write. Do not mass-send: coaches delete blasts.\n"]
    for name, t in ck.TEMPLATES.items():
        parts.append("\n## %s\nNeeds: %s\n\n```\n%s%s\n```\n" % (name, ", ".join(t["needs"]),
                     ("Subject: " + t["subject"] + "\n\n") if t["subject"] else "", t["body"]))
    parts.append("\n## 4-touch cadence (reminders, hypothesis spacing; not a schedule we run)\n| Touch | Days after first | Template |\n|---|---|---|\n")
    for i, (n, lab) in enumerate(zip(ck.CADENCE_DAYS, ck.CADENCE_LABELS), 1):
        parts.append("| %d | %d | %s |\n" % (i, n, lab))
    parts.append("\nTarget list cap: %d schools. Silence is often the rule, not rejection.\n" % ck.TARGET_CAP)
    w("3-contact-scripts.md", "".join(parts))
    # 4 link checklist
    w("4-highlight-link-checklist.md", "# Worksheet 4: Highlight link checklist\n\n" + NOTE + """
- [ ] Link, not an attachment (YouTube, Hudl or Vimeo)
- [ ] YouTube visibility is Unlisted or Public (never Private); setting says "No, not made for kids"
- [ ] Hudl share link is public
- [ ] Opens in a private/incognito window with no login, on a phone too
- [ ] 3 to 5 minutes; best clips in the first 30 seconds
- [ ] Title has name, class year, sport, position
- [ ] Number/jersey color named at the start so the coach can find you
- [ ] Do not upload athlete video to us. We do not host it.
Command-line check: `python3 kit_cli.py link <url> --minutes 4 --title "Name 2029 Sport Position" --tested yes`
""")
    # 5 ask-your-coach one pager
    w("5-ask-your-coach-one-pager.md", "# Worksheet 5: Ask your coach (one page to hand your HS/club coach)\n\n" + NOTE + """
Athlete name: ________  Sport/position: ________  Class: ____  Highlight link: ________

**What I am asking (check one or both):**
- [ ] Send my film to the programs below, or
- [ ] Take a short call with a program's coach

**Target list (max 30; start with 8 to 12)**
| School | Division | Coach to reach | Why this program fits |
|---|---|---|---|
| | | | |
| | | | |

**Three sentences you could say on a call:**
1. (How long you have coached me and in what role.)
2. (One specific strength you have seen, with an example.)
3. (One thing I am working on, honestly.)

Use the reference-request script in Worksheet 3. A coach is free to say no; thank them either way.
""")
    # 6 follow log
    with open(os.path.join(OUT, "6-follow-log.csv"), "w", newline="") as f:
        f.write(ck.blank_log_csv(30))
    w("6-follow-log-README.md", "# Worksheet 6: Follow log\n\n" + NOTE + """
Open `6-follow-log.csv` in any spreadsheet. One row per touch.
- channel: %s
- reply_type: %s
- Dates: YYYY-MM-DD. Run `python3 kit_cli.py log-check 6-follow-log.csv` to validate and list what is due.
Counts you get are self-reported. Do not quote them as results.
""" % (", ".join(ck.CHANNELS), ", ".join(t for t in ck.REPLY_TYPES if t)))
    return sorted(os.listdir(OUT))

if __name__ == "__main__":
    for n in build(): print(n)
