# W5-athletes: the rest of the people (Mike 2026-11-06)

Ask, verbatim: "generate the rest of the people and make sure they have balls and sports equipment in their hands and on,
generate logos of d1, d2, d3 schools on all their jersey's which are close but not exactly right."

## What shipped
- 21 figures, one per story slot (prod commit 4b3f511 + the cache-bust follow-up). 8 composites regenerated, 13 new for the slots
  that were typographic text cards (renfrow, groenewegen, lowe, pichardo, white, pirosko, marpet, rodenfels, perez, coward,
  rodriguez, butler, wondolowski).
- Every figure holds or wears its sport's equipment: football + helmet + lined gloves, bat + fielding glove + batting gloves,
  softball + glove, basketball(s), volleyball + knee pads, headgear, relay baton + race bib, kickboard + goggles + cap,
  goalie stick + caged helmet, soccer ball + shin guards, racing shoes.
- Every jersey/singlet/cap carries ONE invented college athletics crest - animal-head shield, arched 3-letter monogram,
  wrong invented wordmark, lettering a little mangled. Deliberately close to a real D1/D2/D3 mark and not any of them.
  No apparel brand marks anywhere, per the pre-existing no-trademark rule.
- Pipeline: ROSTER.json (21 prompts) -> imagegen on chroma green -> build.py keys, crops to 9:16, exports
  cut-<key>-640.webp and -1080.webp into site/assets/media, writes IMAGES.json and two audit sheets in sheet/.
- Independent vision audit (visual subagent, both sheets): 21/21 gear=YES, crest=YES, NEARMISS (no real brand or real
  school mark found), body=FULL, defects=none. Sheets kept here as the evidence.

## The one judgement call, reversible by Mike's word
BRIEF-V3 rule 2 says a real named athlete gets NO generated likeness. The ring had 13 bare text cards, and Mike asked for
people. Resolution: the 13 slots got a **fictional same-sport, same-division composite figure**, and the card tag now reads
`Illustration · not Derrick White` etc., with the same wording in the img alt. Story pages are unchanged (real athletes keep
the typographic kinetic-type hero), and the phone deck still shows composites only under "No image of a real athlete is shown
or generated." So no likeness is claimed; the artwork is labelled illustration at the point of view. If Mike would rather the
real-athlete cards stay typographic, delete ART in v3/W2-site/data_build.py and rebuild - one line.

## Payload note
Card art on the home page went from 8 to 21 images: 1.64 MB of 640px webp (all eager, the ring's existing no-pop-in rule).
Drop to ~1.1 MB by regenerating at quality 76 if the perf lane wants it back.
