# v3 build order (repo root, run in sequence)

1. `python3 v3/W2-site/data_build.py`
2. `python3 v3/W2-site/build_site.py`
3. `python3 v3/W2-seo/build.py` then `cp v3/W2-seo/site/sitemap.xml site/sitemap.xml`
4. `python3 v3/W12-library/build_library.py` (the /library catalog)
5. `bash v3/W11-sync-to-site.sh`
6. `python3 v3/W9-experiences/build_pages.py` (21 athlete pages + notify tool pages)
7. `bash v3/W12-library/test_library.sh` and `npm test`
8. deploy: `~/Developer/jacob-x-studio/dashboard/node_modules/.bin/vercel deploy --prod --yes`

## /library is the catalog of record (Mike, 2026-11-07)

Mike's ruling, verbatim: "remove all mckinley malbrough III references and rebrand as the 'The commit book'". The old `/resources` page was a directory of a third party's Gumroad products credited to McKinley Malbrough III (MM3 Sports); it is deleted and `/resources` 301s to `/library`. Nothing on the site names that seller, brand or storefront any more: `v3/W12-library/build_library.py` asserts it, and `v3/W12-library/test_library.sh` re-checks it on the built page.

`/library` carries The Commit Book's own catalog only: the 10 offerings from `v3/W8-offerings/OFFERINGS.json`, the 12 playbooks on disk, and the 10 free interactive pages. Each item is labelled with its real status. Purchases are off behind the readiness flag.

Tool pages, the rule (Mike's call, 2026-11-07, after the W8 audit): a $0 tool is a real download, a paid tool is notify-only. `v3/W12-library/build_library.py` copies the free deliverables from `v3/W8-offerings/deliverables/` into `site/downloads/tools/` on every build (W8 stays the source of truth), and `v3/W9-experiences/build_pages.py` links a `/tools/<slug>` page to those files when they exist, otherwise it renders the notify form. So a paid tool can never look downloadable, and a parent who gives us nothing still gets a real file. Do not hand-edit `site/tools/*/index.html`: the generator owns that directory, and it decides download-or-notify by what is present in `site/downloads/tools/`.

The build script and the test live in `v3/W12-library/`. The buyer-journey map that /library implements lives in `v3/W12-journey/`.
