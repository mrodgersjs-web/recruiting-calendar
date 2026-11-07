#!/bin/bash
# usage: sf6.sh outname tool 'json-args'  (key read in-process, never printed)
K=$(grep -E '^SOCIALFETCH_API_KEY=' ~/.hermes/.env | cut -d= -f2- | tr -d '"')
R=$(curl -s -m 90 -D /tmp/sf6h.$$ https://api.socialfetch.dev/mcp -H "x-api-key: $K" -H 'content-type: application/json' -H 'accept: application/json, text/event-stream' \
 -d "{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"tools/call\",\"params\":{\"name\":\"$2\",\"arguments\":$3}}")
echo "$R" > raw/$1.json
OK=$(echo "$R" | grep -qE '"isError":true' && echo 0 || echo 1)
python3 -c "import json,sys,datetime;print(json.dumps({'ts':datetime.datetime.now().astimezone().strftime('%Y-%m-%dT%H:%M:%S%z'),'lane':'intel','tool':'/mcp '+sys.argv[1],'args_summary':sys.argv[2][:200],'http':200,'credits_charged':int(sys.argv[3]),'balance_after':'','source':'commit-book/parent-problems'}))" "$2" "$3" "$OK" >> ~/.rig/state/socialfetch/ledger.jsonl
echo "$1 ok=$OK bytes=${#R}"
