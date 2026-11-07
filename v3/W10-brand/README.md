# Commit Book: visual asset kit

An original, geometric open-book mark crossed by a rising commitment route. The wordmark is drawn from simple custom block geometry, not a font file. This is a proposed brand direction, not legal or trademark clearance. No team, school, league, or third-party marks are included. Original SVG geometry authored for this kit; no external imagery or fonts are embedded. Similarity and trademark searches are still needed before commercial rollout.

## Assets
- `assets/lockup-ink.svg`: default horizontal lockup, transparent, use on light backgrounds.
- `assets/lockup-white.svg`: reverse lockup, transparent, use on dark backgrounds.
- `assets/mark-ink.svg`, `assets/mark-white.svg`: standalone marks.
- `assets/wordmark-ink.svg`, `assets/wordmark-white.svg`: standalone wordmarks.
- `assets/icon-square.svg`: dark square app / favicon source, scalable. Rasterize at target dimensions when required.
- `assets/social-card.svg`: 1200 × 630 brand card. Its tagline uses system Arial; replace or outline it if font-independent rendering is required. No claims, team imagery, or real people.
- `preview.html`: local visual overview. `build.cjs` regenerates SVGs, `tests/test.cjs` checks the kit.

## Color and placement
Ink `#101820`, white `#FFFFFF`, signal lime `#B7E63E` (background/accent only, not the logo). Ink/white contrast is approximately 17.89:1; ink/lime approximately 12.27:1. Do not place the logo directly over busy imagery. Keep a clear margin at least one-quarter of the mark width on all sides; do not stretch, rotate, add effects, change its components, or pair it with unlicensed team marks. Recommended minimum display widths: 160 CSS px for lockup, 24 px for mark. At favicon sizes check legibility visually; use a larger mark rather than forcing fine detail.

## Integration contract
Copy assets into the consuming application's static asset directory in a separate, reviewed change. This kit makes no site edits. Preserve SVG viewBox and aspect ratio; set CSS width with height auto. Use ink on light and white on dark solid backgrounds. Asset paths here are relative to this folder and must be remapped by the integrator. Example:

```html
<a href="/" aria-label="Commit Book home">
  <img src="/assets/lockup-ink.svg" alt="" width="385" height="64">
</a>
```

The link supplies the accessible name; its image is decorative. For a standalone logo, use `<img src="/assets/lockup-ink.svg" alt="Commit Book">`. Avoid duplicate adjacent spoken text. Social card alt text: `Commit Book logo on a dark background with a lime stripe.` Test light and dark contexts, responsive widths, keyboard focus of linked logos, and actual color contrast after integration. No claim of WCAG conformance for the consuming site is made by this kit.

## Verify
Run `node tests/test.cjs`. Open `preview.html` in a browser to inspect desktop, narrow, reverse, and small-mark presentations. Automated tests check SVG parsing where available, asset boundaries, viewBox, accessible titles, contrast, and expected build output; visual review and trademark review remain separate.
