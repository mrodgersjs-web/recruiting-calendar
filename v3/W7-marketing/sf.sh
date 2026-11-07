#!/bin/bash
# usage: sf.sh outname tool 'json-args'   lane commitbook, cap 400
L=~/.rig/state/socialfetch/ledger.jsonl
N=$(grep -c '"source": "commit-book/marketing"' $L); [ "$N" -ge 380 ] && { echo CAP; exit 9; }
K=$(grep -E '^SOCIALFETCH_API_KEY=' ~/.hermes/.env | cut -d= -f2- | tr -d '"')
R=$(curl -s -m 90 https://api.socialfetch.dev/mcp -H "x-api-key: $K" -H 'content-type: application/json' -H 'accept: application/json, text/event-stream' -d "{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"tools/call\",\"params\":{\"name\":\"$2\",\"arguments\":$3}}")
echo "$R" > "$(dirname $0)/raw/$1.json"
OK=$( [ ${#R} -lt 50 ] && echo 0 || (echo "$R" | grep -qE "\"isError\":true|bad_request" && echo 0 || echo 1))
python3 -c "import json,sys,datetime;print(json.dumps({'ts':datetime.datetime.now().astimezone().strftime('%Y-%m-%dT%H:%M:%S%z'),'lane':'commitbook','tool':'/mcp '+sys.argv[1],'args_summary':sys.argv[2][:200],'http':200,'credits_charged':int(sys.argv[3]),'balance_after':'','source':'commit-book/marketing'}))" "$2" "$3" "$OK" >> $L
echo "$1 ok=$OK bytes=${#R}"
