# The Commit Book family solutions: six-tool implementation plan

Date: 2026-11-18
Owner: Aside family-solutions lane
Integration owner: Aside task jxfSAKC9J5Bt6HcG

## Outcome

Build six usable, local-first React tools behind `/solutions` and `/solutions/[slug]`:

1. `next-30-days`: choose sport, class year, target level, and current need; produce three athlete-owned actions, one parent support action, and exact site links.
2. `camp-decision-receipt`: enter camp and travel costs, coach attendance, target-coach attendance, format, refund terms, and film terms; show total cost, unknowns, and a transparent `CONSIDER` / `SKIP` / `NEED MORE INFO` heuristic; save a receipt.
3. `film-outreach-brief`: enter sport, class year, position, optional measurable, highlight link, and full-game link; produce a concise coach email and a film/link checklist. Never imply coach interest.
4. `family-recruiting-receipt`: persist sport, class year, target level, completed actions, next date, and sources; export JSON and print a portable receipt.
5. `offer-aid-comparison`: compare up to four programs; keep verbal vs written and published vs projected distinct; calculate annual net cost only from user-entered values.
6. `program-fit-check`: record roster, coaching, academic-support, development, retention, and evidence inputs; show red flags and unknowns without recommending a school.

Scout cited answer cards and the Source-First Trust Center are owned by the integration lane and are outside this write scope.

## Done test

From the repository root:

```bash
npm run typecheck
npx playwright test --config=solutions-e2e.config.ts
```

The browser suite must prove all six routes render, all primary inputs/actions work, refresh persistence works for the family receipt, calculations remain transparent, no raw personal data leaves the browser, mobile widths do not overflow, and unknown/verbal/projected states remain explicit.

## Current constraints

- Next.js App Router, TypeScript, React, Tailwind, existing SiteHeader/SiteFooter and Commit Book tokens.
- No new dependency and no `package.json` change.
- No API route, Scout, KB, Trust Center, site-chrome, or golden-set edits in this lane.
- No deploy, push, checkout, email, or outward publish.
- User-entered athlete information stays in local component state or localStorage. Export happens only through a user click.
- No invented NCAA dates, prices, roster limits, coach-interest claims, school recommendations, or outcome promises.

## File ownership

- `components/solutions/types.ts`: shared types, solution slug and category definitions.
- `components/solutions/catalog.ts`: six catalog entries and static action/source definitions.
- `components/solutions/shared.tsx`: small presentational and persistence helpers used only by these six tools.
- `components/solutions/<tool>.tsx`: one isolated client component per tool.
- `app/solutions/page.tsx`: catalog landing page.
- `app/solutions/[slug]/page.tsx`: static params and component dispatch.
- `tests/solutions.spec.ts`: route and behavior coverage.
- `solutions-e2e.config.ts`: isolated Playwright web server on port 32122, `testMatch: "solutions.spec.ts"`, `reuseExistingServer: false`, and no model key.

The integration lane may read `types.ts` and `catalog.ts` after the contracts are reported. It must not edit these files without coordination. The integration lane also owns adding the single `/solutions` navigation link; this lane does not edit site chrome.

## Shared contracts

```ts
type SolutionSlug =
  | "next-30-days"
  | "camp-decision-receipt"
  | "film-outreach-brief"
  | "family-recruiting-receipt"
  | "offer-aid-comparison"
  | "program-fit-check";

type SolutionDefinition = {
  slug: SolutionSlug;
  title: string;
  eyebrow: string;
  summary: string;
  outcome: string;
  mechanism: string;
  primaryAction: string;
  sourceLinks: { label: string; href: string }[];
};
```

Only the six slugs above are valid. `generateStaticParams` and `notFound()` define the route boundary. Each catalog card must link to the matching route and name the user outcome, not a backend mechanism.

## UI architecture

- Server-rendered catalog and route shells; client components contain only the interactive tool.
- Existing paper `#f7f5f0`, card white, ink `#141413`, muted `#57534e`, hairline `#e5e0d6`, action blue `#1d4ed8`.
- Use native controls, visible labels, fieldsets where grouped, focus-visible outlines, and at least 44px primary touch targets.
- Desktop forms may use two columns; mobile is one column with no horizontal page overflow. Comparison tables scroll inside a labelled region, not the page.
- Every tool shows its assumptions and source links next to the result. No result is hidden behind a signup.
- Print styles remove site chrome, including `[data-testid="commitbook-chat-launcher"]` and `#commitbook-chat-dialog`, and preserve the result. `window.print()` is the only PDF path; JSON export uses a Blob created after a click.
- Local persistence is limited to the Family Recruiting Receipt under a versioned key. Other tools do not persist sensitive form values after refresh.

## Tool logic and falsifiers

### Next 30 Days

Static action templates are selected by explicit user inputs. Sport changes film/outreach wording; need changes the primary action. The tool links to `/window`, `/sops`, `/auditor`, or `/start` for dated rules rather than duplicating a date. Falsifier: any generated action displays an uncited date or changes to an irrelevant sport template.

### Camp Decision Receipt

`total = campFee + travelCost`. The tool never computes value from price alone. Blank or non-numeric fees produce `NEED MORE INFO` and no total. Missing target-coach attendance, format, refund, or film terms also produce `NEED MORE INFO`. Once all fields are known, `CONSIDER` requires verified relevant-coach attendance; no or unverified relevant-coach attendance produces `SKIP`. Show every entered factor. Use no dollar threshold and labels only `CONSIDER`, `SKIP`, and `NEED MORE INFO`. Falsifier: a camp with no verified relevant coach attendance can produce `CONSIDER`.

### Film + Outreach Brief

Email fields are user-entered and optional except sport/class/position and highlight link. Full-game fallback and logged-out link tests stay visible. Copy requires a button click. Falsifier: output contains invented metrics, implies an offer, or omits the full-game/link checks.

### Family Recruiting Receipt

The receipt loads only after mount from `commitbook.family-recruiting-receipt.v1`, validates parsed localStorage shape, and has a clear action. Export contains `{ schemaVersion: 1, ...values }` and is created only on click. Falsifier: malformed stored JSON crashes the page or a refresh loses valid saved values.

### Offer + Aid Comparison

Annual net cost is `totalCost - athleticAid - academicAid - needBasedAid`. Blank aid is labelled `left blank, counted as $0`; it is never described as existing aid. If aid exceeds cost, show both the raw negative and the floored $0 with an explicit note. Verbal offers never display as written or binding. Signing dates carry `published`, `projected`, or `unknown`. Required test fixtures: cost 50000, athletic 20000, academic 5000, need blank gives net 25000 with the blank-as-$0 label; a second row retains verbal and projected labels. Falsifier: blank values are treated as existing aid or a verbal offer is labelled binding.

### Program Fit Check

Every red flag includes its input and every unanswered item appears under unknowns. The result is a question list, never a school score or recommendation. Falsifier: an unanswered evidence field silently counts as a pass.

## Accessibility, privacy, and safety review

- No athlete name, email, phone, street address, birthday, or private-school record is required.
- No network request is part of any tool action. Links navigate only when the user chooses them.
- Clipboard and export failures show visible status text.
- Buttons have explicit type; live result regions use polite announcements without stealing focus.
- Destructive clear/reset is local and reversible by re-entry; no account data is touched.
- External rule claims remain on the existing sourced pages, not copied into these tools.

## Test matrix

For each route: title, primary form, result, source link, and 390px mobile overflow check.

Specific tests:

- Next30Days changes actions when need changes and links to exact site tools; result text contains no month-day or NCAA date.
- Camp Receipt blocks a positive decision when relevant coach attendance is missing; computes total cost only for complete numeric costs; shows entered assumptions.
- Film Brief generates email text with entered values and no invented metric; includes full-game and logged-out-link checks; copy failure has visible status.
- Family Receipt survives refresh, exports `{schemaVersion: 1, ...values}`, and recovers from malformed localStorage. The other five tools do not create the receipt key or grow localStorage after their actions.
- Offer Comparison calculates the two required fixtures and preserves verbal/projected labels.
- Program Fit displays unanswered items as unknown and evidence-based red flags; no score or school recommendation.
- Unknown slugs render the not-found page.
- At 390px, `document.documentElement.scrollWidth <= clientWidth`; the comparison table is inside a labelled `role="region"` with `overflow-x-auto`.
- Controls have visible labels, primary buttons are at least 44px, result regions use polite live announcements, and no name/email/tel/birthday/address inputs exist.
- Tool actions cause no non-document network request.

## Review record

- Grok 4.7 independent review: NOT READY on the first draft; slug, camp rule, aid math, persistence, safety-test, print/chrome, navigation, and E2E-server findings were resolved above.
- MiMo v2.6 Pro reviewer: provider error before review; no findings accepted.
- Claude Opus 5.5 reviewer: provider rate limit before review; no findings accepted.

## Review request

Review this plan for implementation readiness, contract drift, privacy leakage, incorrect recruiting claims, inaccessible interaction, and avoidable complexity. Return concrete blockers and the smallest safe changes. Do not edit files.
