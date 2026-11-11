import pathlib, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p = pathlib.Path(r"v3\W19-plain\bball-plain.py"); t = p.read_text(encoding="utf-8")
pairs = [
 ("Check every class your child has taken, and every class your child plans to take, against the school's list of NCAA-approved classes.",
  "Check every class your child has taken and plans to take against the school's list of NCAA-approved classes."),
 ("From this day the coach may email, text, call, or send you a form to fill out. The rule is on the coach, not on you. You may write to a coach any time.",
  "From this day the coach may email, text, call, or send you a form. The rule is on the coach, not on you."),
 ("Highlight video is finished. It runs under four minutes. It shows defense. An arrow points at your child in every clip. You send a link, not a file. Keep two full games ready to send on request.",
  "Highlight video is finished. It runs under four minutes, shows defense, and marks your child in every clip. Send a link, not a file. Keep two full games ready."),
 ("This is the review that decides whether your child can play college sports. You may ask for it starting April 1 of senior year, if your child starts college in the fall. The school cannot put your child in a game until this file is done.",
  "This is the NCAA's last review of your child's grades and classes. You may ask starting April 1 of senior year for a fall start. The school cannot play your child until the file is done."),
 ("The final high school transcript, with proof of graduation, must reach the NCAA Eligibility Center. The counselor sends it. A class your child finished but never reported does not count.",
  "The final high school transcript, with proof of graduation, must reach the NCAA Eligibility Center. The counselor sends it."),
 ("It holds your child for one school year. It stops your child from signing with any other junior college. It does not stop your child from signing with a four-year school.",
  "It holds your child for one school year. It stops your child from signing with any other junior college. A four-year school is still open to you."),
]
n = 0
for a, b in pairs:
    if a in t: t = t.replace(a, b); n += 1
    else: print("  miss:", a[:70])
p.write_text(t, encoding="utf-8"); print("plan rows trimmed:", n, "of", len(pairs))
