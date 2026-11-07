# W2 Funnel and checkout (2026-11-05) — TEST MODE ONLY, nothing deployed, nothing charged, no email sent
## Endpoints (funnel/api, re-exported 1-line in api/)
- POST /api/capture {email, consent:true, sport, class_year, plan} — free giveaway capture. plan accepts giveaway + every offer slug (checkout fallback). Returns 503 "not connected" if RESEND env missing (no fake success). SEND_ENABLED still gates any email.
- GET /api/offers — 17 offers: 12 playbooks, Sport Pack x3 sports ($49), Every Playbook ($99), Sideline trial ($149/yr, 14d). Includes exact trial_disclosure.
- POST /api/checkout {offer, sport?, email?} — legacy {plan:"sideline"} still works. One-time = inline price_data (creates no Products). Sideline uses STRIPE_TEST_PRICE_SIDELINE if set, else inline yearly price_data. Trial: 14d, card up front, ToS consent required, disclosure as Stripe submit text.
- GET /api/order?session_id=cs_test_… and GET /api/deliver?session_id=&slug= — /welcome reads the order and serves PDFs from funnel/deliver/pdfs/<slug>.pdf (private, not in site/). Every download re-checks the Stripe session (complete + paid, or trial no_payment_required), rejects livemode, non cs_test_ ids, and slugs not in the order's metadata.
## Guards
sk_test_ only; account must equal sandbox acct_1TocAGPmz9ZnR3g8 (hard-coded; env cannot redirect it); live sessions/events rejected. Offers whose playbooks aren't WRITTEN + PDF present return 409 "Not available yet" (no "coming soon"); PREORDER_ENABLED=true overrides (test only).
## Env names (match Vercel Preview)
STRIPE_TEST_SECRET_KEY (falls back to STRIPE_SECRET_KEY, the name already created in Preview), STRIPE_TEST_WEBHOOK_SECRET (falls back to STRIPE_WEBHOOK_SECRET), STRIPE_EXPECTED_TEST_ACCOUNT, STRIPE_TEST_PRICE_SIDELINE, RESEND_API_KEY, RESEND_AUDIENCE_ID, SEND_ENABLED, SITE_URL, PDF_BASE_URL. New: PREORDER_ENABLED. EMAIL_PROVIDER_KEY (Preview) is still unread; set RESEND_API_KEY or rename.
## Site
site/checkout.js: any [data-offer] (+data-sport) button checks out; on failure it falls back to the capture form with the honest "Checkout isn't live yet" line. Inserts the trial disclosure right after every sideline button unless a .disclose note is already adjacent. Loaded on /, /price, /calendar. /welcome now a real page (rewrite to index.html removed) with site/welcome/delivery.js.
vercel.json: functions includeFiles bundles funnel/** + CATALOG.json so PDFs and the catalog ship with the functions.
## Tests
`npm test` (node --test funnel/test/funnel.test.js): 16/16 pass, fetch mocked, no network.
## Gaps / needs Mike
1. Only 2 playbooks WRITTEN and 0 PDFs in funnel/deliver/pdfs, so every paid offer currently returns 409; drop rendered PDFs in to enable. 2. Sport Pack/Every Playbook/Sideline prices unapproved. 3. Creating sandbox price + webhook is a test-mode action needing Mike's key (step-up 2FA). 4. Existing price page says "30-day full refund" — CTA-SCRIPTS says omit unless a real policy exists; flag for Mike. 5. Counsel review of auto-renew copy. 6. Fulfilment email after purchase is not wired (SEND_ENABLED off).
