# W3 Release: HOLD (not deployed) - 2026-11-05
Gate check result: FAIL, no preview or prod deploy made.
- v3/W3-factcheck/FACTCHECK.md: MISSING
- v3/W2-qa/last-run.log: MISSING (no green QA run on record)
- Legal HIGH #3 strike-through price: still present (site/calendar/index.html, site/price/index.html)
- Legal HIGH #1 disclaimer line: present in 54 html files (looks fixed)
- Legal HIGH #4 (unwired email promises), #6 (auto-renew checkbox), #2 (logo end-card videos): not verified as fixed
- W2-1 (2amyi8vy3GLeRgRL) done status: not confirmed
Current production (unchanged, rollback target): https://recruiting-calendar-g8ydfrwxt-michael-rodgers-projects-e4209a00.vercel.app
Rollback command: ~/Developer/jacob-x-studio/dashboard/node_modules/.bin/vercel rollback https://recruiting-calendar-g8ydfrwxt-michael-rodgers-projects-e4209a00.vercel.app --yes
v3/W2-qa/STOP not touched (loop must still produce a green run).
Re-run this release once all gate items exist.
