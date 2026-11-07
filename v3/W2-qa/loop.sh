#!/bin/bash
# re-run every 20 min until v3/W2-qa/STOP exists; each result appended to runs.log
D=~/Developer/recruiting-calendar/v3/W2-qa
while [ ! -f $D/STOP ]; do /tmp/rc-run.sh >/dev/null; { date; grep -E "✓|×|→|Tests" /tmp/rc-last.log; } >> $D/runs.log; cp /tmp/rc-last.log $D/last-run.log; sleep 1200; done
