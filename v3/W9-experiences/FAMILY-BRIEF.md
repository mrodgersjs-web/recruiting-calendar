# Family chapter images v2 (Mike 2026-11-06 11:52 + "do this for all images")
Mike: "a picture of the parents of the athlete sitting down together trying to figure out why only a couple of schools showed interest" ... "do this for all images. match the section title with picture of the parents and athletes trying to solve the problem. use jev image to verify the athlete looks the same and the parents would be parents of the athlete"

For each athlete id you own: read v3/W9-experiences/out/<id>.json. For EACH chapter i generate ONE image:
imagegen.generate({prompt, inputImages:[REF]}) where REF = /Users/rig128gb/Developer/recruiting-calendar/site/assets/media/<cut>-1080.webp
(cut file: composite-X -> cut-X except composite-swim->cut-swimmer, composite-wbasketball->cut-wbasketball, composite-sprinter->cut-sprinter; real ids -> cut-<id>).

Prompt:
"The young adult athlete from the reference image (same face, same skin tone, same hair, wearing the same jersey with the same invented chest crest) sits with their two parents, who are clearly their biological parents: matching ethnicity and family resemblance, aged mid-40s to 50s. Together they are working on this problem: <chapter title>. <what_was_happening>. Show them actively solving it: <ONE concrete action matching the title, e.g. leaning over a laptop spreadsheet of schools with only two replies circled, comparing printed offer letters, on a speakerphone call with a coach, reviewing a transcript with a highlighter, watching game film on a TV and pausing it, filling a calendar on the fridge>. Warm, real home or relevant setting, emotion matches the moment (worried, focused, relieved). Cinematic editorial photograph, 16:9 landscape, natural light. No readable text, no real school, league, NCAA or brand logos; only the athlete's invented crest."
Every chapter's action must differ and match its title.

Save to /Users/rig128gb/Developer/recruiting-calendar/v3/W9-experiences/famimg/<id>-<i>.png (fs.copyFile from the returned path). Max 3 generations in parallel per REPL call (120s timeout). Resume-safe: skip existing files.

VERIFY each saved image with Jev image (bash):
~/.rig/bin/jev-image check --image <png> --question "<q>" --rubric "<opts>" --json
Q1 "Does the young athlete in this image look like the same person as the athlete in the reference (same skin tone, hair, jersey colours and crest)? Reference: <describe the ref figure in one line>" rubric "same|different"
Q2 "Are there two adults who plausibly look like the athlete's parents (matching ethnicity, family resemblance, parent age)?" rubric "yes|no"
Q3 "Does the scene show the family working on: <chapter title>?" rubric "yes|no"
If any answer is the negative label OR verdict ESCALATE/DEFER, regenerate once with the issue fixed and re-check. Record results to famimg/<id>-<i>.jev.json ({q1,q2,q3: {label,confidence,verdict}}). If jev-image is unreachable, record "DEFERRED" and continue (do not self-certify).

Do not edit other files or deploy. Reply: per athlete done/total, Jev pass counts, failures.
