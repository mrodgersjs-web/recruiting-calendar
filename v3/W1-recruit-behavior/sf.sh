#!/bin/bash
# usage: sf.sh tool 'json-args'
K=$(grep -E '^SOCIALFETCH_API_KEY=' ~/.hermes/.env | cut -d= -f2- | tr -d '"')
R=$(curl -s -m 60 https://api.socialfetch.dev/mcp -H "x-api-key: $K" -H 'content-type: application/json' -H 'accept: application/json, text/event-stream' \
 -d "{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"tools/call\",\"params\":{\"name\":\"$1\",\"arguments\":$2}}")
echo "$R"
OK=$(echo "$R" | grep -qE '"isError":true|"error":' && echo 0 || echo 1)
python3 -c "import json,sys,datetime;print(json.dumps({'ts':datetime.datetime.now().astimezone().strftime('%Y-%m-%dT%H:%M:%S%z'),'lane':'intel','tool':'/mcp '+sys.argv[1],'args_summary':sys.argv[2],'http':200,'credits_charged':int(sys.argv[3]),'balance_after':'','source':'recruiting-calendar/v3-W1'}))" "$1" "$2" "$OK" >> ~/.rig/state/socialfetch/ledger.jsonl
