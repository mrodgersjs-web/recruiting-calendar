# The Commit Book: project handoff

Status recorded 2026-11-08. This is a working handoff, not launch approval. Verify live state before acting.

## Project and access

- Existing private repository: https://github.com/mrodgersjs-web/recruiting-calendar
- Site: https://recruiting-calendar.vercel.app
- The repository is private. James needs a GitHub account with explicit repository access before a link will work; an email address alone does not establish access.
- In Aside, open the project/repository if it is available to your account, then ask: “Read COMMIT-BOOK-HANDOFF.md and inspect the current repository and live site. Explain what is ready and what is blocked; do not enable checkout or publish without approval.” Aside's access depends on the account and permissions actually connected. Do not share credentials.

## Where the work lives

- `BRIEF.md`, `research/`: original brief and research, including proposed business plan.
- `site/`: generated site and assets; inspect source generators before editing generated pages.
- `funnel/`: checkout, delivery, capture and test code.
- `v3/W6-problems/`: dated, directional parent-problem research and group metadata. Sample mentions are not representative population statistics.
- `v3/W7-segments/`, `v3/W7-marketing/`: segmentation and marketing research. Paying-family estimates and conversion scenarios are assumptions, not validated forecasts.
- `v3/W7-access/`, `v3/W7-recruitiq/`, `v3/W7-personalization/`: solution research and implementations.
- `v3/W8-offerings/`: product concepts and deliverable drafts. BUILT means a file exists, not that it passed content, legal or fulfillment review.
- `v3/W11-site-overlay/`: added site pages and assets.
- `v3/W12-library/`: library generator and tests.
- `v3/W12-journey/`: buyer-journey working drafts. The currently uncommitted draft contains unsupported sizing and contradictory price claims; do not use its figures or readiness claims without source review.
- `v3/HEARTBEAT/SCORECARD.md`, `v3/STORY-FLAGS.md`: prior visual scoring and story caveats.

## Most recent established work

The project was rebranded The Commit Book. The old third-party resources directory was removed from the site and redirected to the library. Contact Log and Red Flags were made available as free draft downloads; their content still needs independent review. Other tools were presented as notify-only. Prior production and test observations are dated, not a guarantee of current operation.

## Launch blockers

1. **Price conflict:** local `/calendar`, `/price`, library materials and journey drafts do not agree. `funnel/lib/offers.js` sets a proposed $149/year Sideline and lists Pathway at $499/year as planned, not for sale. A separate $99 Sideline founding presentation exists. Do not choose a price or publish a sales promise by inference.
2. **Payments:** checkout is designed for Stripe test mode and is gated. The subscription API requires consent fields which the inspected frontend does not send. The W8 tool slugs are not registered checkout SKUs. A green mock test is not an end-to-end payment or fulfillment receipt.
3. **Fulfillment:** only two playbook PDFs were observed locally. Independently audit deliverable completeness, recruiting rules, NIL/tax and legal claims, rights, accessibility, and delivery after a test purchase before selling. Do not expose paid drafts as public downloads.
4. **Email and support:** capture and follow-up provider configuration, actual delivery, receipt handling, unsubscribe and a monitored support address require verification.
5. **Research and images:** segment sizing is hypothetical; social observations are directional; synthetic panel scores are not user feedback. Review image rights, real-athlete representations and composite labels before launch.
6. **Shared state:** uncommitted changes exist in the journey and other generated files. Review them before staging. Do not assume generated HTML accurately reflects current JSON.

## Evidence and next steps

From `funnel/`, `node --test test/funnel.test.js` reported 27 passing tests on 2026-11-08; these are mocked tests, not proof of production readiness. Agree the price and offer scope, independently audit the exact deliverables, fix consent and SKU/fulfillment paths, then run sandbox checkout-to-delivery tests and an independent review before any live-payment decision. Preserve the payment guard until those checks pass.

This file summarizes project context, not a complete export of chats, private memories or all assets. Review material for secrets, personal information, rights and recipient access before adding or sharing it.
