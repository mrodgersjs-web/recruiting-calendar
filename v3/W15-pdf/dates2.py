import datetime as dt, calendar, sys
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
def nth_weekday(y,m,weekday,n):
    d=dt.date(y,m,1); off=(weekday-d.weekday())%7
    return d+dt.timedelta(days=off+7*(n-1))
for y in (2026,2027,2028,2029):
    e=nth_weekday(y,11,2,2); print(f"Nov {y}: second Wed = {e}, following Wed = {e+dt.timedelta(days=7)}")
for y in (2027,2028,2029):
    print(f"Apr {y}: second Wed = {nth_weekday(y,4,2,2)}")
print("grade map class of 2029: 9th", "2025-26", "10th 2026-27, 11th 2027-28, 12th 2028-29")
print("June 15 after sophomore year =", dt.date(2027,6,15), "| Aug 1 senior-year written aid =", dt.date(2028,8,1))
print("Dec 24", dt.date(2028,12,24).strftime('%a'), "| NJCAA Nov 1", dt.date(2029,11,1).strftime('%a'))
