# Behavioral Decision Lattice: the parent buyer (W1-bx, 2026-11-05)
Mode: bxskill `lattice` -> `bx-falsifier` -> `bx-verify-gate`. Inputs read: BRIEF-V3.md, research/L6-competitors/PARENT-VOICE.md (PV), research/00-business-plan.md (BP).
Not yet read (had not landed at write time): v3/W1-parent-demand/DEMAND.md, v3/W1-recruit-behavior/PLAYBOOK-INPUTS.md. Re-run this lattice when they land.
Status: a PRIOR from ~30 Reddit verbatims, not a forecast. Zero site observations exist. No number below is a measured conversion rate.

## Jev ruling (binding barrier)
`aside-jev choice`, model jev-1.14.0, 2026-11-05: **trust_skepticism_of_recruiting_products** p=0.66 (effort/athlete won't use it 0.18, price 0.12, relevance 0.04). Confidence 0.55 = marginal. decision_id null (not logged). Treat as the working hypothesis, kill it with P1 below.

## The committee (B2C, 2-4 people) and veto set
| Actor | Role | What they need to say yes | Veto? | Stall cause |
|---|---|---|---|---|
| Primary parent (usually the researcher) | Buyer, reads the story | "This is not NCSA again" + "it fits my kid's sport and level" | Initiator | Burned before or has read the burn stories (PV Pain 1-2) |
| Other parent / co-payer | Spend approver | Price small enough to not need a talk; nothing recurring; refund | Soft veto on spend | "We already paid for X and it did nothing" |
| Athlete (16-18) | User of the playbook | It's theirs to run, not a parent surveillance tool; not embarrassing | **Hard veto on use** (product is dead if they won't do it) | Effort, autonomy, "my coach handles it" |
| Club/HS coach (sometimes) | Advisor | Doesn't contradict what they tell families | Advisory veto | "You don't need that" (PV Pain 3 says coaches dismiss services) |
Consensus is multiplicative: if each of 3 approvers is at 0.8, joint is 0.51. The cheapest lift is shrinking the veto set: price under the "ask my spouse" threshold (removes co-payer) and making the athlete the named operator (turns the veto into a co-owner).

## Barriers (6 axes, condensed)
| Axis | Barrier | Evidence pointer | Strength |
|---|---|---|---|
| Trust / problem history | Recruiting products = sales funnel + vague "a coach viewed you" upsell | PV Pain 1, Pain 2 (NCSA, SportsRecruits refund) | **Binding** (Jev 0.66) |
| Need | Parent wants a system they control, not a service | PV Desire 1 ("simple system we controlled") | Strong; is our product's fit |
| Relevance | Generic advice ignored; sport nuance matters | PV Desire 3 (score 8 and 10, highest in file) | Strong for story matching |
| Emotion | Fear of missing the window + fear of being scammed; both run at once | PV Pain 1-2, Desire 2 | Medium; fear must be resolved, not stoked |
| Effort / capability | DIY needs discipline ("stay on top of your videos") | PV Desire 1 (score 6) | Second barrier (Jev 0.18); athlete veto lives here |
| Price | Low absolute ($7-45 per BP) | BP offer table | Weak as barrier; but a *too-cheap* price can read as low quality: untested |
Status-quo competitor: the family's own spreadsheet + free FieldLevel/NCSA free tier (PV Praise). We must beat "free and mine", not beat NCSA.

## Falsifiable predictions (each with a kill criterion)
Measure on the live site with test-mode checkout/email capture events only. Pre-register before launch; n and windows below are minimums, not powered estimates (no baseline exists).
- **P1 (binding barrier = trust).** Story pages that show the "what this is NOT" block (no sales calls, no contacting your kid, one-time price, every rule cites a bylaw) get a higher story->playbook-click rate than the same page without it. KILL: after >=400 story sessions per arm, if the difference is <1 pt absolute or reversed, trust is not binding; promote P2 (effort) to binding.
- **P2 (athlete veto).** Playbook pages that name the athlete as operator ("built for the athlete to run, parent to support") convert better among sessions arriving with a sport filter set than parent-only framing. KILL: >=300 sessions/arm, no lift >=1 pt => athlete veto is not the stall; drop the framing to a single line.
- **P3 (relevance).** Visitors whose first story matches their selected sport click through to a playbook at >=1.5x the rate of mismatched first stories. KILL: ratio <1.2 over >=500 sessions => sport-matching in the carousel is decoration; stop investing in per-sport stories.
- **P4 (co-payer veto / price).** Offers <= $19 show no higher cart abandonment than $7-9 offers. KILL: if abandonment at $19-45 is >=1.5x the $7-9 rate over >=150 checkout starts each, the co-payer veto is real above ~$19; lead with the $9-25 entry.
- **P5 (anti-prediction: urgency does NOT help).** A calendar-date reminder ("the next contact date for your sport is X, per bylaw Y") improves click-through vs. no date, but generic urgency wording would not; we only ship the factual date. KILL: if the factual date shows no lift over >=400 sessions/arm, dates are not a motivator; keep them as information only.
Every prediction is UNRESOLVED until observations exist. Log observations via `bx_observe` against lattice id `recruiting-calendar-parent` (not yet created in the studio; to do when data exists).

## What this lattice does NOT claim
No effect sizes (none measured). No claim that stories cause purchases. No member counts, outcomes, or testimonials (BRIEF rule 3).
