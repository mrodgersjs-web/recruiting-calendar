# W3 Performance report (2026-11-05)
Method: Lighthouse CLI could not run (sandbox blocks headless Chrome launch: "waiting for dynamic debugging port"). Measured instead in the Aside browser (Chrome) against `python3 -m http.server 8791`, mobile viewport 412x823, PerformanceObserver for LCP/CLS, rAF sampling for frame time. Localhost, no throttling: treat LCP as a lower bound.

| Page | Weight (first load) | LCP | LCP element | CLS | Frame p50/p95 |
|-|-|-|-|-|-|
| / (home, ring) | 230 KB, 15 req | 1.63 s | div.sr__who (text panel) | 0.000 | 8.4 / 16.9 ms (~60fps) |
| /price | 146 KB | 0.10 s | H1 | 0.000 | - |
| /story/*, /playbooks | not measurable: site/story and site/playbooks are EMPTY dirs at 23:00 (W2-1 build pending) | | | | |

Budget: home 230 KB vs 1.5 MB = PASS. CLS 0.000 = PASS. LCP 1.63 s unthrottled; text LCP so mobile 2.5 s likely PASS, unverified under 4G throttle.
Already in place: ring card images use loading="lazy"; videos not loaded on home (only cut-swimmer-640.webp, 63 KB); Google Fonts use display=swap; font-display in css.

## Changes made
- vercel.json (backup vercel.json.bak): added Cache-Control for /assets/media/* (7 d + swr 30 d; not immutable since filenames are not hashed) and /assets/*.js|css|svg|png|woff2 (1 d + swr 7 d). JSON validated.

## Not done (to W2-1 / build_site.py owner, to avoid conflicts)
- Story pages: srcset 640/1080 WebP with sizes="(max-width:700px) 100vw, 50vw"; loading="lazy" + decoding="async" on off-screen plates; fetchpriority="high" + preload on the first figure; videos preload="none" with poster, src attached via IntersectionObserver (rootMargin <= 200px; wide margins load media during first paint).
- Fonts: 4 families incl. Anton + Barlow 4 weights; trim to used weights and add &text= subsetting or self-host woff2; preconnect fonts.gstatic.com.
- Rerun Lighthouse outside the sandbox: `npx lighthouse <url> [--preset=desktop]` for /, /story/<id>, /playbooks, /price.
