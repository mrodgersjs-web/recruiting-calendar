#!/bin/bash
# usage: sf7.sh outname tool 'json-args'
L=~/.rig/state/socialfetch/ledger.jsonl
LANE=${LANE:-intel}; N=$(grep commit-book/ten-layers $L | grep -c "\"lane\": \"$LANE\""); CAP=40; [ $LANE = commitbook ] && CAP=150
K=$(grep -E '^SOCIALFETCH_API_KEY=' ~/.hermes/.env | cut -d= -f2- | tr -d '"')
R=$(curl -s -m 60 https://api.socialfetch.dev/mcp -H "x-api-key: $K" -H 'content-type: application/json' -H 'accept: application/json, text/event-stream' -d "{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"tools/call\",\"params\":{\"name\":\"$2\",\"arguments\":$3}}")
echo "$R" > "$(dirname $0)/raw/$1.json"
OK=$(echo "$R" | grep -qE '"isError":true|"error":' && echo 0 || echo 1)
python3 -c "import json,sys,datetime;print(json.dumps({'ts':datetime.datetime.now().astimezone().strftime('%Y-%m-%dT%H:%M:%S%z'),'lane':sys.argv[4],'tool':'/mcp '+sys.argv[1],'args_summary':sys.argv[2],'http':200,'credits_charged':int(sys.argv[3]),'balance_after':'','source':'commit-book/ten-layers'}))" "$2" "$3" "$OK" "$LANE" >> $L
echo "$1 ok=$OK bytes=${#R}"
