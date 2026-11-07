# KPI: Coach Contact Kit (W10-access)
Source: `../W7-access/ACCESS.md` section 9. **No KPI has been measured. Every target below is a HYPOTHESIS to be set after 30 days of real traffic.** Integrity rule (BRIEF-V3 #3): no fake member counts or outcomes; reply counts are self-reported and are never published as results.

| # | KPI | Definition (exact) | Source of truth | Computed by | Target |
|---|---|---|---|---|---|
| K1 | Kit attach rate | kit downloads or opens / buyers of the $15 Highlight Reel & Social playbook, same 30 days | Site analytics event `kit_open` + order list | Site team (not in this lane) | Set after day 30 |
| K2 | Activation | sessions that open the send-date page for a sport and then open scripts within 7 days / sessions that opened send-date | Site analytics | Site team | Set after day 30 |
| K3 | Emails/DMs logged (14d) | rows with channel email/dm and touch_date in last 14 days | Family's own follow log | `contact_kit.kpis()` `emails_dms_in_window` | Report only |
| K4 | Replies logged | rows with reply_type in staff_generic, coach_personal, film_request, visit_invite; personal = last three | Family's own follow log | `contact_kit.kpis()` `replies_any`, `replies_personal` | Report only. **Never publish as an outcome rate** |
| K5 | Parent-copied rate | touches with parent_copied=yes / touches with a date | Follow log | `kpis()` `parent_copied_rate` | Higher is better (safety default) |
| K6 | Link checklist pass rate | aggregate pass/fail count only; **URL is never stored** | Client-side counter (host + pass/fail) | Site team | Set after day 30 |
| K7 | Support/refund signal | refund requests plus "what date" questions per 100 buyers | Support inbox | Manual | Lower is better |
| K8 | Compare-to-price funnel | visitors reaching /compare/ then /price/ | Site analytics | Site team | Watch only |
| K9 | Copy safety | count of promise-language hits across all shipped kit copy | `promise_hits()` over deliverables (test `test_no_promise_language_in_any_deliverable`) | CI / this test suite | **Must equal 0** |
| K10 | Date freshness | send-date rows older than 60 days since verified | Data file `verified_on` | `send_window()` `stale_warning` | **Must equal 0 at publish** |

## Rules
- K3 to K5 are computed only on a file the family keeps; nothing is uploaded to us by this lane.
- K9 and K10 are hard gates (pass/fail), not aspirations.
- Banned metrics: "athletes helped", "coaches reached", "offers", reply rate as a promise.
- Guardrail pair: if K4 personal replies are reported to a family, show the label `self-reported; not an outcome claim` (emitted by `kpis()`).
