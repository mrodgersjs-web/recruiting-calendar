"""Build site/segments/segments.json from the W7/W6 markdown sources (no hand-copied layer text)."""
import json, re, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
TL = (ROOT/"v3/W7-segments/TEN-LAYERS.md").read_text()
MK = (ROOT/"v3/W7-segments/MARKET.md").read_text()

def chains():
    out = []
    for blk in re.split(r"\n(?=## \d )", TL)[1:]:
        m = re.match(r"## (\d) (.+)", blk)
        n, title = int(m.group(1)), m.group(2).strip()
        hit = re.search(r"Segments hit hardest: (.+)", blk).group(1).strip()
        layers = []
        for ln in blk.splitlines():
            r = re.match(r"\|(\d+)\|([^|]*)\|(.*)\|(EVIDENCED|INFERRED)\|(.*)\|$", ln)
            if r:
                layers.append(dict(n=int(r.group(1)), name=r.group(2).strip(), text=r.group(3).strip(),
                                   status=r.group(4), source=r.group(5).strip()))
        out.append(dict(id=n, title=title, hardest=[s.strip() for s in hit.split(",")], layers=layers))
    return out

def sizing():
    rows = []
    for ln in MK.splitlines():
        c = [x.strip() for x in ln.strip("|").split("|")]
        if ln.startswith("|") and len(c) == 10 and c[1][0].isdigit() and "," in c[1]:
            rows.append(dict(sport=c[0], hs=c[1], growth=c[2], ncaa=c[3], ratio=c[4], spend2019=c[5], skew=c[6], jrsr=c[7], paying=c[8], ceiling=c[9]))
    return rows


# Hand-authored from MARKET.md + PROBLEMS.md. Every `href` must resolve to a real page in site/ (tested).
# `planned_route` records the route the brief named where the real page does not exist yet.
SEGMENTS = [
 {"id":1,"key":"planner","name":"9th/10th Grade Planner","tag":"Early, curious, not yet panicking",
  "who":"Parent of a 9th or 10th grader. No coach has called. The risk is a paid service pitching a young athlete, and spending before the rules say anyone may reply.",
  "chains":[1,5,3],
  "plan":[
   {"step":"This month: read the by-grade checklist","why":"Problem #1 in the Social Fetch sample: 'just give me the steps'.","tool":"Start here by grade","href":"/start/","planned_route":"/start"},
   {"step":"Put the contact dates on your own calendar","why":"D1/D2 coaches generally cannot reply to you before the dates in the bylaws. Emailing earlier gets no answer by rule.","tool":"Rule calendar","href":"/calendar/","planned_route":"/calendar"},
   {"step":"Check every class against the NCAA-approved list","why":"Core-course mistakes cannot be fixed late.","tool":"Eligibility: the 2 hard deadlines","href":"/playbooks/eligibility-2-hard-deadlines/","planned_route":"/playbooks/eligibility-2-hard-deadlines"},
   {"step":"If you live in the Denver metro, check camps and trainers against their sources","why":"Every row shows its source and check date. Denver area only.","tool":"Denver metro camps & trainers","href":"/personalize/","planned_route":"/personalize"},
   {"step":"Hold your money until a coach has actually written","why":"Spend nothing on showcases or services yet.","tool":"Family spending check (view C)","href":"#view-c","planned_route":"#view-c"}],
  "story":{"label":"Tori: started in eighth grade and still found a home","href":"/sports/lacrosse"},
  "spend_note":"Free path. Budget line to protect: nothing recurring before sophomore summer."},
 {"id":2,"key":"late","name":"Late-Start Junior/Senior Panic","tag":"Behind, and feels it",
  "who":"Junior or senior with no list, no film plan, no replies. Roster spots are filling. The risk is mass-emailing the wrong level and buying a panic service.",
  "chains":[2,4,5],
  "plan":[
   {"step":"Reset the level: D2, D3, NAIA and JUCO still fill rosters in senior year","why":"Chain 2 layer 3: aiming too high is the usual cause.","tool":"Late Bloomer playbook","href":"/playbooks/late-bloomer/","planned_route":"/playbooks/late-bloomer"},
   {"step":"Read the by-grade checklist for what is still open","why":"It tells you what is allowed now and what date comes next.","tool":"Start here by grade","href":"/start/","planned_route":"/start"},
   {"step":"Get your earliest contact dates, a 30-school target list and an athlete-voice email","why":"Coaches spot parent-written mail; a short, realistic list beats mass email.","tool":"Reach coaches yourself","href":"/access/","planned_route":"/access"},
   {"step":"Open the Eligibility Center account if you have not","why":"Without it, no D1/D2 official visit.","tool":"Eligibility Center cost answer","href":"/answers/ncaa-eligibility-center-account-cost/","planned_route":"/answers/ncaa-eligibility-center-account-cost"}],
  "story":{"label":"Diego: junior college is a real first step","href":"/sports/baseball"},
  "spend_note":"Spend only on verified essentials. One targeted camp, after a coach has replied."},
 {"id":3,"key":"burned","name":"Burned by a Paid Recruiting Service or Showcase Circuit","tag":"Paid $1,500\u2013$4,200 and wants out",
  "who":"Family that paid a recruiting service or ran the showcase circuit and is asking 'was it worth it, and how do we cancel?' Parents in the sample report up to about $4K plus monthly fees.",
  "chains":[3,4,5],
  "plan":[
   {"step":"Check your athlete against sourced standards before paying anyone to judge level","why":"Chain 3: services did little families could not do; prices hidden until the end of the call.","tool":"Standards & fit explorer","href":"/recruitiq/","planned_route":"/recruitiq"},
   {"step":"Compare what you bought with what is free","why":"Chain 3: services did little families could not do; prices hidden until the end of the call.","tool":"Service vs DIY comparison","href":"/compare/","planned_route":"/compare"},
   {"step":"Rebuild the timeline and tracker yourself","why":"The thing parents liked about services was the contact timeline.","tool":"Rule calendar","href":"/calendar/","planned_route":"/calendar"},
   {"step":"Spot the next pitch before it lands","why":"Red-flag checklist for sales calls and contracts.","tool":"Red flags checklist (coming soon)","href":"/tools/red-flags/","planned_route":"/tools/red-flags"},
   {"step":"Redirect the remaining budget (view C)","why":"The $110 NCAA fee is the one cost every D1/D2 path needs.","tool":"Reallocator","href":"#view-c","planned_route":"#view-c"}],
  "story":{"label":"Men's basketball: zero D1 offers, a D3 start, a long climb","href":"/sports/basketball"},
  "spend_note":"Cancellation terms vary by contract. Read yours; this site gives education, not legal advice."},
 {"id":4,"key":"academic","name":"High-Academic D3 / Ivy / Merit-Aid Family","tag":"Admissions and recruiting at once",
  "who":"Strong student, often swimming, tennis, lacrosse or golf. The questions are early-action with coach support and how athletic and academic aid stack.",
  "chains":[5,4,6],
  "plan":[
   {"step":"Lead with academic aid, then ask the coach about fit","why":"D3 gives no athletic scholarships; aid is academic or need-based.","tool":"D3 path: academic aid first","href":"/playbooks/d3-academic-aid-first/","planned_route":"/playbooks/d3-academic-aid-first"},
   {"step":"Do the roster and aid math before you fall for a school","why":"Know the spots and the real net cost.","tool":"Roster and aid math","href":"/math/","planned_route":"/math"},
   {"step":"Check whether D3 offers athletic scholarships (it does not)","why":"Clears up the most common wrong assumption.","tool":"Parent answer","href":"/answers/does-d3-offer-athletic-scholarships/","planned_route":"/answers"},
   {"step":"Compare offers side by side before deadlines","why":"Early-decision commitments bind.","tool":"Offers & signing playbook","href":"/playbooks/offer-and-signing/","planned_route":"/playbooks/offer-and-signing"}],
  "story":{"label":"Football: no D1 offers? Division III can build an athlete","href":"/sports/football"},
  "spend_note":"Highest household spend in the Aspen data ($100K+ band). Spend on visits that matter, not on volume."},
 {"id":5,"key":"clock","name":"Clock/Mark Sport: Track, XC, Swim","tag":"Your times are the résumé",
  "who":"Athlete whose numbers are public. The lever is a verified mark at a meet coaches use, a clear list, and the right email, not a flashy video.",
  "chains":[4,5,6],
  "plan":[
   {"step":"Know the track dates and rules for your class year","why":"Track recruiting dates differ from team sports.","tool":"Track rules by class year","href":"/rules/track/2029/","planned_route":"/rules"},
   {"step":"Use the marks-to-roster playbook","why":"Turn a verified time into a target list.","tool":"Track & field: marks to roster","href":"/playbooks/track-field-marks/","planned_route":"/playbooks/track-field-marks"},
   {"step":"Check when track coaches may contact you","why":"Direct answer with the bylaw cited.","tool":"Parent answer","href":"/answers/when-can-track-coaches-contact-athletes/","planned_route":"/answers"},
   {"step":"Email in the athlete's voice with the mark in the subject","why":"Coaches skim; grad year and mark first.","tool":"Reach coaches yourself","href":"/access/","planned_route":"/access"}],
  "story":{"label":"Maya: her times were good, nobody knew yet","href":"/sports/swimming"},
  "spend_note":"Aspen 2019 average for track is $191 and swimming $786, so the budget is modest. Protect it."},
 {"id":6,"key":"emerging","name":"Emerging Sport or JUCO/NAIA Transfer Path","tag":"A new door, thin information",
  "who":"Girls' flag football, women's wrestling, or a family weighing JUCO then transfer. Few playbooks exist; the college pathway is new.",
  "chains":[1,2,5],
  "plan":[
   {"step":"Find your sport's pathway checklist","why":"Girls flag football, girls wrestling and boys volleyball are growing faster than most guides track.","tool":"Emerging sports checklist","href":"/emerging-sports/","planned_route":"/emerging-sports"},
   {"step":"Read the JUCO-to-D1 path","why":"Many families use a JUCO year as a real first step.","tool":"JUCO to D1 playbook","href":"/playbooks/juco-to-d1/","planned_route":"/playbooks/juco-to-d1"},
   {"step":"Learn the walk-on route where no scholarship exists yet","why":"New programs often fill through tryouts.","tool":"Walk-on playbook","href":"/playbooks/walk-on/","planned_route":"/playbooks/walk-on"},
   {"step":"Use the by-grade checklist and rule calendar","why":"Rules for new sports lag; confirm each date.","tool":"Start here by grade","href":"/start/","planned_route":"/start"},
   {"step":"See the full playbook shelf","why":"All sport and stage playbooks.","tool":"Playbooks","href":"/playbooks/","planned_route":"/playbooks"}],
  "story":{"label":"Wrestling: stepped away? a new program can still find you","href":"/sports/wrestling"},
  "spend_note":"Cheap sports but a high information need. An emerging-sports program list is not on the site yet."},
]

C = chains()
data = {
 "generated_from": ["v3/W7-segments/MARKET.md","v3/W7-segments/TEN-LAYERS.md","v3/W7-segments/SOLUTIONS.md","v3/W6-problems/PROBLEMS.md"],
 "honesty": {"evidenced": sum(l["status"]=="EVIDENCED" for c in C for l in c["layers"]),
             "inferred": sum(l["status"]=="INFERRED" for c in C for l in c["layers"]),
             "note": "Evidenced = Social Fetch sample (hand-tagged, directional, paraphrased, no usernames) or a primary NCAA rule. Inferred = our working hypothesis, not yet tested with families."},
 "segments": SEGMENTS,
 "chains": C,
 "badges": {"EVIDENCED": "EVIDENCED \u2014 Social Fetch / Primary Rule", "INFERRED": "INFERRED \u2014 Working Hypothesis"},
 "spending": {
   "source": "Aspen Institute Project Play, National Youth Sports Parent Survey, 2024 (n=1,848, fielded Nov-Dec 2024)",
   "url": "https://www.aspeninstitute.org/wp-content/uploads/2025/06/National-Youth-Sports-Parent-Survey-FINAL.pdf",
   "avg_primary_sport": 1016, "avg_other_sports": 475,
   "by_income": [{"label":"Under $50K","amt":604},{"label":"$50K-$99K","amt":961},{"label":"$100K+","amt":1591}],
   "by_sport_2024": [{"label":"Dance","amt":2048},{"label":"Baseball","amt":1113},{"label":"Soccer","amt":910},{"label":"Basketball","amt":876},{"label":"Tackle football","amt":634},{"label":"Flag football","amt":444}],
   "travel_lodging_avg": 278, "travel_lodging_100k": 429,
   "ncaa_cert_fee": 110, "ncaa_cert_url": "https://fs.ncaa.org/Docs/eligibility_center/Student_Resources/Registration_Checklist.pdf"},
 "sizing": {
   "label": "MODEL ASSUMPTION, not a census figure",
   "assumptions": ["Jr+Sr = HS participants / 4 x 2", "College intent 30% (ESTIMATE)", "Paying share by income skew H 55% / M 40% / L 30% (ESTIMATE)", "Revenue ceiling = families x $149 membership; real conversion would be a few percent"],
   "total_serviceable_families": 496245, "conversion_example": {"rate": 0.02, "families": 9925},
   "participation_source": "NFHS 2024-25 participation survey (record 8,266,244); division percentages from NCAA Probability of Competing Beyond HS (derived, rounded)",
   "rows": sizing()},
}
p = ROOT/"site/segments/segments.json"
p.write_text(json.dumps(data, indent=1, ensure_ascii=False))
print(len(C), data["honesty"], len(data["sizing"]["rows"]))
