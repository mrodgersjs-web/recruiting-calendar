const fs=require("fs");
const cat=require("../../research/00-mm3-offers.json");
const live=require("/tmp/gr/live.json");
const STAMP=new Date().toISOString();
const SF="https://malbrough6.gumroad.com";
const kindOf=s=>/bundle/.test(s)?"bundle":/ebook|guide-ebook/.test(s)?"ebook":"tool";
const OFFERS={};
for(const o of cat){const l=live.find(x=>x.slug===o.slug);
 const price=l.cat_price, lp=Number(l.live_price);
 OFFERS[o.slug]={title:o.name,price:l.cat_price,live_price:lp,price_match:lp===price,kind:kindOf(o.slug),
  status:(l.http===200)?"LIVE":"CHECK",href:`${SF}/l/${o.slug}`,on_storefront_page1:null,verified_at:STAMP};}
const sf=new Set(fs.readFileSync("/tmp/sf_slugs.txt","utf8").trim().split("\n"));
for(const k in OFFERS)OFFERS[k].on_storefront_page1=sf.has(k);
// relevance: story tags -> product slugs (ordered by fit). Only products that really match.
const P={
 offerComp:"ndeiiv",redflag:"buqpl",coachScripts:"college-coach-conversation-scripts",visit:"campus-visit-question-guide-and-scoring-sheet",
 tracker:"recruiting-tracker",contactLog:"recruiting-contact-log-starter",nilCheck:"nil-contract-checklist",nilKit:"qtzruz",
 pathway:"xrczv",field:"mm3-basketball-pathway-field-guide-ebook",profile:"player-profile-reel-template",recruitBundle:"recruit-and-parent-bundle",
 overseas:"szvqp",collegeBundle:"mm3-college-athlete-bundle",localNil:"local-nil-deal-kit-for-athletes",nilTax:"college-athlete-nil-tax-and-income-tracker",
 transition:"athlete-career-transition-workbook",proPath:"pro-pathway-checklist-pack",agentScore:"agent-vetting-scorecard",clearance:"letter-of-clearance-timeline"};
const common=[P.redflag,P.offerComp,P.coachScripts,P.tracker,P.recruitBundle,P.collegeBundle];
const S={
 renfrow:{tags:["football","walk-on","D1"],why:"Preferred walk-on: recruiting-contact, coach-conversation and offer-comparison tools fit",picks:[P.coachScripts,P.offerComp,P.redflag,P.tracker,P.profile,P.recruitBundle]},
 groenewegen:{tags:["softball","club tournaments","outreach emails"],why:"Found at tournaments via coach emails: tracker, scripts, profile/reel brief fit",picks:[P.coachScripts,P.tracker,P.profile,P.visit,P.offerComp,P.recruitBundle]},
 lowe:{tags:["volleyball","walk-on","scholarship offers elsewhere"],why:"Walk-on vs scholarship offers elsewhere: offer comparison and red flags fit",picks:[P.offerComp,P.redflag,P.visit,P.coachScripts,P.tracker,P.recruitBundle]},
 pichardo:{tags:["baseball","walk-on tryout","D1"],why:"Walk-on tryout: scripts, tracker, profile fit",picks:[P.coachScripts,P.profile,P.tracker,P.redflag,P.visit,P.recruitBundle]},
 white:{tags:["basketball","D2 partial aid","D1 transfer","parent video outreach"],why:"D2 partial aid then D1 transfer: basketball pathway, offer comparison, transfer timeline fit",picks:[P.pathway,P.offerComp,P.coachScripts,P.clearance,P.field,P.nilKit]},
 pirosko:{tags:["basketball","D2","academic + athletic"],why:"Regional D2 basketball: pathway planner, visit guide, offer comparison fit",picks:[P.pathway,P.visit,P.offerComp,P.coachScripts,P.field,P.tracker]},
 marpet:{tags:["football","D3","academics first"],why:"Academic-first D3: visit guide, offer comparison, red flags fit",picks:[P.visit,P.offerComp,P.redflag,P.coachScripts,P.tracker,P.recruitBundle]},
 rodenfels:{tags:["track","late starter","D3"],why:"Late starter D3: tracker, scripts, visit guide fit (story HELD)",picks:[P.tracker,P.coachScripts,P.visit,P.profile,P.redflag]},
 perez:{tags:["lacrosse","D3","first-gen"],why:"First-gen D3: visit guide, offer comparison, red flags; parent-focused bundle fits",picks:[P.visit,P.offerComp,P.redflag,P.coachScripts,P.tracker,P.recruitBundle]},
 coward:{tags:["basketball","D3 to D1","transfer"],why:"D3 start then D1 transfers; basketball pathway, transfer timeline, NIL fit",picks:[P.pathway,P.clearance,P.offerComp,P.field,P.nilCheck,P.nilKit]},
 rodriguez:{tags:["wrestling","NAIA","women's"],why:"NAIA recruit: generic recruiting tools fit; nothing wrestling or NAIA specific",picks:[P.redflag,P.offerComp,P.coachScripts,P.visit,P.tracker]},
 butler:{tags:["basketball","JUCO to D1"],why:"JUCO then D1 transfer; basketball pathway, transfer timeline, NIL fit; pro-pathway follows",picks:[P.pathway,P.clearance,P.offerComp,P.field,P.nilKit,P.proPath]},
 wondolowski:{tags:["soccer","D2","found at tournament"],why:"Found at a tournament, D2: scripts, tracker, profile/reel fit; nothing soccer specific",picks:[P.coachScripts,P.tracker,P.profile,P.visit,P.offerComp]},
 "composite-baseball":{tags:["baseball","JUCO"],why:"JUCO-first path: scripts, tracker, offer comparison, transfer timeline fit",picks:[P.coachScripts,P.tracker,P.offerComp,P.clearance,P.redflag]},
 "composite-football":{tags:["football","D3 academics"],why:"D3 academic fit: visit guide, offer comparison, red flags fit",picks:[P.visit,P.offerComp,P.redflag,P.coachScripts,P.tracker,P.recruitBundle]},
 "composite-softball":{tags:["softball","club","D2"],why:"Club tournament discovery: scripts, tracker, profile/reel fit",picks:[P.coachScripts,P.tracker,P.profile,P.visit,P.offerComp,P.recruitBundle]},
 "composite-sprinter":{tags:["track","D3 academics"],why:"Academics-first D3: visit guide, offer comparison fit",picks:[P.visit,P.offerComp,P.tracker,P.coachScripts,P.redflag]},
 "composite-swim":{tags:["swimming","D2","club"],why:"Times-driven D2 outreach: scripts, tracker, profile fit; nothing swim specific",picks:[P.coachScripts,P.tracker,P.profile,P.visit,P.offerComp]},
 "composite-volleyball":{tags:["volleyball","D2","close to home"],why:"Late specializer, D2: visit guide, offer comparison, scripts fit",picks:[P.visit,P.offerComp,P.coachScripts,P.tracker,P.redflag,P.recruitBundle]},
 "composite-wbasketball":{tags:["basketball","NAIA","wide outreach"],why:"Wide outreach to JUCO/D2/NAIA: basketball pathway, scripts, offer comparison fit",picks:[P.pathway,P.coachScripts,P.offerComp,P.tracker,P.field,P.redflag]},
 "composite-wrestling":{tags:["wrestling","D3"],why:"Stepped away and returned, D3 fit: red flags, visit guide, offer comparison fit",picks:[P.redflag,P.visit,P.offerComp,P.coachScripts,P.tracker]},
};
const MAP={},GAPS=[];
for(const [id,s] of Object.entries(S)){
 const picks=[...new Set(s.picks)].slice(0,6);
 MAP[id]={tags:s.tags,relevance_basis:s.why,verified_at:STAMP,
  offers:picks.map((slug,i)=>({rank:i+1,slug,title:OFFERS[slug].title,price:OFFERS[slug].price,href:OFFERS[slug].href,status:OFFERS[slug].status})),count:picks.length};
 if(picks.length<6)GAPS.push({story:id,count:picks.length,note:"Fewer than six credible matches; not padded with unrelated products"});
}
// sport-specific gaps
const sportGaps=[
 ["rodriguez","no wrestling- or NAIA-specific product in the catalog"],["wondolowski","no soccer-specific product"],["composite-swim","no swimming-specific product"],
 ["composite-wrestling","no wrestling-specific product"],["rodenfels","no track/XC-specific product; story HELD (noindex)"],["composite-sprinter","no track-specific product"],
 ["groenewegen","no softball/women's-sport-specific product"],["pichardo","no baseball-specific product"]];
fs.writeFileSync("OFFERS.json",JSON.stringify(OFFERS,null,1));
fs.writeFileSync("STORY-OFFERS.json",JSON.stringify(MAP,null,1));
fs.writeFileSync("GAPS.json",JSON.stringify({fewer_than_six:GAPS,no_sport_specific_product:sportGaps.map(([story,note])=>({story,note}))},null,1));
console.log(Object.keys(OFFERS).length,"offers;",Object.keys(MAP).length,"stories;",GAPS.length,"short");
for(const [k,v] of Object.entries(MAP))console.log(k,v.count);
console.log("price mismatches:",Object.entries(OFFERS).filter(([k,v])=>!v.price_match).map(x=>x[0]));
