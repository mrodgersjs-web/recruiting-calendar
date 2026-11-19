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


## CopilotKit + vercel-labs/ui integration (2026-11-19)

Status recorded 2026-11-19. Working notes from the v1.1 lane. Not launch approval. The integration is uncommitted. HEAD is still `4d2afba492169ac0379da116e60c9fde3d83fbbd` on `feat/commitbook-chatbot-kokonut`.

### What landed in the working tree

Not committed. `package.json` is now `commit-book` 1.1.0.

- `app/api/copilotkit/route.ts`: CopilotKit runtime, AG-UI agent, Vercel AI SDK `streamText`. Returns 503 without `OPENAI_API_KEY` and 429 on the existing IP limit.
- `lib/copilotkit-service.ts`, `lib/copilotkit-types.ts`, `lib/content-search.ts`: site KB, five internal reel drafts cited as "internal research draft, not published", approved hosts only (`ncaa.org`, `naia.org`, `njcaa.org`, this site).
- `package.json` and `package-lock.json`: `@copilotkit/runtime`, `@copilotkit/react-core`, `@copilotkit/react-ui` at 1.89.0; `@ag-ui/client` 1.0.5; `@ui-sdk/react` and `@ui-sdk/core` at 0.1.0-beta.10; `@playwright/test` 1.65.1.
- `tests/chatbot.spec.ts`, `e2e.config.ts`, `.e2e/dev-server.mjs`, `.e2e/openai-stub.mjs`, `.e2e/tsconfig.check.json`: Playwright harness. A5 authored it and typechecked it. A5 did not run it.
- `docs/BRIEF.md`: one-page v1.1 brief.
- `test-results/`: leftover from the failed Playwright run. Untracked. Not a product file.

No component file imports `@ui-sdk/*` or `@copilotkit/react-ui`. The visible panel is still the Kokonut launcher on `/api/chat`.

### Agents

- A1: no report in the drop folder by 2026-11-19T02:08Z.
- A2: no report by the same time. Dependency files are on disk; this note does not invent an A2 write-up.
- A3 (`a3-vercel-ui-audit.md`): PARTIAL_ADOPT. vercel-labs/ui does not export Conversation, PromptInput, Response, Sources, or Actions. Chrome only (Dialog, Accordion, TriggerMenu, Textarea). Do not replace the Kokonut message list. That chrome was not applied.
- A4 (`a4-deploy-readiness.md`, checked 2026-11-19T01:38Z): push stays BLOCKED. `remote_writes_enabled` false, `block_public_pushes` true, no recruiting-calendar grant. Kill switch ACTIVE means the pause file is absent. It is not the deny. Ready to push: no. Ready to preview deploy: no. Vercel access token expired 2026-11-19T01:08:56Z. `vercel` is not on PATH.
- A5 (`a5-e2e-report.md`): seven cases authored. Compile check passed. Not an executed suite.
- A6 (`a6-flawlessux-review.md`): rendered the current panel. P0: `aria-modal` with no focus move, no inert background, focus not restored. Placeholder 2.43:1. Slash descriptions 2.82:1. Launcher covers "Playbooks for Football" at 1440. "Verified KB" 4.37:1.
- A7 (`a7-verification-report.md`, run-only, ~18:38-19:05 America/Denver): typecheck exit 0, lint exit 0, `next build` exit 0 (97 pages). GET `/` on port 3138 returned 200. POST `/api/chat` and POST `/api/copilotkit` returned 503 `provider_not_configured` with no key in the shell. Playwright (`npx playwright test --config=e2e.config.ts`) failed 7/7, `net::ERR_CONNECTION_REFUSED`. Cause: `e2e.config.ts` calls `freePort()` at module scope and workers re-evaluate the config. Harness bug, not an app 500. Dev server was killed. Port 3138 was free afterward.

### Open risks

- No green e2e. Do not cite the Playwright run as proof the panel works.
- Build warning, not a failure: critical dependency expression in `@ai-sdk/google-vertex`, imported through `@copilotkit/runtime` into `app/api/copilotkit/route.ts`.
- CopilotKit telemetry logged as on. Opt out with `COPILOTKIT_TELEMETRY_DISABLED=true`.
- Live answers stay 503 until `OPENAI_API_KEY` is set. That write is still a secret and a paid key.
- Push still needs an exact-scope unexpired public-push grant. The 2026-10-24 standing grant does not replace that hook, and it does not cover secret writes. A4 found no grant.
- UI defects in A6 are unfixed. The dialog claims to be modal and is not.
- Price conflicts, unpublished reel facts, and Priority Waitlist offerings from the 2026-11-08 handoff are unchanged. Do not publish a price or a draft.

### Remaining approvals

Still required, and not waived by this note: `production_publish`, `env_secret_write`, `paid_api_key`, `destructive_change`, `public_push_grant`. Do not push, do not deploy, do not set env secrets, do not turn on checkout.

## Production deploy (2026-11-19)
- Deployed to production via Vercel API (deployment dpl_HUjC2Q342ep7diPbvhwBxSEvgAgM) from commit 34a387f.
- Model backend: Vercel AI Gateway with OIDC (no stored API key); model openai/gpt-4o-mini. OPENAI_API_KEY/OPENAI_BASE_URL/OPENAI_MODEL remain optional overrides.
- Live checks: /api/chat streams answers; injection refusal verified; UI verified on production (launcher, panel, citation accordion).
- Push grants: commitbook-chatbot-20261119T023753Z, gateway-fallback, oidc-fix (all finalized).
