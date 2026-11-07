#!/bin/bash
# usage: lh.sh outdir url...
out=$1; shift; cd "$out"
for p in "$@"; do n=$(echo "$p" | tr -c 'a-zA-Z0-9' _); for f in mobile desktop; do
 extra=""; [ $f = desktop ] && extra="--preset=desktop"
 npx -y lighthouse "http://localhost:8791$p" $extra --quiet --chrome-flags="--headless=new" --only-categories=performance --output=json --output-path=$n$f.json >/dev/null 2>&1
 node -e "const r=require('./$n$f.json');const a=r.audits;console.log('$p|$f|'+Math.round(r.categories.performance.score*100)+'|'+a['largest-contentful-paint'].displayValue+'|'+a['cumulative-layout-shift'].displayValue+'|'+a['total-blocking-time'].displayValue+'|'+Math.round(a['total-byte-weight'].numericValue/1024)+'KB|'+(a['largest-contentful-paint-element']?.details?.items?.[0]?.items?.[0]?.node?.selector||''))"
done; done
