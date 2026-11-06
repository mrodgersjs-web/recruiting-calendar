const fs=require('fs');
const base='https://recruiting-calendar.vercel.app';
const routes={
 '/start':'Free grade-by-grade recruiting steps (live)',
 '/access':'Access routes for families (W10-access; not yet live in site/)',
 '/recruitiq':'RecruitIQ readiness (W10-recruitiq; not yet live in site/)',
 '/personalize':'Personalized plan (W10-personalization; not yet live in site/)',
 '/segments':'Sport/segment hub (not yet live in site/)',
 '/emerging-sports':'Emerging sports: girls wrestling, flag football (not yet live in site/)',
 '/resources':'Third-party resource directory (built here, site/resources/)'};
const seg=(id,label,ads,stories,hooks,primary,secondary,sport_filter,angle)=>({id,label,ads,stories,hooks,primary_route:primary,secondary_routes:secondary,resources_story_filter:sport_filter,primary_angle:angle});
const segments=[
 seg('football','Football parents',['F1','F2','F3'],['marpet','renfrow','composite-football'],
  ['Every date a coach can contact your kid, with the rule number','Late isn\'t over: an honest next 30 days for a junior/senior','Before you pay a recruiting service, read this comparison'],
  '/start',['/personalize','/recruitiq','/resources'],'renfrow','Proof over hype; bylaw-cited calendar vs Full Ride U free calendar ad'),
 seg('travel_baseball_softball','Travel baseball / softball',['S1','S2','S3'],['composite-softball','composite-baseball','groenewegen','pichardo'],
  ['Check which showcases fit before the next one','D1 scholarships are split across a roster: see the math'],
  '/start',['/personalize','/segments','/resources'],'groenewegen','Showcase ROI and honest roster-split math'),
 seg('club_volleyball','Club volleyball',['V1','V2','V3'],['composite-volleyball','lowe'],
  ['The recruiting dates are different for your sport','What to write in the first email to a college coach'],
  '/start',['/personalize','/segments','/resources'],'lowe','Sport-specific dates; first-email words'),
 seg('wrestling_incl_girls','Wrestling incl. girls',['W1','W2'],['rodriguez','composite-wrestling'],
  ['Women\'s wrestling is now an NCAA D-III championship sport','The two Eligibility Center dates that can cost eligibility ($9, no sales call)'],
  '/emerging-sports',['/start','/recruitiq','/resources'],'rodriguez','New-sport pride; eligibility dates'),
 seg('aau_basketball','AAU basketball',['L1'],['butler','white','coward','composite-wbasketball','pirosko'],
  ['Late isn\'t over: an honest next 30 days for a junior/senior'],
  '/access',['/start','/recruitiq','/resources'],'butler','JUCO/transfer paths; plain-cost framing'),
 seg('late_start_jr_sr','Late-start junior/senior families',['L1','L2','F2'],['marpet','butler','composite-baseball'],
  ['Late isn\'t over: an honest next 30 days for a junior/senior','The two Eligibility Center dates that can cost eligibility ($9, no sales call)'],
  '/recruitiq',['/personalize','/start','/resources'],'butler','Fast honest readiness check, then 30-day plan')];
const small=[
 {id:'girls_flag_football',ads:['G1'],primary_route:'/emerging-sports',note:'Small $50 test; program list is a sourcing GAP so copy says where to look, not which schools. No story exists; resources filter n/a.'},
 {id:'track_xc',ads:['T1'],primary_route:'/segments',stories:['rodenfels','composite-sprinter'],note:'Small $50 test; rodenfels story page is HELD (noindex), use composite-sprinter for any creative link until released.'}];
const out={generated:'2026-11-06',status:'DRAFT, nothing launched or posted',landing_base:base,routes,
 live_status_note:'Only /start (and /resources once released) exist in site/ today. The other routes are mapped from sibling W10 builds; do not run any ad pointing at a route until it is live and Mike approves the exact text.',
 buyer_segments:segments,small_tests:small,
 out_of_scope_paid:['hs_coaches_ads','club_directors','single_parent_first_gen']};
fs.writeFileSync('landing-page-map.json',JSON.stringify(out,null,1));
