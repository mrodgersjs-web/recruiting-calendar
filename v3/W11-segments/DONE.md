# W11-4 DONE: Market Segmentation & 10-Layer Diagnostic (2026-11-06)

Result: Ran 25 tests, OK (python3 v3/W11-segments/test_segments.py). Also driven in a real browser against a local server: no JS errors, no mobile overflow at 390px.

## Shipped (write scope respected)
- site/segments/index.html, segments.js, segments.css, segments.json
- v3/W11-segments/test_segments.py, build_data.py (regenerates segments.json from the W7/W6 markdown; layer text is parsed, not retyped), DONE.md

## What it does
- **A. Parent diagnostic:** 6 situations (9th/10th planner, late-start panic, burned by $1,500-$4,200 service/showcase, high-academic D3/Ivy, clock/mark sport, emerging/JUCO/NAIA). Each loads a 4-step plan linking real site pages, a matching athlete story, the problem chains behind it, and a spend note. Deep link: ?segment=burned.
- **B. Ten-layer drilldown:** all 6 chains x 10 layers = 60, stepped layer by layer, each badged [EVIDENCED \u2014 Social Fetch / Primary Rule] or [INFERRED \u2014 Working Hypothesis]. Count is exactly 42 evidenced / 18 inferred, checked against TEN-LAYERS.md and by walking all 60 in the browser. Layer 10 links to the free tools.
- **C. Spending + reallocator:** Aspen 2024 ($1,591 for $100K+ vs $604 under $50K; baseball $1,113; avg $1,016 + $475), plus a slider tool ($110 NCAA fee, single-school camps after coach contact, verified mark meets). Sizing (496,245 families, top-8 table) is labeled MODEL ASSUMPTION, NOT A CENSUS FIGURE with its assumptions listed.

## Deviations to know about
1. **The four brief routes (/access, /recruitiq, /personalize, /emerging-sports) were missing when I started and exist now** (sibling workers shipped them mid-task). Plans link them directly, with labels matched to what each page really does: /personalize is Denver-metro camps and trainers only (shown just in the 9th/10th plan, labelled Denver area); /recruitiq is a standards and fit explorer, not a service comparison, so the service-vs-DIY step still links /compare. A test requires all six brief routes (/start /access /recruitiq /personalize /emerging-sports /playbooks) to be linked from some plan and to resolve.
2. **Design system:** the live site uses /assets/tokens.css + commit.css (not site/style.css, which is the older v2 sheet). I followed the live system.
3. **W2 build_site.py strips the commit.css <link> from every index.html** (it rewrote mine). segments.css therefore @imports commit.css. Worth fixing upstream; not touched (out of scope).
4. Tool pages /tools/red-flags etc. are marked "(coming soon)" on the site; linked as-is, labeled in the step text.
5. Aspen sport-level 2024 data covers only 6 sports; track/swim budgets use the 2019 averages ($191 / $786) and say so.

## Honesty standard kept
Social Fetch counts are directional, hand-tagged, paraphrased, no usernames, no minors. No testimonials, no invented numbers, no offer or scholarship promises. Calculator is illustration only; nothing is stored or sent (test asserts no localStorage/beacon and a single fetch).
