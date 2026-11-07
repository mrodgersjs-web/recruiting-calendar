# W3 Legal and Integrity Review (2026-11-05)
Reviewer: Aside agent, NOT a lawyer. Every item marked COUNSEL needs sign-off by a licensed attorney before live payments.
Scope read: v3/BRIEF-V3.md, site/ (index, price, free, calendar, legal/*, assets/ring.js, assets/stories.js, checkout.js, forms.js), funnel/api/capture.js + portal.js, v3/W2-funnel/COPY.md, v3/W2-images/IMAGES.json, v3/W2-video/manifest.json + gen.py.

## Summary table
| # | Issue | Severity | Counsel |
|---|---|---|---|
| 1 | 13 real named athletes (Renfrow, Groenewegen, Lowe, Pichardo, White, Pirosko, Marpet, Rodenfels, Perez, Coward, Rodriguez, Butler, Wondolowski) shown on ring cards and story panels that end in a paid playbook, with NO "not affiliated / not endorsed" line next to any story. Card label is only "Real athlete · sourced". | HIGH | YES (right of publicity / Lanham Act false endorsement; using names adjacent to a buy button is the core risk) |
| 2 | Each real-athlete video (real-*-720p.mp4) is kinetic typography of the name with OUR logo end card. Name + our logo = implied sponsorship. | HIGH | YES |
| 3 | Price conflict: home card "$99/yr ~~$149~~" vs trial disclosure "then $149 per year" (checkout.js, COPY.md) vs band "then $149 a year (proposed)". Disclosure must state the price actually charged. Strike-through $149 is a former-price claim (16 CFR 233.1) unless $149 was really charged. | HIGH | YES (ROSCA / BPC 17602 "clear and conspicuous" terms) |
| 4 | Trial disclosure promises "We email you 7 days before the trial ends" and auto-renewal page promises "We email you before each renewal", but capture.js sends nothing (SEND_ENABLED=false). A promised notice that cannot fire is a deceptive-practice risk and BPC 17602(a)(3)/(4) trial-notice duty. | HIGH | YES |
| 5 | Cancellation method inconsistent: checkout "Cancel any time online in one click" vs /legal/auto-renewal "Cancel any time by email or from your account". portal.js exists (Stripe test portal) but no visible account/cancel link on site. CA 17602(d) requires online cancel for online sign-ups. | MED | YES |
| 6 | No affirmative consent to auto-renewal terms before charge (free form consent box is email-only). BPC 17602(a)(2) / ROSCA require express informed consent. Stripe Checkout must carry a required checkbox or terms_of_service consent with the disclosure text. | HIGH (before live keys) | YES |
| 7 | Refund wording: approved policy = 30-day full refund. /legal/refund OK. /legal/auto-renewal says only "A renewal charged within the last 30 days is refundable" (narrower, reads as renewals-only). COPY.md line 8 still flags the 30-day line as "omit unless real policy" (stale flag; policy is approved). | MED | no (exact-text fix) |
| 8 | Privacy policy vs collection: says "email and sport and class year". Actual: also plan/offer and consent flag; stored in Resend Audiences (processor not named); Stripe processes payment data (not named); Vercel hosting logs IP. No contact address other than a .example placeholder. No CCPA/"do not sell or share" notice, no retention period. | MED | YES (CCPA/CPRA applicability) |
| 9 | COPPA: form collects only email; copy addresses parents; no age gate. Class-year 2029 kids are ~13-14, but we do not collect from them. Low risk; add a parents-only line. | LOW | no |
| 10 | Trademarks: NCAA/NAIA/NJCAA named nominatively with a sitewide "Not affiliated with or endorsed by the NCAA, NAIA or NJCAA" footer: good. School names (Clemson, UCLA, Brown, Marquette, etc.) appear factually; no school logos/marks found in IMAGES.json (prompts forbid logos, numbers, text). Header "Rules checked against the 2026-27 NCAA Division I Manual" is nominative and fine. Add schools to the non-affiliation line. | LOW | no |
| 11 | Generated imagery: all 16 images real_person=false, composites aged 20-22, no brand marks; labeled "Illustration". Videos: "no faces" per manifest. Complies with brief rule 2. Verify visually that "Illustration" tag is rendered top-left on every image (ring.js labels cards "Illustration · Composite"). Prompt says "Nike-campaign editorial lighting": style reference only, no Nike mark in output; keep "Nike" out of any public copy. | LOW | no |
| 12 | Minors: no minors depicted; composite ages 20+. Real athletes' stories include HS-era facts (they are adults now): acceptable, sourced. No Jacob found. | OK | no |
| 13 | FTC endorsements (16 CFR 255): no testimonials or member counts found. Real-athlete stories must not be framed as using/recommending our playbooks; "In this story: playbooks" panel next to a real name can read as endorsement -> fix #1 covers it. Composite story must say it is a composite (it does). | MED | YES (bundled with #1) |
| 14 | All legal pages say "Draft for review. Not yet in effect." while the site is live with prices and trial buttons. Fine for email-capture mode; must be finalized before live Stripe keys. | MED | YES |

## Exact-text fixes (applied via site lane where marked APPLY)
F1 (APPLY, #1/#2/#13): directly under every real-athlete story header and on every real-athlete ring card hover/panel, add:
"Public facts only, sourced below. [Name] is not affiliated with, has not endorsed, and was not paid by The Recruiting Calendar. [School] and the NCAA/NAIA/NJCAA are not affiliated with us."
Real-athlete videos: replace end card logo with that same sentence, or drop the logo end card. (Video re-render is a W2-video task; counsel decides whether names can sit next to "Get the playbook" at all; conservative option: move the playbook panel below a divider headed "Playbooks for parents (not part of [Name]'s story)".)
F2 (APPLY, #3): pick one price. If $99 is the charge: trial disclosure = "Free for 14 days, then $99 per year, renewing yearly until you cancel. Cancel any time online in one click. We email you 7 days before the trial ends." and remove the $149 strike-through unless $149 was actually charged. Price choice is Mike's; lane must not guess. Do NOT apply until Mike names the price.
F3 (APPLY, #5): /legal/auto-renewal body =
"Paid memberships start with a 14-day free trial, then renew automatically every year at the price shown at checkout until you cancel. We email you 7 days before the trial ends and before each renewal. Cancel any time online from the link in your receipt email, or by emailing us; cancelling stops the next charge. You can get a full refund within 30 days of any charge, including a renewal."
F4 (APPLY, #7): /legal/refund add: "This covers the first purchase and every renewal."
F5 (APPLY, #9): under every email form: "For parents and guardians. We do not knowingly collect information from children under 13."
F6 (APPLY, #10): footer line becomes "Not affiliated with or endorsed by the NCAA, NAIA, NJCAA, any college, or any athlete named on this site."
F7 (APPLY, #8): /legal/privacy body =
"We collect your email, the sport, class year and plan you choose, and whether you agreed to email. We store it with our email provider (Resend) and, if you buy, Stripe processes your payment; we never see your card number. Our host (Vercel) keeps standard server logs. We do not collect athlete names, film, stats or photos, and we do not sell or share personal data. Ask us to see or delete your data by email and we will."
F8 (#4, NOT applied): until SEND_ENABLED is true, the "We email you 7 days before" promise is false. Either ship the reminder email or keep checkout off (current test-mode state). Blocking for live keys.
F9 (#6, NOT applied): Stripe Checkout must use consent_collection.terms_of_service=required with custom_text carrying the exact trial disclosure. Code change, counsel to approve text.
F10 (COPY.md): delete the stale line-8 flag; 30-day full refund is approved.

## Not found / not checked
- Did not render every page visually; checked HTML/JS text. Did not verify license status of any press imagery (none found in media; all real-athlete media is typography).
- Did not verify each sourced fact URL (that is W1-stories/QA).
