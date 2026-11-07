# L4 Funnel — The Recruiting Calendar (2026-11-05)
Pattern copied from the RIG GrokBot launch: free giveaway captures email, contact/capture form always visible, plan buttons feed the same form (with `plan` field), lower tiers carry zero owner time, no "coming soon" on purchase controls (disabled is fine), and **price approval is not a production release**. Status: everything here is local/test. Nothing deployed, sent, or charged.

## 1. Free giveaway
| Candidate | Pro | Con |
|---|---|---|
| A. "Your kid's recruiting calendar, {sport}, Class of {year}" (PDF) | Personal, maps 1:1 to the paid product, built straight from site/data.js, captures sport+year for segmentation | Only 3 sports, class 2029 in data today |
| B. "The 2 hard eligibility deadlines" checklist | Short, urgent | Thin; gives away the core fear without showing the product |
| C. "Roster math cheat sheet post-House" | Topical | Roster/aid numbers would need fresh sourcing per sport; risk of stale or invented figures (rule 3) |

**Pick: A.** It is the product in miniature, every row already has a bylaw + URL, and the sport/year fields segment the list for the trial email. B can be a section inside A (HARD DEADLINE rows are highlighted).

Built: `funnel/lead-magnet/generate.cjs` reads site/data.js, keeps only entries with `rule` + `citation_url` (30/30 today: football 11, baseball 10, track 9), labels `kind:"projected"` rows "PROJECTED (not yet published)" and `action` rows "Recommended (not NCAA)", adds a no-promise disclaimer. PDF: `research/L4-funnel/recruiting-calendar-class-2029.pdf` (all three sports, one per page). Per-sport HTML in `funnel/lead-magnet/out/`. Gap: data.js has class 2029 only, so the "Class of {year}" picker must be limited to 2029 until other years are verified.

## 2. Free trial that auto-renews into Sideline
- **Length: 14 days.** Under California's 31-day threshold for the special trial-end notice (BPC 17602(b)(1)), but we send one anyway at day 7 (safe under any reading of the 3-21 day window).
- **Card up front: yes** (`payment_method_collection: always`). Required for a true auto-renew; trades lower trial starts for higher paid conversion. Alternative: no card + `missing_payment_method: cancel` (no auto-renew, just a nudge). Mike's call.
- **Disclosure at checkout (clear and conspicuous, next to the button):** "Free for 14 days, then $149 per year, renewing yearly until you cancel. Cancel any time online in one click." Plus a required consent checkbox (Stripe `consent_collection`). CA requires express affirmative consent and an acknowledgment email with terms + how to cancel; keep proof of consent (Stripe session record).
- **Notices:** day 7 of trial (trial-ending email, draft 3); annual renewal notice 15-45 days before each yearly renewal (CA BPC 17602(b)(2), required because Sideline's term is one year) — schedule at 30 days; receipt on each charge.
- **Cancellation:** online, Stripe customer portal, cancel-at-period-end, no retention survey gate. Link in every billing email and the account page. Online signup must be cancellable online (CA ARL).
- Sources: CA BPC 17602 (https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=BPC&sectionNum=17602.&article=9), AB 2863 effective 2025-01-01 (https://leginfo.legislature.ca.gov/faces/billTextClient.xhtml?bill_id=202320240AB2863), CA AG consumer alert 2025-09-04 (https://oag.ca.gov/news/press-releases/attorney-general-bonta-issues-consumer-alert-california%E2%80%99s-automatic-renewal-law). Federal: FTC click-to-cancel rule was vacated, but ROSCA still applies (Clark Meyers summary, https://clarkmeyers.com/california-automatic-renewal-law-compliance). Other states (NY, CO, VA, etc.) have similar laws; designing to CA covers most. Not legal advice; have counsel review before launch.

## 3. Stripe plan (TEST MODE ONLY)
Coordination per the Stripe notes (finance-ops memory, 2026-11-05): account of record for live is `acct_1TocAABrLv42sOK8` — **not touched**. The live account already has 37 products/48 prices; search before creating anything when live is approved. Test work goes to the sandbox `acct_1TocAGPmz9ZnR3g8`. `api/checkout.js` refuses any non-`sk_test_` key and any account id other than the sandbox; the webhook rejects `livemode` events. Stripe key writes need Mike's step-up 2FA, so never assume unattended key creation.
Steps (test): create product "Sideline" + yearly price $149 in sandbox -> set `STRIPE_TEST_PRICE_SIDELINE`; Checkout `mode=subscription`, `subscription_data.trial_period_days=14`; enable Customer portal (cancel at period end, update card); test webhook endpoint for `checkout.session.completed`, `customer.subscription.trial_will_end`, `invoice.paid`, `invoice.payment_failed`, `customer.subscription.deleted`; test clocks to simulate trial end and renewal. Founding $99 = a coupon on the first year (if approved). Do NOT add a 4th live webhook; the live account already has three.

## 4. Emails
`funnel/emails/DRAFTS.md`: welcome, day-3 value, trial-ending notice, renewal receipt. Plain copy, no scholarship promise, every price labeled proposed. Drafts only.

## 5. Email-capture endpoint
`funnel/api/capture.js` (Vercel Node function): validates email, honeypot, consent flag, sport, plan (plan buttons post here); stores to provider; returns PDF link. Sending disabled behind `SEND_ENABLED`.
**Provider recommendation: Resend** (Audiences + transactional in one API; free tier ~3,000 emails/mo, Pro ~$20/mo for 50k — verify current pricing before buying). Alternatives: Loops (~$49/mo, nicer sequences), Buttondown (~$9/mo, newsletter-first), or Supabase table ($0, but you build sending). Prices are estimates from memory of vendor pages, not re-verified today. Lead fields: email, sport, class_year, plan, consent timestamp.

## Files
funnel/lead-magnet/{generate.cjs,render-pdf.sh,out/}, funnel/api/{capture,checkout,portal,stripe-webhook}.js, funnel/emails/DRAFTS.md. All APIs pass `node --check`; none deployed or run against Stripe.

## Needs Mike
1. Giveaway pick A and the PDF text. 2. 14-day trial, card up front. 3. Sideline $149/yr and $99 founding (still unapproved). 4. Email provider + spend (Resend). 5. Exact text of all 4 emails. 6. Creating sandbox product/price/webhook (test). 7. Any live product/price/deploy (separate approval). 8. Counsel review of auto-renew copy.
