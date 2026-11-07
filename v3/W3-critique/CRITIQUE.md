# W3 Cold Design Critique — The Recruiting Calendar v3 (2026-11-05 ~23:05 MT)
Critic: cold, zero build context. Inputs: BRIEF-V3.md, W1-design/DESIGN-SYSTEM.md, ds-critique laws (design-studio-os CRITIQUE mode).
Served `site/` on localhost:8791 (python http.server). Captures: `shots/` (26 pages x 1440/390 + home scroll 33/66/100%).

**Verdict: REVISE (blocking).** The served site is still the v2 editorial build (serif "The Recruiting *Calendar*" masthead, cream paper, newspaper rules). `index.html` loads none of `assets/ring.js|ring.css|stories.js|tokens.css`; `/story/` and `/playbooks/` are empty directories (directory listing). Ring at rest / mid-spin and story scroll depths **could not be captured: they do not exist on any served page.**

## Jev image (hosted typesafe, yes|no; raw JSON in shots/jev.jsonl). P(yes):
| image | premium wow | Nike polish | typography | imagery | ring/motion | purchase intent |
|-|-|-|-|-|-|-|
| blank PNG (control) | 0.00 | 0.00 | 0.04 | 0.00 | 0.01 | 0.00 |
| home 1440 | 0.06 | 0.15 | 0.20 | 0.00 | 0.00 | 0.55 |
| home 390 | 0.14 | 0.20 | 0.15 | 0.00 | 0.00 | 0.76 |
| price 1440 | 0.10 | 0.06 | 0.08 | 0.00 | 0.00 | 0.14 |
| nike.com hero (ref) | 0.96 | 0.79 | 0.88 | 0.75 | 0.03 | 0.03 |
Control is clean (all ~0), Nike ref scores high on brand axes, so the judge discriminates. Our pages sit near the blank control on every brand axis. Purchase intent on home is the only marginal signal (copy-driven); price page fails it (0.14). Required pass bar 0.9: nothing passes.

## Ranked findings
| # | finding | law cited | sev | exact fix |
|-|-|-|-|-|
| 1 | v3 home not wired: ring assets exist but index.html is v2; no ring, no ticks, no Drag/View cursor, no "In this story" panel | 71 (commit hero to concept or it reads unfinished), 5 (no imagery/motion) | P0 | Replace site/index.html with the v3 ring shell: `<link assets/tokens.css, ring.css>` + `<script assets/stories.js, ring.js>`; header per DS §5; delete v2 masthead |
| 2 | /story/ and /playbooks/ empty -> directory listing; every story must end in a purchase (brief) | 24 (buy control loudest), 64 | P0 | Generate story/<slug>/index.html per stories.js entry and playbooks/<slug>/index.html PDP with h60 ink pill "Get playbook"; add 404 fallback |
| 3 | Zero imagery on every page (Jev imagery 0.00 everywhere) though 13 real-* posters/mp4 and hero-loop exist | 40, 91, 65 | P0 | Full-bleed hero-loop-720p.mp4 (poster hero-loop-poster.jpg) behind home; ring cards use real-*-poster.jpg (type/motif only, no likeness) |
| 4 | Type is a didone serif + italic red; DS mandates Anton/Barlow Condensed/Inter Tight | 26, 27 (face matches sector), 25 | P0 | Load Google Fonts Anton, Barlow Condensed 600/700, Inter Tight 400-600, JetBrains Mono; set h1 Anton uppercase clamp(56px,8vw,128px)/0.88 bottom-left |
| 5 | Palette cream #f3efe6 + red, not ink/paper black-white | 8, 3 | P1 | Body bg #fff, text #111; red #d2321e only on live tick and Get button |
| 6 | Header: serif wordmark + 6 uppercase links + VOL.1/date newspaper strip; mobile header eats ~40% of first screen with a boxed MENU button | 45, 39, 90, 84 | P1 | 60px header: new wordmark+grid glyph left (assets/logo/lockup-horizontal-dark.svg), centred Stories·Calendar·Playbooks·Rules, bag right; delete VOL/date strip; 56px mobile header with icon menu |
| 7 | Primary CTA "SHOW MY DATES" is a grey square (#6f6f6a) — reads disabled | 24, 23, 6 | P1 | Ink #111 pill r30 h48 white text; inverse white pill on photo |
| 8 | Double-rule / boxed form / hairline dividers everywhere (newspaper chrome) | 14, 34, 76 (double rule reads old-fashioned) | P1 | Remove borders; separate sections with 96px rhythm and snow #f5f5f5 bands; cards r0 no border |
| 9 | Home hero is text-only; long 4-line paragraph sub | 30, 89, 84 | P1 | Hero = one fact headline ("Signed. NAIA. Year 2 of JUCO." style) + one-line sub + pill; move explanatory para below fold |
| 10 | Price page (purchase intent 0.14): no product grid, no image per plan | 24, 64, 48 | P1 | Rebuild as DS playbook grid: 3-up 4:5 image cards, label/title/price stacked, 12px gaps, each with Get pill |
| 11 | Mobile: home 15,455px tall, calendar rows dense small grey | 37, 21, 67 | P2 | Collapse date rows to accordions; muted text #707072 min 14px |
| 12 | `assets/media/cut-swimmer-1080.webp` is 0 bytes (broken asset) | 4 (cut pass) | P2 | Re-export or remove from srcset |
| 13 | /calendar/ serves the same document as home (identical height) | 39 | P2 | Give /calendar its own page or redirect to /#dates |
| 14 | Red eyebrow + red italic wordmark + red rules: accent overused | 6, 13 | P2 | One red use per screen |

## Nike side-by-side (W1-design/screenshots/nike-hero.png vs shots/home-1440.png)
Nike: full-bleed photo, condensed heavy uppercase bottom-left, white pill, black/white chrome. Ours: no photo, serif headline top-left, grey square button, cream newspaper chrome. Gap is structural (the v3 build is not deployed into index), not a polish gap.
