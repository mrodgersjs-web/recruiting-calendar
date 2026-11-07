#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
for dir in access recruitiq personalize segments emerging-sports account billing library downloads price; do
  if [ -d "$ROOT/v3/W11-site-overlay/$dir" ]; then
    mkdir -p "$ROOT/site/$dir"
    cp -R "$ROOT/v3/W11-site-overlay/$dir/." "$ROOT/site/$dir/"
  fi
done
echo "Synced W11 overlay routes into site/"
