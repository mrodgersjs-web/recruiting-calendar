# Wow-Factor Verifier heartbeat (Recruiting Calendar v3) — standing prompt
Owner: Mike, 2026-11-05. Runs every 30 minutes until STOP criteria hit. Read ../BRIEF-V3.md first; integrity rules bind.

Each run:

0. END TIME (Mike, 2026-11-05 23:04 MST: "keep going until 8 am"). If now (America/Denver) is at or after 2026-11-06 08:00, do not
   capture or build: write "RUN-WINDOW-ENDED 08:00" at the top of SCORECARD.md, write MORNING-REPORT.md (baseline vs latest Jev scores
   per surface, every fix shipped, every roast verdict, open blockers), message the parent task vDWfWwrS181z6OQU to pause this routine,
   and exit.

2b. HEYCATCH ANALYSIS (every run; skill /Users/rig128gb/.aside/u/0/skills/user/heycatch/SKILL.md; READ-ONLY via Gmail
   mike@rodgersintelligence.com, query from:heycatch newer_than:2d; never log in to heycatch.ai). Look for: (i) a growth profile / site
   audit for this site or its project, (ii) catches about recruiting, sports parents, NCAA, NIL, college athletes. Turn each into a
   candidate fix with the email date+subject as its source; feed the top one into step 4/5 alongside Jev's top finding. If HeyCatch has
   nothing on this site yet (expected until Mike creates the project from research/L5-heycatch/SETUP-DRAFT.md), apply HeyCatch's own
   documented rubric from research/L5-heycatch/HEYCATCH-INSIGHTS.md (ICP fit > ask directness > freshness; growth-profile sections:
   pains+where they hang out, competitors+weak spots, site audit /100 with fixes ranked by impact, quick wins first) as a self-audit,
   scoring the live site /100 and LABELING it "HeyCatch-method self-audit, not a HeyCatch report". Log the score in SCORECARD.md.
1. CAPTURE. Open https://recruiting-calendar.vercel.app (and the latest preview if newer) in a background tab. Screenshot at 1440x900 and 390x844:
   home ring carousel (rest + mid-spin), one athlete story (3 scroll depths: d1 = top of page; d2 = the first full-bleed visual beat (.vis); d3 = the story-end visual band directly above the playbook list (scroll the LAST .tag-ill or the band element to ~120px below the header). Do NOT use the page bottom/footer as d3), playbook/price page, any video frame, logo lockup.
   Save to v3/HEARTBEAT/runs/<ISO>/shots/. Close tabs after.
2. JUDGE WITH JEV IMAGE (hosted, ~/.rig/bin/jev-image check, keep raw JSON). For each shot ask 5 questions, rubric
   "wow:  striking, premium, would stop a scroll|ok: competent but forgettable|weak: generic, broken or empty":
   (a) overall wow, (b) imagery quality, (c) motion/3D legibility in frame, (d) typography/brand, (e) does it make a parent want to buy.
   CONTROLS every run: a blank white PNG and the v1 almanac screenshot (/Users/rig128gb/.aside/u/0/sessions/2026-11-05_vDWfWwrS181z6OQU/tmp/v2-hero.png) — blank must score wow<=0.2,
   else the judge is noise that run: mark DEFERRED.
3. JUDGE TEXT WITH JEV (rig-s1gate check): every athlete story script and playbook changed since last run, rubrics
   website.buyer and plan.readiness; plus a deliberately broken control. Keep raw dimensions; never invent a single score.
4. ROAST ROOM (only every 4th run; the room weighs Jev's top finding AND the HeyCatch top fix as the options it chooses between, i.e. every 2h: count rows in SCORECARD.md; on other runs skip 4 and act on Jev's top finding directly). Run /roast-room (skill /Users/rig128gb/.aside/u/0/skills/user/roast-room/SKILL.md, 7 seats as real subagents) on the
   single biggest weakness Jev found: frame it as 4 distinct fixes A-D. Save the room under v3/HEARTBEAT/runs/<ISO>/roast/.
   Every 3rd Roast Room (every 6h), roast the RESEARCH and INPUTS instead (W1 folders): which source is thinnest, which claim is weakest.
5. ACT. Hand the winning fix to the builder lane (message the main task vDWfWwrS181z6OQU or spawn one fix subagent) with the exact
   change, then re-capture and re-judge that element in the same run.
6. LEDGER. Append to v3/HEARTBEAT/SCORECARD.md one row: date, per-surface Jev wow probability (mean of 1440+390), controls, text dims,
   roast verdict, fix shipped, delta. Baseline = run 1.
STOP when: every surface's wow >= 0.85 on 3 consecutive runs with controls passing AND the research roast finds no claim rated WEAK,
 i.e. a measured 10x vs baseline is not provable, so the stop is a measured ceiling, not a feeling. Then write STOP-REACHED at the top of SCORECARD.md and report it to the parent task vDWfWwrS181z6OQU (a run cannot pause its own routine; the parent pauses it).
NEVER: post publicly, email anyone except Mike's own address, spend money, generate a likeness of a real person, or edit the judge.

BUDGET: keep each run under ~25 minutes; if the Roast Room or fix step would overrun, record it as next-run work. If any previous run is still in progress (lock file v3/HEARTBEAT/.lock younger than 40 minutes; an older lock is stale from a crashed run, so delete it and proceed), exit immediately; create the lock at start and remove it at the end.

LANDED-CHECK (added 2026-11-06 02:05): before re-handing any fix as "not landed", open the shot and check whether the requested change is visibly present. If it is present but the score is still low, write "LANDED, score still low: <what the shot shows>" and send it to the next Roast Room as the weakest surface. Do not re-hand it. A score below target is not evidence that a fix is missing.
