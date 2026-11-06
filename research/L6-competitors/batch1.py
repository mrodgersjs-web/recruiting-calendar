from sf import call
from concurrent.futures import ThreadPoolExecutor
C={"context":"competitor research for a parent recruiting-info site"}
jobs=[]
for h in ["ncsasports","fieldlevel","captainu","sportsrecruits","prepbaseballreport","on3sports","prepredzone","nextcollegestudentathlete","fullrideuniversity","coachschuman","keithmondillo","dream2elite","sportsforce","baseballpath"]:
    jobs.append(("instagram_profile_get_v2",{"profile":h,"include":["recentMedia"],**C},"ig_"+h))
for n in ["NCSA College Recruiting","FieldLevel","SportsRecruits","Prep Baseball Report","CaptainU","Next College Student Athlete","SportsForce","Recruited To Play","Full Ride University","Dream2Elite"]:
    jobs.append(("facebook_company_ads_list",{"companyName":n,"country":"US",**C},"fbads_"+n.replace(" ","_")))
for h in ["NCSAsports","PrepBaseballReport","CoachSchuman","KeithMondillo","FullRideUniversity","NextCollegeStudentAthlete"]:
    jobs.append(("youtube_channel_videos_list",{"handle":h,"sortBy":"popular",**C},"yt_"+h))
for q in ["NCSA recruiting worth it","NCSA scam","FieldLevel recruiting","SportsRecruits worth it","Prep Baseball Report worth it","recruiting service parents worth it","college recruiting service scam","CaptainU","Next College Student Athlete","PBR showcase worth it"]:
    jobs.append(("reddit_search_list",{"query":q,"sortBy":"relevance","timeframe":"all",**C},"reddit_"+q.replace(" ","_")))
for q in ["NCSA recruiting","recruiting service for my son","PBR showcase"]:
    jobs.append(("threads_search_list",{"query":q,**C},"threads_"+q.replace(" ","_")))
for h in ["ncsasports","fullrideuniversity","coachschuman","prepbaseballreport"]:
    jobs.append(("tiktok_profile_get",{"handle":h,**C},"tt_"+h))
for h in ["NCSA","FieldLevel","PrepBaseball","SportsRecruits"]:
    jobs.append(("twitter_profile_get",{"handle":h,"by":"handle",**C},"x_"+h))
def run(j):
    r=call(*j);ok=r and "error" not in r and not r.get("result",{}).get("isError");print(j[2],"OK" if ok else "FAIL")
with ThreadPoolExecutor(6) as ex: list(ex.map(run,jobs))
