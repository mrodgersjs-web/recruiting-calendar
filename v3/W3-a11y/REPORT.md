# W3 Accessibility audit (WCAG 2.2 AA) - 2026-11-05
Served site/ on 127.0.0.1:64831; axe-core 4.10.2 (wcag2a/aa, 21aa, 22aa) on 13 pages (home, calendar, free, coaches, about, welcome, math, camps, price, compare, rules, rules/football/2028, legal/privacy).

## Key finding: the V3 experience is not in site/ yet
No 3D ring/carousel, no story pages (site/story/ has no index.html), 0 <video>, 0 aria-live regions on home. Ring keyboard path, look-change announcements, video captions/pause could NOT be audited. Re-run when W2-site lands.

## Fixed directly (CSS tokens, style.css line 1; backup /tmp/style.css.bak-a11y)
- --ink3 #7a7468 -> #665f54 (4.12:1 -> 5.59:1 on cream)
- --red  #d2321e -> #b5281a (4.42 -> 5.67 on cream, 5.09 on paper2, cream-on-red 5.67)

## Open for W2-1
1. --ink3 on black (#141414): was 3.97, now 2.92. Fail either way; dark sections need their own muted token (e.g. #a39d92, ~7:1).
2. assets/tokens.css --c-signal #d2321e on cream fails 4.42 (only OK as large text / on dark).
3. Remaining contrast hits are scroll-reveal elements captured mid-fade (opacity); confirm reveals finish (and are instant under reduced motion) so text is never left faded.
4. /math/ span chips fail contrast (8 nodes).
5. Ring (when built): roving tabindex, ArrowLeft/Right, aria-roledescription="carousel", slides role=group "N of M", polite live region announcing look change, autoplay pause button (WCAG 2.2.2) + stop on focus/hover, disable autoplay + 3D under prefers-reduced-motion, 24x24 min targets for 01-0N ticks, Drag/View cursor must not be the only affordance.
6. Video: captions track, visible pause, no autoplay with sound, reduced-motion poster fallback.
7. Generated images: alt text + visible "Illustration" label.

## Passed
Images all have alt; focus visible (outline auto) on first tab stop; prefers-reduced-motion rules exist in style.css and motion.js; no target-size violations; no form-label violations.

Screenshots: home-focus.png, home-reduced-motion.png
