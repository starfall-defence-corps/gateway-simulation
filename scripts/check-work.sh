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
    echo -e "  RANK EARNED: ENSIGN"
    echo -e "  The Starfall Defence Corps salutes you."
    echo -e "  ==============================================${RESET}"
    echo ""
    echo -e "  ${YELLOW}${BOLD}Performance Tiers:${RESET}"
    echo -e "  ${DIM}  Under 45 min  — Ace Cadet"
    echo -e "    45–55 min    — Distinguished"
    echo -e "    55–65 min    — Qualified"
    echo -e "    65–75 min    — Passed"
    echo -e "    75+ min      — RTB (Return to Base)${RESET}"
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
