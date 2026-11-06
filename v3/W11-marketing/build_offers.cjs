// Builds site/resources/offers.json from W10-offers (read-only inputs).
const fs=require('fs'),path=require('path');
const W10=path.join(__dirname,'..','W10-offers');
const rd=f=>JSON.parse(fs.readFileSync(path.join(W10,f),'utf8'));
const offers=rd('OFFERS.json'),live=rd('LIVE-CHECK.json'),story=rd('STORY-OFFERS.json'),gaps=rd('GAPS.json');
const CAT={ // category by slug (5 filter categories)
 'buqpl':'Parent Guides','szvqp':'Mental/Performance','ndeiiv':'Coach Outreach','xrczv':'Parent Guides',
 'qtzruz':'NIL','qnxpr':'Mental/Performance','mzsvsy':'Parent Guides','mm3-college-athlete-bundle':'Parent Guides',
 'college-coach-conversation-scripts':'Coach Outreach','campus-visit-question-guide-and-scoring-sheet':'Parent Guides',
 'overseas-contract-questions':'Mental/Performance','agent-vetting-scorecard':'Parent Guides','overseas-budget-planner':'Mental/Performance',
 'letter-of-clearance-timeline':'Mental/Performance','nil-contract-checklist':'NIL','recruiting-tracker':'Recruiting Trackers',
 'aspiring-agent-launch-kit':'Mental/Performance','player-profile-reel-template':'Coach Outreach','going-pro-overseas-bundle':'Mental/Performance',
 'recruit-and-parent-bundle':'Parent Guides','pro-pathway-checklist-pack':'Mental/Performance','overseas-offer-budget-starter':'Mental/Performance',
 'recruiting-contact-log-starter':'Recruiting Trackers','youth-travel-ball-season-planner':'Recruiting Trackers',
 'athlete-career-transition-workbook':'Mental/Performance','mm3-basketball-pathway-field-guide-ebook':'Parent Guides',
 'aspiring-agent-bundle':'Mental/Performance','local-nil-deal-kit-for-athletes':'NIL','wnba-cba-pay-and-contract-guide':'NIL',
 'college-athlete-nil-tax-and-income-tracker':'NIL'};
const out={generated_from:'v3/W10-offers/{OFFERS,STORY-OFFERS,GAPS,LIVE-CHECK}.json',verified_at:null,
 seller:{name:'McKinley Malbrough III',brand:'MM3 Sports',storefront:'https://malbrough6.gumroad.com',credential:'J.D., MS-HRM, certified WNBA player agent; not a licensed attorney'},
 attribution:'By McKinley Malbrough III, MM3 Sports. Educational material, not legal, tax or financial advice.',
 categories:['NIL','Coach Outreach','Recruiting Trackers','Mental/Performance','Parent Guides'],
 offers:[],stories:[]};
for(const l of live){
  const o=offers[l.slug]; if(!o) throw new Error('missing '+l.slug);
  const lp=Number(l.live_price);
  if(lp!==o.price) throw new Error('price mismatch '+l.slug);
  if(!CAT[l.slug]) throw new Error('no cat '+l.slug);
  out.offers.push({slug:l.slug,title:l.live_title,price:lp,price_label:lp===0?'$0+ (free / pay what you want)':'$'+lp,
   free:lp===0,kind:o.kind,category:CAT[l.slug],href:l.url,http:l.http,verified_at:o.verified_at});
  out.verified_at=out.verified_at||o.verified_at;
}
const gapMap={};for(const g of gaps.fewer_than_six)gapMap[g.story]=g.note;
const nosp={};for(const g of gaps.no_sport_specific_product)nosp[g.story]=g.note;
for(const [k,v] of Object.entries(story)){
  out.stories.push({slug:k,tags:v.tags,relevance_basis:v.relevance_basis,count:v.offers.length,
   gap:k in gapMap?gapMap[k]:null,no_sport_specific:nosp[k]||null,held:k==='rodenfels',
   offers:v.offers.map(x=>x.slug)});
}
fs.writeFileSync(path.join(__dirname,'..','..','site','resources','offers.json'),JSON.stringify(out,null,1));
console.log(out.offers.length,out.stories.length,out.stories.filter(s=>s.count===6).length,out.stories.filter(s=>s.count===5).length);
