# L2 Capability Map: studio -> Recruiting Calendar (2026-11-05)

Source: private studio repo (athlete-specific, not named here) + fca-crm. Buckets: PRODUCTIZE / INTERNAL / KEEP_PRIVATE. Effort S/M/L. Tiers are the proposed (unapproved) tiers in BRIEF.md.

| Capability | Source path | Bucket | Parent-facing feature | Tier | Effort |
|---|---|---|---|---|---|
| Coach follow/engagement signal tracking on X | `automation/daily/census.py, coach_reporting.py, tracker/kpi.jsonl` | PRODUCTIZE | Coach-follow signal tracker | Pathway | M |
| Resolve coach names to X handles/staff pages | `automation/daily/coach_identity_resolver.py, automation/recruiting/program_handle_resolver.py` | INTERNAL | (powers coach directory + follow tracker) | - | M |
| D1 coach census scrape + classify (role, activity, follow mix) | `research/coach-x-osint-2026-10-23/scrape_coaches.py, analyze.py, jev_classify.py; research/coach-census/` | INTERNAL | (powers coach-activity benchmarks) | - | L |
| Aggregate coach X behavior by role (posting rate, RT share, recruit share of follows) | `research/coach-x-osint-2026-10-23/analysis/summary.json (aggregate fields only)` | PRODUCTIZE | Which coaches actually use X (role benchmarks) | Sideline | S |
| Coach + recruiter directory (fca-crm: 6,213 coach_directory rows, 797 rec_directory rows) | `~/Developer/fca-crm/data/fca_crm.sqlite` | PRODUCTIZE | Program & coach contact directory | Pathway | M |
| National program list + peers | `coaches/programs-national.csv` | INTERNAL | (seeds directory/target lists) | - | S |
| Program targeting / fit list | `strategy/08-coach-recruiting-funnel.md` | PRODUCTIZE | Target school list builder | Pathway | M |
| Coach outreach log schema + jsonl tracker | `tracker/COACH-OUTREACH-SCHEMA.md` | PRODUCTIZE | Hosted recruiting tracker (contacts, replies, next step) | Sideline | M |
| Recruiting KPI tree + scorecard | `automation/recruiting/kpi_scorecard.py, strategy/04-kpi-tree.md, tracker/kpi-targets.json` | PRODUCTIZE | Recruiting progress scorecard | Pathway | S |
| Recruiting X account audit (bio, pinned, cadence) | `research/04-baseline-audit.md, 05-live-account-audit.md, automation/cdp/x_account.py` | PRODUCTIZE | Recruiting X profile audit | Recruiting Audit | S |
| Score a recruiting profile (Hudl/X) against D1 coach review rubric | `automation/film/d1_profile_jev.py, d1_review.py, d1_coach_100.py` | PRODUCTIZE | Coach-eye profile review | Recruiting Audit | M |
| Highlight reel planning, cut gates, clip selection checklists | `automation/film/CUT-GATES.md, HARNESSES.md, film.pre-landing-*/HIGHLIGHT-PLAN.md` | PRODUCTIZE | Film reel brief + cut checklist | Pathway | S |
| Automated clip assembly pipeline | `automation/film/assemble.py, flows/` | INTERNAL | (optional future: reel assembler) | - | L |
| How coaches screen film (research) | `research/2026-10-01-film-coach-screening.md` | PRODUCTIZE | Film guide: what coaches watch first | Free | S |
| NCAA contact/NIL rules research + correction | `research/01-compliance-nil-rules.md, 01a-coach-contact-CORRECTION-2026-09-18.md` | PRODUCTIZE | Sourced contact-period rules (by bylaw) | Free | S |
| NIL deal/inbound/prospect CLIs + readiness | `automation/cli/nil_*.py, strategy/09-10, cron/06-weekly-nil-readiness.md` | PRODUCTIZE | NIL readiness checklist (state rules) | Pathway | M |
| X growth research + case studies, post playbook | `research/02-x-growth-and-case-studies.md, FIVE-STAR-X-PLAYBOOK-20261023.md, strategy/07,17` | PRODUCTIZE | Recruiting X playbook for parents | Sideline | S |
| Daily signal->draft->gate cron, editorial calendar, posting times | `automation/cron/01-05, automation/daily/drafts.py, posting-times.json, content/` | PRODUCTIZE | Weekly recruiting content calendar (drafts only) | Pathway | M |
| Guardian Gate-D: nothing posts without parent approval | `GATES.md, strategy/03-risk-autonomy-gates.md` | PRODUCTIZE | Parent-approval gate (no auto-posting) | Sideline | S |
| Camp/visit signal analysis (coach RT content classes incl. camp/visit) | `analysis retweet_content aggregates; strategy/08` | PRODUCTIZE | Camp ROI checker | Sideline | M |
| Stats/scores pulls (MaxPreps) | `automation/cdp/maxpreps.py` | INTERNAL | (stats import for tracker) | - | M |
| Eden draft/schedule bridge | `automation/eden/` | INTERNAL | (drafts export; never auto-post) | - | S |
| Agent roster: film scout, hudl scout, reply scout, QC verifier | `automation/agents/` | INTERNAL | (ops agents) | - | - |
| Next.js KPI dashboard | `dashboard/` | INTERNAL | (pattern for member dashboard) | - | M |
| Master harness, proof obligations, fixer, durable worker | `00-master-harness.md, architecture/, automation/fixer, automation/durable` | INTERNAL | (ops governance) | - | - |
| Identity brains, film folders, follower lists, coach follower crossmatch, guardian inputs, clips, Hudl inventory, campaigns, goals | `brains/, film/, research/coach-x-osint-2026-10-23/analysis/*follower*, tracker/*hudl*, tracker/wn-*, tracker/guardian-inputs.json, campaigns/, goals/, content/, follow-queue/` | KEEP_PRIVATE | - | - | - |
| 3 other athlete-specific repos (private repos, athlete-specific) | `github mrodgersjs-web/*` | KEEP_PRIVATE | - | - | - |

## Safe aggregate findings (coach X census, 2026-10-24, 610 D1 accounts)
- Program accounts: 98% active in last 30 days; position coaches 50-83%.
- Position coaches mostly retweet (RT share 0.78-0.97); recruits are 21-38% of their recent follows.
- Implication for parents: coaches read and amplify on X but rarely originate; a clean profile matters more than volume. Label as estimate until re-run.

## Not checked
- `gh` CLI absent on this host; repo list taken from GitHub API + stored credential listing. 3 other athlete-specific private repos left unopened (KEEP_PRIVATE).
