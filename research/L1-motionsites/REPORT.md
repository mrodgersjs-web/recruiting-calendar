# L1: motionsites.ai research for The Recruiting Calendar (2026-11-05)
Read-only visit. No sign-up, purchase or submission. Screenshots are in `shots/`. Terms text is in `terms-raw.txt`. The three prompts I captured are in `prompts-raw.json` (internal only, see licence below).

## 1. What motionsites.ai offers (as seen 2026-11-05)
- **Library filters:** Featured, Popular, Recent, All, Apps, Sections, Pricing, plus Hero, Landing Page, SaaS, 3D, Portfolio, Creative, Agency, AI, Travel, Interactive, Fintech, Ecommerce, Technology, Wellness and 3D Website.
- **Other nav items:** MCP, Backgrounds (animated video backgrounds), Academy (a course), 3D, Affiliate, Submit and Contact. There is also a "Go Unlimited" paid tier.
- **Two kinds of cards:** "Copy prompt" cards are free and "Unlock prompt" cards are paywalled. On the Sections view about half the cards were locked. Locked ones I saw include Smart Pricing, NimBus Pricing, Rocket FAQ, Halo Benefits, Editorial Collection CTA, Bento Grid Stats, Technical Specifications (tabs), Kova Testimonial, Apex Program Accordion and Solace sign-in. **I stopped at that paywall.**
- **Free section prompts seen:** Offline (footer), Animated Cards, Glow Features, Lumina (footer), Cognitra Feature, Capabilities, Koru Tech Footer, ZENTRADE FAQ, Rocket CTA, Vantix Footer, Price Calculator, Radial Diagram, NimbusOS Footer, FAQ CTA, Axion About, Halo Use Case, Pixel Grid Hover, Vize Footer, Stark Minimal Footer, Liquid Glass CTA, Elo One Results, Autonomous Ops, Atlas Lab Features, Task Engine, VeilGuard CTA, Guardnet Benefits, Kresna Footer, Rocket Pricing, Blog Showcase, NexaCore Results/Control, LaunchEx About and others.
- **Overall look:** almost everything is dark, glassy, neon, 3D or video: agency and SaaS aesthetics. **None of it is editorial or print-like.**
- **Prompt format:** long build specs (3-9K characters) with exact tokens, framer-motion or WAAPI motion, and acceptance checklists. Stacks are mixed: React+Tailwind+framer-motion, or single-file HTML/CSS/vanilla JS.

## 2. Licence and terms (READ before reuse) — from motionsites.ai/terms
- **Allowed:** "You may copy prompt text and source code into your own projects, modify them, build with them, and publish or sell the websites and apps you create with them."
- **Not allowed:** resell, redistribute or share the prompt text or source code itself; republish the library; share accounts; **"scrape, automate bulk access, or try to bypass paywalls"**.
- **What that means for this lane:**
  1. A built site is fine.
  2. Do NOT commit `prompts-raw.json` to a public repo or paste prompts into any outward doc.
  3. I captured only 3 prompts by normal clicks and then stopped, to stay clear of the bulk-access clause.
  4. This report paraphrases specs instead of reproducing prompts.
  5. Locked prompts would need a paid plan. That is a purchase, so it is Mike's decision.

## 3. Recommendation: keep the current brand
Keep cream paper, newspaper masthead, Didot dates and one red accent. No motionsites design is better for a trustworthy, parent-facing, data-first product. Their look (black backgrounds, neon glows, glass, 3D) reads as "AI agency" and would undercut the "every date cites its bylaw" positioning.

**What to take from them:** structure and motion only. That means FadeUp stagger, spotlight borders done as a hairline red rule, an accordion with grid-rows animation, an interactive calculator, and a staggered intro sequence. All of it gets re-skinned to the paper palette.

## 4. Chosen designs (7)
| # | Design | URL | Screenshot | Maps to | Prompt status |
|-|-|-|-|-|-|
| 1 | Rocket Pricing | https://motionsites.ai/?prompt=rocket-pricing | shots/rocket-pricing.png, shots/sec-rocket-pricing.png | **Pricing** | Free; captured |
| 2 | Price Calculator | https://motionsites.ai/?prompt=price-calculator | shots/price-calculator.png | **Roster math** (interactive sliders: roster spots / aid ÷ players) | Free; captured |
| 3 | ZENTRADE FAQ | https://motionsites.ai/?prompt=zentrade-faq | shots/zentrade-faq.png | **Sport picker** (4 category cards) + FAQ accordion + **hero intro motion** | Free; captured |
| 4 | Task Engine | https://motionsites.ai/?prompt=task-engine | shots/task-engine.png | **Date ledger** / tracker preview | Free; prompt not captured (stopped per terms) |
| 5 | Blog Showcase | https://motionsites.ai/?prompt=blog-showcase | shots/blog-showcase.png | **Lead magnet** (rule briefs / sample sport PDF) | Free; not captured |
| 6 | FAQ CTA | https://motionsites.ai/?prompt=faq-cta | shots/faq-cta.png | **Trial signup** CTA band | Free; not captured |
| 7 | Stark Minimal Footer | https://motionsites.ai/?prompt=stark-minimal-footer | shots/stark-minimal-footer.png | **Footer** (closest to print minimalism) | Free; not captured |

There is no good match for the **hero**. Every hero card on the site is 3D, video or glass. Keep the existing masthead hero and borrow only the ZENTRADE intro sequence.

**Captured but rejected:** Animated Cards, Atlas Lab, Capabilities (dark/neon). Their screenshots are in `shots/` for reference.

## 5. Motion specs extracted (paraphrased from captured prompts)
- **FadeUp (Rocket Pricing):**
  - Start at opacity 0, translateY 24px, and end at 1 / 0.
  - Duration 0.6s, easing cubic-bezier(0.22,1,0.36,1).
  - Triggers on in-view: once, 30% visible.
  - Section header stagger 0 / 0.1 / 0.2s; card inner stagger 0 / 0.1 / 0.2 / 0.3 / 0.4s.
- **Spotlight border (Rocket Pricing):** a 1px ring drawn with a mask-composite exclude trick. A radial-gradient spot follows the pointer through CSS vars `--spot-x` and `--spot-y`. Re-skin: spot colour `rgba(210,50,30,.35)` (red) on the `--rule` border.
- **Button text roll (Rocket Pricing):** on hover the label slides up and is replaced from below. Use about 0.25s with the same easing.
- **Accordion (ZENTRADE):**
  - One row open at a time.
  - The answer animates `grid-template-rows: 0fr → 1fr` over .32s.
  - The chevron rotates 180°.
  - Card hover tints the border with the accent colour.
- **Intro sequence (ZENTRADE):**
  - One-time Web Animations sequence, about 1.9s total.
  - Gated behind an `intro-pending` class with a 3.8s failsafe; starts on `document.fonts.ready` or after 500ms.
  - Nav settles 0-600ms, then the main control rises, then the 4 cards resolve in reading order 85ms apart.
  - Buttons lift 1px on hover.
  - `prefers-reduced-motion`: no entrance and no transitions.
- **Calculator (Price Calculator):**
  - Radio group, slider (min/max/step/default) and add-on checkboxes.
  - Live recomputed comparison cards: "typical vs. you" with a large number at text-4xl/5xl.
  - Accent colour on the active radio, checkbox and slider value.

## 6. Section-by-section build spec for Lane 8
Global setup:
- Keep `site/style.css` tokens (`--paper #f5f1e8`, `--ink #141414`, `--red #d2321e`, `--rule #d3cbb8`) and Didot / Iowan / Helvetica.
- Add one `motion.js` (vanilla, no framer):
  - an IntersectionObserver FadeUp (`[data-fade]`, `data-delay` in s, 0.6s, cubic-bezier(.22,1,.36,1), threshold .3, once);
  - a pointer-spotlight on `[data-spot]`;
  - a reduced-motion kill switch.

1. **Masthead + hero (keep the current one; add the intro only):**
   - Apply `intro-pending` on `<html>`.
   - After fonts load, run the WAAPI sequence: wordmark/nav/dateline 0-600ms, then H1 and lede, then the picker panel rises at 700ms.
   - Failsafe 3.8s.
   - No video, no 3D.
2. **Sport picker (from ZENTRADE cards):**
   - Three cards: Football, Baseball, Track/XC. Each is a cream `#fffdf7` card with a 1px ink border and a Didot sport initial in a ruled circle.
   - Cards resolve 85ms apart.
   - Hover: border turns `--red` and the card lifts 1px.
   - Selecting a card sets the class-year select and scrolls to the ledger.
3. **Date ledger (Task Engine structure + the existing `.ledger`):**
   - Keep the existing grid (big Didot day | what changes | what it costs you + bylaw source).
   - Rows FadeUp with stagger 0.06s, capped at 6.
   - The red dot pulses once (scale 1→1.4→1, 0.6s) on the row nearest today.
   - Locked rows stay blurred behind the paywall.
4. **Roster math (re-skinned Price Calculator):**
   - Inputs: sport radio, roster size slider, scholarship-equivalent input, plus an "include walk-on / NIL-era roster cap" checkbox.
   - Output: three cards, "Roster spots", "Avg aid per rostered player", "Players per full scholarship". Each shows a Didot number at 48-56px, and each must cite its source per the BRIEF no-invented-numbers rule. Defaults must come from Lane data with a URL and date, or be labeled estimate.
   - The number counts up over 0.4s when an input changes.
   - Never present the result as a scholarship promise.
5. **Pricing (re-skinned Rocket Pricing):**
   - Header kicker "Published price", H2 "One price. No sales call.", right-aligned 30-day refund line. Stagger 0 / .1 / .2.
   - Cards on `#fffdf7` with hairline borders. The featured card (Sideline) gets a 3px red top rule plus a "Founding 100" tag instead of a white pill.
   - Spotlight border in red.
   - Inner stagger 0-.4s.
   - **Tier prices are NOT approved to publish (BRIEF).** Use placeholders, or render behind a `data-draft` flag until Mike approves the exact text.
6. **Lead magnet (Blog Showcase layout):**
   - A 3-column "clippings" grid of free one-page rule briefs per sport, each with a dateline and bylaw cite.
   - Hover: an image-less card rises 2px and a red underline draws left to right over 0.3s.
   - The email capture is a draft form with no live submit.
7. **Trial signup (FAQ CTA):**
   - The ZENTRADE-style accordion (one open at a time, 0fr→1fr .32s, chevron rotate) holds about 5 parent objections: refund, no promise, sources, minors' data, cancel.
   - Followed by a single ink band CTA "Start free" with a ghost secondary button.
   - Every form is a preview only; nothing submits.
8. **Footer (Stark Minimal Footer):**
   - Big Didot wordmark across the width, a 3px double rule above.
   - Sans uppercase 11px link columns (Sources, Refund policy, Privacy, Contact).
   - Fine print: "No scholarship promise. Every date cites its bylaw."
   - No animation apart from a link-hover colour change to red over .15s.

## 7. Flags
- Licence forbids sharing prompt text: keep `prompts-raw.json` out of any public repo or deploy.
- Licence forbids scraping or bulk access: I captured only 3 prompts, by hand.
- The paywall blocks Smart/NimBus Pricing, Rocket FAQ, Editorial Collection CTA, Bento Grid Stats and others. Unlocking them is a purchase and needs Mike's OK.
- Paywalled prompts are not needed: the free prompts cover every section except the hero.
