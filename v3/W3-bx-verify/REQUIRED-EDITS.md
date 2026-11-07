# Required edits (W3 bx-verify, 2026-11-05) in priority order
1. Beat 7 template (all 14, W2-scripts/build.cjs / stories-src*.cjs): remove "[Name]'s path came down to a few moves you just read about" and "turn those steps into tools". Replace with: "Want to work on the steps from this story? These playbooks cover them. This athlete did not use them." Keep beat 6 directly above.
2. Beat 7 playbook mapping: list only playbooks whose topic matches a SOURCED beat 3-5 move in that story; drop Highlight Reel / Camp ROI where the source shows no such move (pirosko, perez, groenewegen, coward, wondolowski, rodriguez: re-check each).
3. OUTLINE playbooks: label "In progress, get notified" with button "Notify me", not "Get the playbook", for the 10 OUTLINE items in W1-playbooks/CATALOG.json.
4. Homepage + compare: remove or source "Most families can run recruiting on their own / themselves / most families should". Suggested: "You can run recruiting yourself. This is the calendar, the rules and the tracker for it."
5. Homepage lede "It also tells you what each one costs if you miss it": rewrite to "It also says what changes after each date." (removes loss framing; keeps P5 factual-date only).
6. Refund: Mike confirms the 30-day refund policy is real, or remove all refund lines and /legal/refund.
7. /welcome "we will email it" and checkout "we'll send the link": true only once SEND_ENABLED is approved; until then say "We saved your email. Sending isn't switched on yet."
8. Lattice (W1-bx/LATTICE.md): P1/P2 need a real control arm (A/B toggle of the trust block and operator line) or are relabeled "not testable on current build". Replace n=400/300 with a power calc (detect 1 pt at observed base rate) or state "directional only". P3 needs randomized first story. P4 deferred until live Stripe. P5: drop the untested "urgency would not" half or add it as an explicitly-not-run arm.
9. Rodriguez beat 4: still HOLD (no NAIA rule in site/data.js).
10. Flag for Mike: named real athletes as the lead-in to a paid offer (implied endorsement risk); and $149/yr trial vs "nothing recurring" trust posture.
