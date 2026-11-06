from sf import call
from concurrent.futures import ThreadPoolExecutor
C={"context":"competitor research for a parent recruiting-info site"}
J=[]
for h in ["ncsa","prepbaseball","on3recruits","captainurecruiting","fullrideu","nextlevelbaseball","trackbeast","recruitedtoplay","nowusports"]:
    J.append(("instagram_profile_get_v2",{"profile":h,"include":["recentMedia"],**C},"ig2_"+h))
for h in ["keithmondillo","coachschuman","prepredzone","fieldlevel"]:
    J.append(("instagram_profile_media_list_v2",{"profile":h,"tab":"reels",**C},"igreels_"+h))
for q in ["NCSA college recruiting","Prep Baseball Report","Full Ride University recruiting"]:
    J.append(("youtube_search_list",{"query":q,**C},"ytsearch_"+q.replace(" ","_")))
for h in ["@NCSA","@KeithMondillo"]:
    J.append(("youtube_channel_get",{"handle":h,**C},"ytch_"+h[1:]))
for pid in ["1shq2rt","1vig5pe","1pvfd3s","1xcd518"]:
    J.append(("reddit_post_comments_list",{"postId":pid,**C},"rcom_"+pid))
J.append(("facebook_company_ads_list",{"companyName":"Next College Student Athlete","country":"ALL",**C},"fbads_NCSA2"))
J.append(("facebook_company_ads_list",{"companyName":"Keith Mondillo","country":"US",**C},"fbads_Keith_Mondillo"))
J.append(("facebook_company_ads_list",{"companyName":"Coach Schuman","country":"US",**C},"fbads_Coach_Schuman"))
J.append(("facebook_company_ads_list",{"companyName":"BaseballPath","country":"US",**C},"fbads_BaseballPath"))
def run(j):
    r=call(*j);ok=r and "error" not in r and not r.get("result",{}).get("isError");print(j[2],"OK" if ok else "FAIL")
with ThreadPoolExecutor(6) as ex: list(ex.map(run,J))
