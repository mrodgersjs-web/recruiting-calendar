import json,sys,os,re,urllib.request,datetime,subprocess
HOME=os.path.expanduser("~");LEDGER=HOME+"/.rig/state/socialfetch/ledger.jsonl";CAP=118
RAW=os.path.dirname(os.path.abspath(__file__))+"/raw"
def key():
    for l in open(HOME+"/.hermes/.env"):
        if l.startswith("SOCIALFETCH_API_KEY="):return l.split("=",1)[1].strip().strip('"\'')
def spent():
    t=0;d=datetime.datetime.now().strftime("%Y-%m-%d")
    for l in open(LEDGER):
        try:j=json.loads(l)
        except:continue
        if j.get("ts","").startswith(d) and j.get("lane")=="intel":t+=int(j.get("credits_charged") or 0)
    return t
def mcp(method,params):
    b=json.dumps({"jsonrpc":"2.0","id":1,"method":method,"params":params}).encode()
    r=urllib.request.Request("https://api.socialfetch.dev/mcp",data=b,method="POST",headers={"x-api-key":key(),"Content-Type":"application/json","Accept":"application/json, text/event-stream"})
    raw=urllib.request.urlopen(r,timeout=120).read().decode()
    for line in raw.splitlines():
        if line.startswith("data:"):raw=line[5:]
    return json.loads(raw)
def call(tool,args,name):
    if spent()>=CAP: print("CAP");return None
    try:res=mcp("tools/call",{"name":tool,"arguments":args})
    except Exception as e: print("ERR",e);return None
    ok="error" not in res and not res.get("result",{}).get("isError")
    with open(LEDGER,"a") as f:f.write(json.dumps({"ts":datetime.datetime.now().astimezone().strftime("%Y-%m-%dT%H:%M:%S%z"),"lane":"intel","tool":"/mcp "+tool,"args_summary":json.dumps(args)[:300],"http":200,"credits_charged":1 if ok else 0,"balance_after":"","source":"recruiting-calendar/v3-W1-parent-demand"})+"\n")
    json.dump(res,open(f"{RAW}/{name}.json","w"),indent=1)
    return res
if __name__=="__main__":
    if sys.argv[1]=="list":
        r=mcp("tools/list",{});print("\n".join(t["name"] for t in r["result"]["tools"]))
    elif sys.argv[1]=="schema":
        r=mcp("tools/list",{})
        for t in r["result"]["tools"]:
            if t["name"] in sys.argv[2:]:print(t["name"],json.dumps(t["inputSchema"].get("properties"))[:500])
    elif sys.argv[1]=="bal":print(json.dumps(mcp("tools/call",{"name":"billing_balance_get","arguments":{}}))[:400])
