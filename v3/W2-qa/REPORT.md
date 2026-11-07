# W2-qa REPORT (2026-11-05, continuous QA)
Suite: ~/.rig/e2e-harness/suites/recruiting-calendar-v3 (tests/v3.e2e.ts, 8 deterministic expect() tests, no model judging).
Target: ~/Developer/recruiting-calendar/site served at http://127.0.0.1:4519 (run: v3/W2-qa/run.sh). Override: RIG_E2E_RC_BASE / RIG_E2E_RC_SITE.

## Checks
1 ring visible and active athlete changes after 6.5s (autoplay 5s) | 2 pick -> URL has "story", >=3 visible .beat after scroll
3 [data-add] click raises [data-bag-count] by 1 | 4 [data-checkout] lands on cs_test Stripe or /checkout|/api/checkout|#join, never cs_live
5-6 every page under site/: zero console.error/uncaught errors, no horizontal overflow @1440 and @390
7 every [data-rule]/.rule/.evrow/[data-fact] and every "Bylaw N" text block has an http citation link
8 site/IMAGES.json exists; generated images only for composites; every generated image shown carries "Illustration"

## Trust proof (fails on purpose)
- Demo (v3/W1-motion/demo): checks 1-3 GREEN (run-demo-green.log).
- Mutated copy (autoplay off, bag counter attr renamed): checks 1 and 3 FAIL as expected (run-deliberate-fail.log). Suite catches real breaks.

## Run 1 vs current site (22:53 MT): 5 FAIL / 3 PASS (run1-site.log)
FAIL: no ring; no athlete pick/story; no bag; checkout stays on / with 1 console error; IMAGES.json missing.
PASS: console+overflow on all pages at 1440 and 390; citation links.
Sent to W2-1 (2amyi8vy3GLeRgRL) with concrete selectors.

## Continuous loop
loop.sh runs every 20 min, appends to runs.log, copies last-run.log. Stop: `touch v3/W2-qa/STOP` after W2-1 reports done and a green run.
Stopped: STOP touched after W2-1 reported done.

## Run 2 on 3ab4915: 5 FAIL / 3 PASS
FAIL: checkout.js SyntaxError from an apostrophe (every page), /calendar TypeError on a null element, no [data-offer] on home, D3 Bylaw 15 had no citation link, 2 beats per story. W2-1 says 2 beats is the design, so the bar is now 2 (a judgment call, flag it if the spec says 3+).
## Final run on cbb09b0: 8/8 GREEN (run-final-green.log)
Checkout POST to /api/checkout is stubbed in the test (route.fulfill), so it proves the button fires the POST, not that a live Stripe test session gets created.
