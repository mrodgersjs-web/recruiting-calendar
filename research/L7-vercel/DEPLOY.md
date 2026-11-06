# L7 Vercel hosting (2026-11-05 MT)

- Preview URL: https://recruiting-calendar-ol2ssgwl9-michael-rodgers-projects-e4209a00.vercel.app
  (status Ready; behind Vercel Deployment Protection, so anonymous curl gets 302 to SSO; logged-in browser = 200)
- Verified: /rules/football/2029 returned 200 and rendered the Class of 2029 date ledger (11 dates, verified 2026-11-05). Screenshot: preview-rules-football-2029.png
- Project: recruiting-calendar, id prj_fH00YUAIBlgV40gedKIUpoAjWzTz, team team_4uvtoN6Mzf0JCzyR3ySQvXc5 (michael-rodgers-projects-e4209a00)
- Repo: https://github.com/mrodgersjs-web/recruiting-calendar (PRIVATE), branch main
- Registered in ~/Developer/rig-intelligence/registry/workstation-repositories.json as id recruiting-calendar (backup .bak-20261106-recruiting-calendar). Steward git_guard PASS on commit + push.
- First commit used RIG_JEV_PRECOMMIT_SKIP=1: 4.5M-char initial import, gate saw a truncated view (decision 311039). Reason is in the commit message.
- No production deploy, no domain attached, nothing bought.

## Layout
- site/ = static output (vercel.json outputDirectory), cleanUrls on, HSTS/nosniff/DENY frame/referrer/permissions headers.
- /rules/:sport/:class -> /index.html?sport=&class= (app.js renders it). /welcome -> index.html.
- api/*.js are one-line re-exports of funnel/api/*.js (capture, checkout, portal, stripe-webhook incl. bodyParser:false config). Lane 4 adds a file in funnel/api, then add a matching 1-line file in api/.
- CLI: /Users/rig128gb/Developer/jacob-x-studio/dashboard/node_modules/.bin/vercel (not on PATH), logged in as rodgemd1-9353.

## Env vars (Mike sets values; Preview placeholders = PLACEHOLDER_SET_BY_MIKE)
Created (Preview, Secret): STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET, EMAIL_PROVIDER_KEY.
NOTE: L4's code actually reads STRIPE_TEST_SECRET_KEY, STRIPE_TEST_WEBHOOK_SECRET, STRIPE_TEST_PRICE_SIDELINE, STRIPE_EXPECTED_TEST_ACCOUNT, RESEND_API_KEY, RESEND_AUDIENCE_ID, SEND_ENABLED, SITE_URL, PDF_BASE_URL. Either rename in code or set these names too. Must be sk_test_ only (checkout refuses live keys).
Set one: `vercel env add STRIPE_TEST_SECRET_KEY preview` (paste value; repeat for production when approved).

## Promote to production (ONLY after Mike's approval)
cd ~/Developer/recruiting-calendar && /Users/rig128gb/Developer/jacob-x-studio/dashboard/node_modules/.bin/vercel promote https://recruiting-calendar-ol2ssgwl9-michael-rodgers-projects-e4209a00.vercel.app --yes
(or a fresh build: `... vercel --prod`). Production env vars must be added first. Custom domain (TheRecruitingCalendar.com, not bought) is a separate approval: `vercel domains add <domain>`.
