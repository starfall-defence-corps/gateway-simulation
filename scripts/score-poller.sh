#!/usr/bin/env bash
# ARIA exercise scoring poller (#56)
# ==================================
# TCP-probes each scored node's published SSH port every ARIA_SCORE_INTERVAL
# seconds and appends a JSONL availability sample to ARIA_SCORE_LOG:
#
#     {"t": 1690000000, "up": {"sdc-fwd-web": 1, "sdc-fwd-db": 0, ...}}
#
# Started in the background by `make setup`; runs until `make reset`/`destroy`
# kills it (PID in .aria_score.pid). At `make test`, ARIA reads the log and
# reports service availability over the whole run as an exercise score — the
# same way a real cyber-exercise scoring engine measures uptime under pressure.
#
# Config (env):
#   ARIA_SCORE_LOG       path to the JSONL log to append to        (required)
#   ARIA_SCORE_TARGETS   space-separated  name=port  probe targets (required)
#   ARIA_SCORE_HOST      host to probe                     (default 127.0.0.1)
#   ARIA_SCORE_INTERVAL  seconds between polls                     (default 10)
set -u

LOG="${ARIA_SCORE_LOG:?ARIA_SCORE_LOG required}"
TARGETS="${ARIA_SCORE_TARGETS:?ARIA_SCORE_TARGETS required}"
HOST="${ARIA_SCORE_HOST:-127.0.0.1}"
INTERVAL="${ARIA_SCORE_INTERVAL:-10}"

# TCP connect test: 0 = reachable (up), non-zero = down. Uses bash /dev/tcp so
# no nc/curl dependency; the redirect is swallowed on refused connections.
_probe() {
    (exec 3<>"/dev/tcp/$1/$2") 2>/dev/null || return 1
    exec 3>&- 3<&- 2>/dev/null || true
    return 0
}

while :; do
    ts=$(date +%s)
    body=""
    first=1
    for target in $TARGETS; do
        name="${target%%=*}"
        port="${target#*=}"
        if _probe "$HOST" "$port"; then up=1; else up=0; fi
        [ "$first" -eq 1 ] || body="$body,"
        body="$body\"$name\":$up"
        first=0
    done
    printf '{"t":%s,"up":{%s}}\n' "$ts" "$body" >> "$LOG"
    sleep "$INTERVAL"
done
