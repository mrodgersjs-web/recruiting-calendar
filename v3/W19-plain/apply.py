# -*- coding: utf-8 -*-
"""W19: apply the proofreader's plain-language fixes to the generator.

Matching is whitespace-flexible (the source is hard-wrapped) and reports every
pair it could not find, so nothing is silently skipped.
"""
import pathlib, re, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

P = pathlib.Path(r"C:\Users\Jloeh\Developer\recruiting-calendar\v3\W19-plain\bball-plain.py")
src = P.read_text(encoding="utf-8")

PAIRS = [
 ("This is not a list of camps and combines.", "This is not a list of camps and team showcases."),
 ("Then work the plan in Chapter 2", "Then follow the plan in Chapter 2"),
 ("with your school counselor, one line at a time, and cross off each item when you finish it.",
  "counselor. Go one line at a time. Cross off each item when you finish it."),
 ("Three rules that caught families off guard last year", "Three rules that surprised families last year"),
 ("A family that knows the roster limit, the signing dates, and the video standard competes",
  "A family that knows the team size limit, the signing dates, and the video standard compete"),
 ('If something you read says "sign your NLI," it is a year out of date.',
  'If something you read says "sign your NLI (National Letter of Intent)," it is a year out of date.'),
 ("The person who recruited you is the person who owes you an answer.",
  "The person who recruited you is the one who has to reply to you."),
 ("In basketball the team is small and the number of players is huge",
  "In basketball the team is small and the pool of players is huge"),
 ("Aid is not capped and no one is promised more than one year",
  "There is no cap on the amount of aid, and no one is promised more than one year"),
 ("The offer is about getting in, plus the aid the school gives for grades or need.",
  "The offer is about getting on the team, plus the aid the school gives for your grades or your family's money needs."),
 ("The lowest grade rules and the fastest coach contact.", "The lowest requirements and the fastest coach contact."),
 ("one letter that closes the door on other junior colleges.",
  "one letter that stops your child from signing with other junior colleges."),
 ("play right away, and move up a year later.", "play right away, and move up to a four-year school a year later."),
 ("Now count the doors the other way.", "Now look at the same numbers from the other side."),
 ("61% of those places", "61% of those open team spots"),
 ("where the grades and the aid package work for your family",
  "where your grades qualify and the aid they offer fits your family"),
 ("If your list is shorter than this, it is a hope, not a plan.",
  "Add those up and you have 40 to 55 schools. If your list is shorter than this, it is only a wish, not a working plan."),
 ("are worked out from the rule, which says early signing starts on the second Wednesday in November and runs to the next Wednesday, and that the regular period starts on the second Wednesday in April.",
  "are worked out from the rule. The rule says early signing starts on the second Wednesday in November and runs to the next Wednesday. It also says the regular period starts on the second Wednesday in April."),
 ("First day a Division I men's basketball coach may contact you first.",
  "First day a Division I men's basketball coach may contact you."),
 ("Highlight video is finished. It runs under four minutes, it shows defense, an arrow points at your child in every clip, and you send a link rather than a file.",
  "Highlight video is finished. It runs under four minutes. It shows defense. An arrow points at your child in every clip. You send a link, not a file."),
 ("A few days around this week are usually a dead period, so no visits and no in-person talking.",
  "A few days around this week are usually a dead period, a stretch when coaches may not talk to you in person."),
 ("April is a real second door.", "April is a real second chance to sign."),
 ("This is the NCAA's last look at your grades, your classes, and your play. You may ask from April 1 of senior year for a fall start.",
  "This is the review that decides whether your child can play college sports. You may ask for it starting April 1 of senior year, if your child starts college in the fall."),
 ("It holds your child for one school year and it closes the door on every other junior college. It does not close the door on a four-year school.",
  "It holds your child for one school year. It stops your child from signing with any other junior college. It does not stop your child from signing with a four-year school."),
 ("Each level uses a different paper, and the papers bind you in different ways.",
  "Each level uses a different form, and each form sets different limits on what you can do."),
 ("enforce one</td>", "make schools follow it</td>"),
 ("It gives you no national protection.", "It gives you no protection under the national rules."),
 ("It does not stop a four-year school. It does close the door on every other junior college.",
  "It does not stop a four-year school. It does stop every other junior college."),
 ("may answer questions one and two, and the new settlement rules say they may share roster numbers.",
  "may answer questions one and two. The new rules that came out of a court settlement say coaches may share team-size numbers."),
 ("Class year, position, height, GPA, town, and one number that matters:",
  "Class year, position, height, GPA (grade point average), town, and one number that matters:"),
 ("I averaged {{PPG}} points, {{RPG}} rebounds and {{APG}} assists in {{games}} varsity games",
  "I averaged {{PPG}} points per game, {{RPG}} rebounds per game and {{APG}} assists per game in {{games}} varsity games"),
 ("I also grab {{n}} rebounds a game in the half court, which is the part of my game I want to turn into a college job.",
  "I also grab {{n}} rebounds a game in half court. That is the part of my game I want to turn into a college job."),
 ("a stat line from the weekend", "your numbers from the weekend"),
 ("class year, eligibility number</li>", "class year, eligibility number (the ID from your child's NCAA file)</li>"),
 ("Your defensive rebounding rate might.", "A strong defensive rebounding number might."),
 ("plus two or three full possessions</td>", "plus two or three full plays shown start to finish</td>"),
 ("A full play shows a choice. One cut shows editing.", "A full play shows the player's choices. A short clip shows editing skill."),
 ("Unlisted YouTube link, no password, plus a separate",
  "Unlisted YouTube link (anyone with the link can watch it, and it is not listed in searches), no password, plus a separate"),
 ("That is where a summer team is set up, where the adults are checked, and where extra paperwork shows up if a player lives with a family that is not his own.",
  "That is where a summer team is set up. It is also where the adults are checked. Extra paperwork shows up if a player lives with a family that is not his own."),
 ("The hours a coach may watch are limited, and they differ for boys and girls: in June, men's coaches may watch from noon Friday to 6pm Sunday, and women's coaches from noon Thursday to 6pm Saturday.",
  "The hours a coach may watch are limited, and they differ for boys and girls. In June, men's coaches may watch from noon Friday to 6pm Sunday. Women's coaches may watch from noon Thursday to 6pm Saturday."),
 ("and is that paperwork filed?", "and has that paperwork been filed?"),
 ("and it may not fall inside a period when coaches are barred from contact.",
  "It may not fall inside a dead period, when coaches are not allowed to contact recruits."),
 ("Now the one that hurts: in Division I, an unofficial visit is not allowed during the month of July unless your child has already signed a written offer of aid or admission, or paid a deposit to the school.",
  "Now for the rule that catches most families. In Division I, an unofficial visit is not allowed during the month of July. It is allowed only if your child already signed a written offer of aid or admission, or paid a deposit to the school."),
 ("The July trip becomes a road trip, because the coach cannot host you.",
  "The July trip becomes a trip you pay for yourself, because the coach cannot host you."),
 ("A branch of a top camp is worth it because the college staff who run the main camp show up.",
  "A branch of a top camp is worth it because the college coaches and staff who run the main camp show up."),
 ("Two ways to do it: handle it yourself for $700 to $2,000 a year (build the profile, keep the classes on track, send the emails yourself, shoot your own video), or pay for help at $1,000 to $3,500 a year on top of the camp money you were spending anyway.",
  "Two ways to do it. Handle it yourself for $700 to $2,000 a year: build the profile, keep the classes on track, send the emails yourself, and shoot your own video. Or pay for help at $1,000 to $3,500 a year, on top of the camp money you were already spending."),
 ("when your child is not the type they chase", "when your child is not the kind of player those coaches recruit"),
 ("The first invite was the real one.", "A school that is already texting you has already invited you in."),
 ("[ ] map every planned class against the school's NCAA-approved list, keep a signed copy",
  "[ ] check every planned class against the school's NCAA-approved list, and keep a signed copy"),
 ("[ ] start lifting and shooting routine; play a second sport if you can",
  "[ ] start a lifting and shooting routine, and play a second sport if you can"),
 ("[ ] build the school list to 60 programs by position</p>",
  "[ ] build the school list to 40 to 55 schools across all five levels</p>"),
 ("[ ] ask the four questions in Chapter 3 of every school that is serious</p>",
  "[ ] ask the four questions in Chapter 3 of every school that is serious about recruiting you</p>"),
 ("A real total, spread over four years: <strong>$3,000 to $10,000 a year</strong>.",
  "Expect to spend <strong>$3,000 to $10,000 a year</strong> while your child is in high school."),
 ("one source says March 1 of junior year, another says June 1 after 10th grade.",
  "One source says March 1 of junior year. Another says June 1 after 10th grade."),
 ("Treat the men's June 15 date as firm, and confirm the women's date, and the first paid-visit date for both boys and girls, in the current rule book before you plan a trip.",
  "Treat the men's June 15 date as firm. Confirm the women's date, and the first paid-visit date for boys and girls, in the current rule book before you plan a trip."),
 ("Second, the page that lists the 2026-27 signing dates prints November 19, while the rule text and the recruiting page give November 11 to 18.",
  "Second, one page that lists the 2026-27 signing dates prints November 19. The rule text and the recruiting page give November 11 to 18."),
 ("A rule book that admits what it has not checked is worth more trust than one that hides it.",
  "A rule book that admits what it has not checked is more trustworthy than one that hides it."),
 ("Print the class checklist in Chapter 7 and book the counselor meeting for the first open slot this term.",
  "Print the class checklist in Chapter 7. Book the counselor meeting for the first open slot this term."),
 ("Build the school list to 40 to 50 programs across all five levels", "Build the school list to 40 to 55 schools"),
]

done, missed = 0, []
for old, new in PAIRS:
    pat = re.compile(re.escape(old).replace(r"\ ", r"\s+").replace("\\\n", r"\s+"))
    if pat.search(src):
        src = pat.sub(lambda _: new, src, count=1)
        done += 1
    else:
        missed.append(old)
P.write_text(src, encoding="utf-8")
print("applied:", done, "of", len(PAIRS))
for m in missed:
    print("  NOT FOUND:", m[:95])
