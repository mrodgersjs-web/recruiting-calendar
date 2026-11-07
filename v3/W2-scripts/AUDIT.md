# W2-scripts AUDIT (2026-11-05): bx-bias-auditor then bx-falsifier, per story
Method note: the bxskill gateway tools (bx_bias_audit / bx_falsify) were not loadable in this subagent session, so both passes were run by hand against each skill's SKILL.md method (claim extraction, framing fidelity, asymmetric search for counter-evidence, citation check). Treat as a self-audit, not an independent judge: an independent bx_falsify run is still owed before publish.

## Pass 1: bias auditor (framework claims in copy)
| Check | Result |
|---|---|
| Survivorship / availability: famous outcomes (NFL, NBA, MLS, Olympics) can make rare endings look typical | MITIGATED: beat 5 says "extremely rare / not typical" on Renfrow, Marpet, Coward, Wondolowski, Rodriguez; beat 6 says the ending is not typical. RESIDUAL: carousel selection itself skews to stars (9 of 13 real athletes reached pro/national level). Recommend W2 carousel add 2+ non-pro athletes in a later wave. |
| Status anxiety / D1-as-win framing | PASS: every beat 5 names the level as a destination, not a consolation. |
| Loss aversion / fear inflation | PASS: no "most kids miss out", no uncited stats, no scarcity or countdowns. Beat 7 matches CTA-SCRIPTS banned list. |
| Causal claim from rule or playbook | PASS: beat 4 says the rule did not cause the outcome; beat 6 says the athlete never used our playbooks. |
| Confirmation bias in our own sourcing (choosing details that fit the "agency" story) | WEAK on Renfrow beat 3, Coward beat 3, Butler beat 3: "the choice that mattered" is our framing, not the source's. Softened Renfrow; others stay narrowly attributed. |
| Inferred identity | FIXED: Perez "Hispanic" label dropped; only "Colombian heritage" as stated in the feature. |

## Pass 2: falsifier (each factual claim attacked)
| Story | Verdict | Notes |
|---|---|---|
| Renfrow | SURVIVES | 3 independent outlets. Beat 4 rule is current; recruit year (c.2013) precedes the current rule, stated as rule then / rule now. |
| Groenewegen | SURVIVES (narrow) | Recruiting path single-source (gophersports 2015, attributed in copy); bio facts double-sourced (Softball Canada, COC). |
| Lowe | SURVIVES | HS corrected to La Costa Canyon (W1 "San Diego" was imprecise). 4 sources incl. UCLA, ESPN, USA Volleyball. |
| Pichardo | SURVIVES (narrow) | SI + one profile; national-team claim rests on the profile site. Recommend a USA Baseball roster link. |
| White | SURVIVES | 4 sources. |
| Pirosko | SURVIVES (narrow) | Second source added (Gannon signing release 2018-05-02). Recruiting process not sourced; beat 2-3 say so. |
| Marpet | SURVIVES after correction | W1 HS "Hackley" was WRONG; Hastings High School (NY Post, Wikipedia). "small public school" softened to "small school" (public status not sourced). |
| Rodenfels | SURVIVES | 3 sources. |
| Perez | SURVIVES (narrow) | No independent 2nd source (Oglethorpe page is a repost). School stats PDF confirms roster/goalie only. |
| Coward | SURVIVES | Flag resolved: Willamette -> Eastern Washington -> Washington State, 5 sources. |
| Rodriguez | HOLD | Facts survive (3 sources) but beat 4 has no cited NAIA rule in site/data.js. Cannot ship until a NAIA bylaw row is added. |
| Butler | SURVIVES | NFHS + Marquette. Beat 4 uses D1 core-course rule (general, applies to D1 entry) with note that JUCO transfer rules are not covered. Weakest rule fit of the set. |
| Wondolowski (NEW, soccer, real D2) | SURVIVES | NCAA.com + De La Salle alumni profile. HS city stated only as California (sources conflict-free but city not stated). |
| Composite "Maya" | SURVIVES as composite | Labeled in hook and on every image; sources are patterns, outcome marked illustrative. |

## QA checklist (SCRIPT-FRAMEWORK)
- Every fact URL + retrieved date: yes (SCRIPTS.json sources[]).
- No quotes: yes (no quote characters in copy; build check).
- Beat 4 bylaw matches site/data.js: yes for 12; Rodriguez HOLD.
- Beat 6 present, beat 7 no causal claim: yes, all 14.
- Level coverage: D1 (Renfrow, Groenewegen, Lowe, Pichardo), D2 (White, Pirosko, Wondolowski, composite), D3 (Marpet, Rodenfels, Perez, Coward), NAIA (Rodriguez, HOLD), JUCO (Butler). NAIA slot is empty until Rodriguez clears.
- Word counts: beats 1-5, 7 all 60-83 words (Rodenfels beat 7 82, Groenewegen beat 7 80). Beat 6 is a fixed 62-word line.
- Narration: 133-204 words at ~2.5 w/s = 53-82 s. Renfrow (53 s) runs short of the 60 s floor; W2-6 may slow the read or add a line.
- Playbook status: most mapped playbooks are OUTLINE in CATALOG.json; only Football Junior Year and Eligibility are WRITTEN. Selling an OUTLINE playbook needs the checkout copy to say "notify me" (already the test-mode line).
