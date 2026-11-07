cd ~/.rig/e2e-harness/suites/recruiting-calendar-v3; curl -sf http://127.0.0.1:4519/ >/dev/null || (cd ~/Developer/recruiting-calendar/site && nohup python3 -m http.server 4519 --bind 127.0.0.1 >/tmp/rc-srv.log 2>&1 &); sleep 1
~/.rig/bin/rig-e2e run recruiting-calendar-v3 "$@" > /tmp/rc-last.log 2>&1; echo "exit $?"
