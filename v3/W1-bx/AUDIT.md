# Bias audit of persuasion claims (bx-bias-auditor method, 2026-11-05)
Verdicts: SUPPORTED / WEAK / REFUTED / UNFALSIFIABLE. "Support" here = mechanism has published support AND our own data points the same way; no claim has site data yet.
| # | Claim used in the scripts | Verdict | Basis / note |
|---|---|---|---|
| 1 | Trust is the binding barrier for this buyer | WEAK | Jev choice p=0.66, conf 0.55 (marginal) + PV Pain 1-2 verbatims; n~30 Reddit comments, self-selected complainers. Testable via P1. |
| 2 | Identifiable single stories persuade more than statistics (beat 1) | SUPPORTED (literature), unmeasured here | Identifiable-victim effect is from charity giving; transfer to purchase intent is an assumption. Boundary: composites may weaken it. |
| 3 | Two-sided messages ("what this doesn't prove") raise trust with skeptical audiences (beat 6) | SUPPORTED (literature) | Meta-analytic support for refutational two-sided messages; effect small and depends on the downside being refuted/minor. |
| 4 | Showing a cited bylaw raises credibility (beat 4) | WEAK | Plausible (verifiability); PV Desire 3 supports demand for sport-specific rules; no direct test. P1 tests it. |
| 5 | Bundle framing ($25 vs $37 separately) | SUPPORTED as arithmetic; WEAK as persuasion | BP #20 = $25; parts #10 $7 + #9 $9 + #16 $9 + #15 $12 = $37. Draft 1 listed three items at $25 (no saving, false framing): fixed. Show the real separate sum only. |
| 6 | Low price shrinks the co-payer veto | WEAK | Committee logic; no B2C threshold data. P4 tests it. |
| 7 | Naming the athlete as operator turns a veto into ownership | UNFALSIFIABLE as stated; made falsifiable as P2 | Autonomy framing is a hypothesis; P2 gives the kill rule. |
| 8 | Free starter first increases later paid purchase (foot-in-door) | WEAK | Foot-in-the-door effects are small and inconsistent; could also cannibalize. Track free->paid within 30 days. |
| 9 | Fear of missing the recruiting window motivates purchase | REFUTED for our use | Not refuted as a motive, but using it is excluded by the no-fake-urgency rule; only factual dated rules allowed (P5). |
| 10 | "Coaches don't use services" positions us well | WEAK | Second-hand (PV Pain 3, explicitly "not verified"). Use only as our own stance, never as a quoted coach claim. |

## Dark-pattern check on CTA-SCRIPTS.md
No scarcity, no timers, no confirmshaming, no hidden recurring charge, test-mode disclosed. PASS on self-read; independent verification below.

## Verification
Jev (jev-1.14.0, 2026-11-05) on CTA-SCRIPTS.md dark-pattern question: noul 0.05 (low probability of a dark pattern). decision_id null. bx_verify / bx_falsify gateway runs NOT executed this wave: lattice predictions are DEFERRED for independent falsification, not self-certified.
