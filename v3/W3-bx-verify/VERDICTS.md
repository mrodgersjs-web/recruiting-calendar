# W3 independent behavioral falsifier: VERDICTS (2026-11-05)
Method: bx MCP tools (bx_falsify, bx_bias_audit) NOT available in this session (search_tools found none). Ran bx-falsifier method by hand from ~/Developer/behavioral-science-studio/skills/bx-falsifier/SKILL.md. bx-verify-gate SKILL.md not present at that path: verify step = Jev (aside-jev noul, jev-1.14.0, decision_id null on all calls) plus file evidence. Author of this file did not write W1/W2. No verdict below is self-certified as "shipped"; Jev numbers are quoted, not used as the verdict alone. Literature claims were NOT re-searched this pass (no 7-against search run): marked accordingly.

## A. The 5 lattice predictions
| P | Verdict | Evidence / attack |
|---|---|---|
| P1 trust block lifts story->playbook click | UNFALSIFIABLE as built | Beat 6 (the "what this is NOT" content) is fixed text on all 14 stories and beat 7 repeats "No calls, no sales team, nobody contacts your kid". There is no "without" arm, so the >=400/arm kill can never fire. Also: n=400/arm cannot detect a 1-pt absolute difference at a ~2-5% base rate (needs ~5-10k/arm); a null at 400 is uninformative, not a kill. |
| P2 athlete-as-operator framing | UNFALSIFIABLE as built | "For the athlete to run, parents support" is in every beat 7 and the carousel micro-line: no control arm. Same power problem (300/arm). "Sessions with a sport filter set" is undefined in tracking. |
| P3 sport-matched first story >=1.5x | SURVIVES as a design (testable, untested) | Kill rule (ratio <1.2 over >=500 sessions) is measurable if first-story sport and selected sport are both logged. Confound: carousel autoplay order decides "first story", not the user; need random first-story assignment or the ratio measures self-selection. |
| P4 price / co-payer veto | UNFALSIFIABLE now | Checkout is email-capture/test-mode: "cart abandonment" and ">=150 checkout starts each" at $19-45 do not measure payment friction. Kill cannot fire honestly until live payments. Story offers are $9-29, not a clean split. |
| P5 factual date helps, urgency does not | REFUTED in its "anti" half as a claim, UNFALSIFIABLE as test | Only the factual-date arm ships, so "generic urgency would not help" is never tested (asserted, not predicted). Separately, live homepage copy "It also tells you what each one costs if you miss it" is loss framing adjacent to the urgency P5 excludes (Jev noul 0.31 dark-pattern: low, keep but watch). |
Overall: the lattice is a PRIOR (W1 says so). 4 of 5 kill criteria cannot fire on the current build. Status: all 5 remain UNRESOLVED/DEFERRED for observation; none SURVIVES as tested.

## B. W1 AUDIT persuasion claims (re-attacked)
| # | Claim | W1 | W3 verdict |
|---|---|---|---|
| 1 | Trust is binding barrier | WEAK | UNFALSIFIABLE until P1 has an arm. Jev 0.66/conf 0.55 on ~30 self-selected complainer comments is not evidence of a population barrier. |
| 2 | Identifiable story > statistics | SUPPORTED (lit) | WEAK here: identifiable-victim effect is a charity-donation finding with mixed replication; 13 of 14 stories are real people mostly at pro/national level, so this also imports survivorship. Not re-searched. |
| 3 | Two-sided message raises trust | SUPPORTED | SURVIVES (narrow): beat 6 is short, honest, present on all 14. Risk: identical 62-word block x14 reads as boilerplate legal cover, which the framework's own boundary condition warns against. |
| 4 | Cited bylaw raises credibility | WEAK | WEAK, agree. Rodriguez beat 4 HOLD (no NAIA rule) still open. |
| 5 | Bundle $25 vs $37 | SUPPORTED arithmetic | UNFALSIFIABLE on stories: no beat 7 shows a bundle; CTA-SCRIPTS bundle (#20 $25) not used. Check pricing page sum before ship. |
| 6 | Low price shrinks co-payer veto | WEAK | UNFALSIFIABLE now (see P4). And the site also sells a $149/yr trial, which contradicts the "nothing recurring" co-payer need in the lattice. |
| 7 | Athlete-as-operator | UNFALSIFIABLE | UNFALSIFIABLE (see P2). |
| 8 | Free starter -> paid | WEAK | WEAK, agree; no free->paid event defined. |
| 9 | Fear of window | excluded | SURVIVES as exclusion except the "costs if you miss it" line (see P5). |
| 10 | "Coaches don't use services" | WEAK | SURVIVES as stance only; FAQ "Do coaches use this? No" is our position, fine. |
| new | "Most families can run recruiting on their own / themselves" (site/index.html lines 24, 93; compare page "most families should") | - | UNFALSIFIABLE / unsourced quantitative claim. Jev noul 0.65 "unsupported factual claim". No cited source. Violates BRIEF rule 3 spirit (no uncited outcome claims). |

## C. Beat 7 offers (14 stories): implied causation and dark patterns
Template: "The steps in this story, as a playbook. [Name]'s path came down to a few moves you just read about. These playbooks turn those steps into tools your athlete can run: ..."
- Implied causation: REFUTED as "no causal claim". Jev noul 0.70 and 0.72 (two calls, same text) that it implies buying produces the outcome. Mechanism: "[Name]'s path came down to a few moves" + "these playbooks turn those steps into tools" attaches a real athlete's outcome (NFL, Olympics, NBA #11 pick) to the product one sentence after beat 6 denies it. Beat 6 mitigates but the reader's last sentence before the button is the causal frame. Worst cases: coward (NBA lottery), renfrow, marpet, wondolowski, groenewegen (extreme outcomes). Also "a few moves you just read about" overstates: several stories (pirosko, perez, groenewegen) say their recruiting process is NOT sourced, so the "moves" mapped to playbooks (Camp ROI, Highlight Reel) are not moves the source shows.
- Product-to-story mapping: REFUTED for specific pairs where the playbook topic is not a sourced beat (e.g. Highlight Reel & Social for Coward/Wondolowski/Groenewegen; Camp ROI for Perez/Rodriguez) unless beat 3 shows that move. Needs per-story check against beats 3-5.
- Availability: REFUTED as presented. 10 of 12 catalog playbooks are OUTLINE (only Football Junior Year and Eligibility WRITTEN), yet beat 7 lists them at a price with "Get the playbook". The "checkout isn't live, leave email" line rescues payment honesty but not product existence. Jev noul 0.75 deceptive. Must say "in progress / notify me".
- Dark patterns: SURVIVES. No scarcity, timers, confirmshaming, fake counts in beat 7. Decline link neutral per CTA-SCRIPTS.
- Real athletes named in a sales CTA: risk (not a behavioral verdict): using "Hunter's/Cedric's path" as the sales lead-in to a paid product approaches implied endorsement / right-of-publicity use. Flag for Mike/legal.

## D. Funnel / pricing copy
- Trial "$149/yr, renewing yearly until you cancel, reminder 7 days before" : SURVIVES on disclosure (clear auto-renew terms). But it contradicts the lattice/CTA "one-time, nothing recurring" trust posture: strategic inconsistency, not a dark pattern.
- Refund: site has /legal/refund and "30-day full refund" lines; CTA-SCRIPTS says omit unless a real policy exists; W2-funnel flagged the conflict. UNFALSIFIABLE until Mike confirms the policy is real; if not, it is an invented guarantee (REFUTED).
- /welcome "we will email it": REFUTED as a promise while SEND_ENABLED is false (funnel/api/capture.js:22 is a stub). Also checkout line "we'll send the link when it is" has the same dependency.

## Jev log (aside-jev noul, jev-1.14.0, decision_id null; 1=yes)
| Question | Input | noul |
|---|---|---|
| Beat 7 implies buying produces outcome | renfrow beat 7 | 0.70, 0.72 |
| Dark pattern (fear/urgency/loss) | homepage lede "costs if you miss it" | 0.31 |
| Unsupported factual claim | "Most families can run recruiting on their own" | 0.65 |
| Deceptive to sell OUTLINE as available | beat 7 + OUTLINE status | 0.75 |
Jev scores are marginal (0.6-0.75) and dual-judge was not run; they corroborate the textual analysis, they do not decide it.
