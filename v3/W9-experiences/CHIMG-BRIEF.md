# Chapter imagery brief (Mike 2026-11-06 11:36: "different images that match each section title and what it is talking about")

For each athlete id you own, read v3/W9-experiences/out/<id>.json. For EACH chapter i (0-based), generate ONE image in the REPL with imagegen.generate({prompt, inputImages:[REF]}).

REF = /Users/rig128gb/Developer/recruiting-calendar/site/assets/media/cut-<id>-1080.webp  (the Pick-a-Path figure; a fictional adult in an invented-crest jersey).

Prompt template:
"Use the athlete in the reference image as the same person, same face, same jersey colours and same invented chest crest. Place them in a scene that shows: <chapter title>. Context: <what_was_happening>. <one concrete scene you choose that literally illustrates the title, e.g. offers -> athlete and two fictional parents at a kitchen table comparing printed offer letters and a laptop spreadsheet; eligibility -> athlete with a school counselor reviewing a transcript; film -> athlete editing game film on a laptop; visit -> athlete touring a generic campus with a coach; signing -> athlete signing a paper at a table with family; practice -> athlete training in their sport>. Cinematic editorial photograph, 16:9 landscape, natural light. Any other people are fictional adults. No readable text, no real school, league, NCAA or brand logos except the athlete's invented crest."

Every scene must be DIFFERENT and must match its own chapter title. Do not repeat the plain standing pose.

Save: copy each result to /Users/rig128gb/Developer/recruiting-calendar/v3/W9-experiences/chimg/<id>-<i>.png (fs.copyFile from the returned path). Run at most 4 generations in parallel per REPL call (calls time out at 120s). Skip files that already exist (resume-safe). If a generation errors, retry once; then record it as failed.

Do not edit any other file and do not deploy. Reply with: per athlete, chapters done / total, and any failures.
