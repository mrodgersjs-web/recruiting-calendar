# Commit Book KPI contract
2026-11-06. Targets below are proposed operating bars, not benchmarks or observed results. Store event timestamp in UTC, report America/Denver; record environment, SKU/edition, consent version and pseudonymous order id. Never include raw payment details, athlete names, film, public profile handles or minor contact data in analytics. Exclude synthetic traffic from business metrics, retain it in QA evidence. A zero denominator is N/A, never 0% success/failure.

## Current baseline
- Production availability: 0/17 offer variants available; 0 ready playbook slugs returned by API.
- Local editorial status: 2/12 WRITTEN; 10/12 OUTLINE. Paid PDF packages found: 0/12.
- Mock handler suite: 16/16 passed. Sandbox end-to-end purchases performed by this audit: 0. Real payments: 0.
- Retention, conversion, delivery, demand and support performance: NOT MEASURED. No customer-order ledger/inbox/dashboard was read.

## Checkout KPIs
1. **Price agreement:** matching surface/SKU assertions / all required assertions. Bar 100% before any paid launch; daily and every price change. Source: versioned manifest, rendered UI, API and sandbox Stripe Price/receipt. Owner: commerce.
2. **Consent evidence coverage:** sandbox subscriptions with required exact-version consent record / completed sandbox subscriptions. Bar 100%. Separate marketing opt-in. Review every release. Owner: billing/privacy.
3. **Checkout completion:** completed legitimate sandbox sessions / eligible initiated sandbox sessions, classified success/cancel/decline/3DS. Bar 100% of deterministic success fixtures, 0 grants for negative fixtures. Production conversion gets no arbitrary target before clean cohort data exists. Owner: QA.
4. **Duplicate charge/grant:** duplicates per idempotency key. Bar 0 across replay/concurrent retry suite; alert on any observed production incident. Owner: backend.
5. **Cancellation success:** subscriptions cancelled with correct effective date and no next scheduled charge / all cancellation fixtures. Bar 100%, including mobile and re-login; proposed self-serve completion <2 minutes, no forced survey. Owner: billing.

## Fulfillment KPIs
6. **Promise completeness:** inspected promised deliverable components present and usable / total advertised components, per SKU. Bar 100% before offering it; no weighted average hiding a missing file. Source: manifest + artifact hash/render/worksheet tests. Owner: editor.
7. **Order-to-access:** eligible sandbox orders receiving usable correct entitlement / all eligible sandbox orders. Bar 100% on prelaunch suite, proposed >=99.5% in production once authorized; proposed p95 <60 sec. Measure actual first successful download separately from link issuance. Owner: backend.
8. **Unauthorized access:** negative fixtures that expose any foreign/private file or portal / all negative fixtures. Bar 0. Daily synthetic smoke plus every auth change. Owner: security QA.
9. **Reconciliation gap:** paid/trial-eligible order ids without one correct fulfillment record, plus orphan grants. Bar 0 after documented retry window (proposed 5 minutes); daily reconcile and on webhook incident. Owner: operations.
10. **Notice timeliness:** required notices provider-accepted before reviewed deadline / notices due; bar 100%. Report delivered/bounced/unknown separately, never equate accepted with read. Source: scheduler due ledger + provider receipt + approved template. Owner: lifecycle.
11. **Recurring value:** correct 30/7-day event alerts delivered / due alerts; bar 100% synthetic, proposed >=99.5% live with no stale/sport-wrong alerts. Track tracker save/reopen success 100% synthetic and rule-refresh due items reviewed on time 100%. Owner: service operations.
12. **Service SLA:** reviews/plans answered within disclosed SLA / items due; bar 100% at capacity-limited pilot. Count overdue items and queue age, not just completed outputs. Stop new service sales when capacity threshold is reached. Owner: delivery lead.

## Claims KPIs
13. **Claim traceability:** factual/commercial claims with dated source or operating proof and named reviewer / all claims, including CTA microcopy. Bar 100% for price, outcomes, rules, tax/NIL and readiness before launch. Owner: editor.
14. **Expired rule coverage:** rules beyond review deadline or lacking applicable edition / all displayed rules. Bar 0 for a paid dated calendar; quarantine rather than silently display stale critical dates. Owner: rules editor.
15. **Story/media provenance:** adult real-athlete stories with fact references and commercial-use review, and media with license/generation/visible label records / full respective inventories. Bar 100%; report sub-denominators separately. Owner: editorial/safety.
16. **Corrections:** substantiated errors open beyond published SLA; proposed critical rule/price correction containment <24h, 0 outstanding at paid release. Distinguish report volume from confirmed error rate. Owner: support/editor.

## Minor safety KPIs
17. **Data minimization coverage:** collected fields with purpose, adult consent boundary, processor and retention mapping / every collected field. Bar 100% before new intake. Owner: privacy.
18. **Family isolation:** foreign-family records/portal/files exposed in negative tests. Bar 0; sample all roles and token/invite expiry states. Owner: security QA.
19. **Direct minor outreach/publication:** unauthorized automated sends/posts/coach handoffs involving minor data. Bar 0; kill switch and incident receipt required. Draft generation is not approval. Owner: safeguarding.
20. **Deletion completeness:** verified synthetic requests removed across active stores/processors within approved retention policy / deletion requests due. Bar 100%; deadline must be explicitly adopted with counsel, not inferred from this audit. Backups follow documented expiry, not a false instantaneous-delete claim. Owner: privacy/support.
21. **Safeguarding response:** actionable safety reports triaged within adopted SLA / safety reports due. Proposed urgent triage <=24h; immediate containment for public child-data exposure; 0 unresolved critical incidents before sale. Owner: safeguarding.

## Dashboard discipline
Each metric shows numerator, denominator, environment, observation window, freshness, source availability and exclusions. Missing feed is UNKNOWN, not zero. Keep checkout conversion separate from fulfillment reliability and child safety; no aggregate score may offset a P0 failure. Weekly review names one owner/action/due date per breached bar. No live instrumentation changes are authorized by this document.
