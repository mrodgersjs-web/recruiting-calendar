# V3 Design System — The Recruiting Calendar (W1-design, 2026-11-05)
Sources: read-only 1440x900 captures of nike.com (home, Jordan, men's shoes grid, a PDP), adidas, Under Armour, On, lululemon, New Balance (`screenshots/`, `<site>-hero.png` / `-scroll.png`, `nike-pdp.png`); runway spec §4-9 (attachment); `research/L1-motionsites/REPORT.md`. Computed styles measured live, values below.

## 0. Trademark guardrails (binding)
- No swoosh, stripe-trio, chevron, "jumpman"-like silhouette or tick-shaped mark. Our logo is a wordmark + calendar-grid glyph (W2 logo lane owns it).
- No imperative motivational tagline in the "Just Do It" / "Impossible is Nothing" mould. Headlines state facts ("Signed. NAIA. Year 2 of JUCO.").
- No Nike/adidas fonts (Futura ND, Helvetica Now, AdihausDIN, Neue Plak, On Diatype). Only OFL Google Fonts below.
- No athlete likeness generated for real people (BRIEF rule 2): real = type/motif cards; composite = labelled "Illustration".

## 1. What the category does (measured)
| Site | Display | Body | Button | Notes |
|-|-|-|-|-|
| Nike | Futura ND 76px/0.9 uppercase, condensed heavy | Helvetica Now 16/28, #111 | pill r30, 18x24 pad, 60px PDP, #111/#fff | 3-up editorial tiles 12px gap, 48px gutter |
| Jordan | N.Haas 24 bold, black bg | 16/28 white on #000 | same pill | inverted dark mode |
| adidas | AdihausDIN 32 / adidasFG 24 bold uppercase ls 2.5px | 16/22 | square r0 | hard edges, black/white |
| Under Armour | Neue Plak 24 700 | 14/20 #1d1d1d | r0 #1d1d1d, 12px 700 | dense grid |
| On | 50px 700 ls -1% | 16 | circular r50% icon buttons, uppercase 14 ls .84px | airy white |
| lululemon | Saans 72/1.1 ls -4% | 16 | pill r1000 #f4f3f2 | soft neutral |
| New Balance | Proxima 24 500 | 14/20 300 | 1px 6px text buttons | utilitarian |
Patterns we adopt: full-bleed photo hero with bottom-left heavy condensed uppercase headline + one-line sub + white pill CTA; strict black/white UI chrome; image does the colour; product grid with zero radius cards, 12px gaps, title/sub/price stacked under the image; sticky 60px header with centred category nav.

## 2. Type
- **Display:** Anton (uppercase, hero & story chapter titles only). Fallback Barlow Condensed 800.
- **Condensed:** Barlow Condensed 600/700 for H1-H3, tick labels, stat numerals, level tags.
- **Text:** Inter Tight 400/500/600 for body and UI.
- **Mono:** JetBrains Mono 500 for bylaw citations and dates (keeps the "every rule cites its bylaw" signal).
Scale (`tokens.css`): hero clamp(56-128)/0.88 · d1 clamp(40-76)/0.9 · d2 clamp(32-48) · h1 32 · h2 24 · h3 20 · body-l 18 · body 16/1.65 · small 14 · label 12 uppercase .14em · micro 10. Mobile h1 24.
Rules: display always uppercase, tight leading, max 3 lines; never set body in condensed.

## 3. Colour
Ink #111 / paper #fff / snow #f5f5f5 / stone #e5e5e5 / line #cacacb / muted #707072. One signal: RIG red #d2321e (carried over from v2 brand) — live tick, "In this story" Get button on dark, bylaw rule hairline. Dark story chapters invert (ink bg, paper text, Jordan pattern). Level tags D1/D2/D3/NAIA/JUCO are neutral greys + two earth tones so no division looks "better". "Illustration"/"Composite" tags on #fff3b0.

## 4. Spacing & grid
4px base: 4/8/12/16/24/32/48/64/96/144. 12-col grid, gutter clamp(24-48px), gap 12px (8 mobile), max 1920. Product (playbook) grid: 3-up desktop, 2-up tablet, 1.2-up swipe mobile. Section rhythm 96px desktop / 64 mobile.

## 5. Components
- **Header:** 60px, white, wordmark left, centred nav (Stories · Calendar · Playbooks · Rules), search pill + bag right; 14px/500 nav, 10px pad.
- **Buttons:** pill r30, h48 (h60 on PDP/"Get playbook"); primary ink, inverse white-on-photo, outline, signal. Text-roll hover (motionsites Rocket Pricing, .25s ease-fade). Focus 2px #1151ff.
- **Cards:** r0, 4:5 image on #f5f5f5, then 12px label (sport · state), 16/500 title, 16 muted sub, price. Hover: image scale 1.04 over 1.4s ease-out (spec §5.5).
- **Playbook PDP:** 2-col (thumb rail + 4:5 gallery | 456px info col), price, option chips r4 1px line, h60 primary CTA, accordion (motionsites ZENTRADE grid-rows 0fr→1fr .32s).
- **Story chapters:** full-bleed sticky media + scroll-pinned text; chapter numerals in Barlow 700 "01/06".
- **Bylaw chip:** mono 12px, 1px signal-red left rule, links to source.

## 6. Home: 3D athlete ring (port of spec §4-9, re-skinned)
- Grid `1fr 380px`; left stage white, panel border-left 1px line. Title "Pick a path." (Anton 46/24). Panel head **"In this story"** + "N playbooks"; rows 92px thumb / text / 44px **Add/Get** button (+ → check → spinner states).
- Ring math unchanged: 12 bodies (n stories padded), R .62W, P 1.65W, horizon .36H, front scale 1.08, blur 1.8px/slot to 6.5 max, opacity clamp((cosφ+.55)/.3), spring K95 C19.49, entrance -1.15 steps. Phone ≤749 classic walk line.
- Hero hand-off at rest, light sweep 1.5s soft-light, ticks 01-0N (44→190px active, 2px bar, autoplay fill 5s), Drag/View cursor, prev/next 44px icon rings.
- Figures: real athletes = typographic poster cards (name, school, level, sport glyph) at 9:16; composites = labelled illustrations, transparent cut-out with contact shadow.

## 7. Motion
Easings: out (.16,1,.3,1) default · silk (.65,0,.35,1) sweeps · spring (.34,1.56,.64,1) pins/chips · sheet (.32,.72,0,1) mobile sheets · fade (.22,1,.36,1) FadeUp. Durations: 150 micro / 250 fast / 400 base / 600 FadeUp / 900 morph / 1400 reveal / 1500 sweep / autoplay 5s. FadeUp: 24px→0, stagger 100ms, once at 30% in view. Intro: title letter-spacing .03→-.02em over 1.8s. Reduced motion zeroes all.

## 8. Image treatment
Full-bleed 16:9 hero (mobile 4:5), bottom scrim 45%→55% black for legible white type; editorial 3-up tiles. Colour graded natural, no neon/glass (motionsites aesthetic rejected per L1). Composite illustrations: consistent matte editorial style, single-subject, plain studio ground, visible "Illustration" tag top-left. Real athletes: licensed press only, else typographic.

## 9. motionsites picks mapped
Rocket Pricing → playbook pricing (FadeUp + spotlight hairline red); Price Calculator → roster/aid math; ZENTRADE → sport picker + FAQ + intro sequence; Task Engine → date ledger; Blog Showcase → story index; FAQ CTA → end-of-story CTA band; Stark Minimal Footer → footer. Structure only; prompts stay internal (licence).
