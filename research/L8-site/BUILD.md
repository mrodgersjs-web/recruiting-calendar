# L8 site build (2026-11-05, v5)
Generator: `node research/L8-site/build.cjs` (root package.json is ESM). Home = hand-edited site/index.html.
Pages (26): / · /rules · /rules/{baseball,football,track}/{2027..2030} (12) · /math · /camps · /price · /coaches · /compare · /about · /free · /welcome · /legal/{terms,privacy,refund,auto-renewal}
Static files win over L7's vercel.json rewrites; internal links are slashless (trailingSlash:false). .vercelignore excludes research/.
Verify (python http.server :8792, Playwright): 26 pages x 1440/390, 0 console errors, 0 horizontal overflow, mobile menu opens (aria-expanded=true), checkout falls back to the visible form when /api is absent. Shots: shots/.

Folded in:
- Mobile menu <860px (button + aria-controls, Esc closes), site/forms.js.
- Citations: Bylaw 17.2 opted-in roster limits (FB 105, BSB 34, T&F 45 indoor / 45 outdoor, XC 17) checked against the 2026-27 manual text. 85/11.7/12.6 labeled "pre-2025 limits; non-opted-in schools follow settlement terms", linked to the Feb 2026 D1 Q&A.
- L4: forms POST JSON to /api/capture (email, sport, class_year, plan, consent, honeypot) and return the PDF; plan/trial buttons POST /api/checkout {plan}, test mode; 14-day trial auto-renewal disclosure next to the button; /welcome success page; PDF copied to site/downloads/.
- L1: motion.js (FadeUp .6s cubic-bezier(.22,1,.36,1), WAAPI intro with 3.8s failsafe, red spotlight borders, ledger stagger + nearest-date pulse, one-open accordion with 0fr->1fr grid rows, calculator count-up), sport cards, FAQ + ink CTA band, big-wordmark footer, reduced-motion kill switch.
- L6: "No sales call. Nobody phones your kid." in the hero; DIY-kit framing; free-PDF contrast without naming the competitor; 30-day refund line at every buy button; /compare cells taken only from COMPETITORS.md, dated 2026-11-05, "Not checked" where we have no fact; parent pains paraphrased, no Reddit quotes.
- L2 features -> /price table. L5 objection -> FAQ.

Left:
- Prices still proposed; legal pages are drafts; counsel review of the auto-renew copy.
- /api only works on Vercel with env set; locally the forms show a "not connected" message.
- The lead-magnet PDF and data.js only cover Class of 2029 (the capture form sends class_year=2029). Other class years are shifted from 2029 rules.
