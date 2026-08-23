#!/usr/bin/env bash
set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
TEST_FILE="$ROOT_DIR/molecule/default/tests/test_gateway.py"

# -- Colors ----------------------------------------------------------------
GREEN='\033[32m'
RED='\033[31m'
CYAN='\033[36m'
YELLOW='\033[33m'
BOLD='\033[1m'
DIM='\033[2m'
RESET='\033[0m'

echo ""
echo -e "  ${CYAN}${BOLD}=============================================="
echo -e "  ARIA — Automated Review & Intelligence Analyst"
echo -e "  Gateway Simulation: Operation First Contact"
echo -e "  ==============================================${RESET}"

cd "$ROOT_DIR"

# Activate project venv if it exists
if [ -f "$ROOT_DIR/venv/bin/activate" ]; then
    source "$ROOT_DIR/venv/bin/activate"
fi

# #50 — real wall-clock for the ARIA performance tier. make setup stamps the
# start; the plugin reads ARIA_ELAPSED_MIN and prints the tier on completion.
if [ -f "$ROOT_DIR/.aria_start" ]; then
    _aria_start="$(cat "$ROOT_DIR/.aria_start" 2>/dev/null || true)"
    if [ -n "${_aria_start:-}" ]; then
        export ARIA_ELAPSED_MIN=$(( ( $(date +%s) - _aria_start ) / 60 ))
    fi
fi

# #56 — hand the availability log to ARIA for the exercise score.
if [ -f "$ROOT_DIR/.aria_score.jsonl" ]; then
    export ARIA_SCORE_LOG="$ROOT_DIR/.aria_score.jsonl"
fi

# Run tests.
ARIA_COLOR=1 python3 -m pytest "$TEST_FILE" --tb=no --no-header -q 2>&1 1>/dev/null \
    | grep -vE '^(assert |FAILED| *\+  where|  *\+  |[0-9]+ (passed|failed))' || true
EXIT_CODE=${PIPESTATUS[0]}

echo ""
if [ $EXIT_CODE -eq 0 ]; then
    echo -e "  ${GREEN}${BOLD}=============================================="
    echo -e "  ARIA: All objectives verified."
    echo -e "  Gateway Simulation status: COMPLETE"
    echo -e ""
    echo -e "  Cadet, you have secured the forward"
    echo -e "  observation post. The Voidborn threat"
    echo -e "  has been neutralised."
    echo -e ""
    echo -e "  The Starfall Defence Corps salutes you."
    echo -e "  ==============================================${RESET}"
    # Rank earned + performance tier are emitted above by the ARIA reporter
    # (aria#9 plugin): a single source of truth, timed from make setup.
else
    echo -e "  ${RED}${BOLD}=============================================="
    echo -e "  ARIA: Deficiencies detected."
    echo -e "  The observation post remains compromised."
    echo -e "  Review the findings above and correct."
    echo -e "  Run 'make test' again when ready."
    echo -e "  ==============================================${RESET}"
fi

echo ""
exit $EXIT_CODE
