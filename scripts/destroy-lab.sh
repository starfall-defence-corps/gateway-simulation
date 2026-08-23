#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
DOCKER_DIR="$ROOT_DIR/.docker"

# #56 — stop the exercise scoring poller and clear its log.
if [ -f "$ROOT_DIR/.aria_score.pid" ]; then
    kill "$(cat "$ROOT_DIR/.aria_score.pid")" 2>/dev/null || true
    rm -f "$ROOT_DIR/.aria_score.pid"
fi
rm -f "$ROOT_DIR/.aria_score.jsonl" "$ROOT_DIR/.aria_start"

echo ""
echo "=============================================="
echo "  Decommissioning forward observation post..."
echo "=============================================="
echo ""

# Stop and remove containers
if [ -f "$DOCKER_DIR/docker-compose.yml" ]; then
    docker compose -f "$DOCKER_DIR/docker-compose.yml" down -v 2>&1 | while read -r line; do
        echo "    $line"
    done
fi

# Remove SSH keys
rm -rf "$DOCKER_DIR/ssh-keys"
rm -rf "$ROOT_DIR/workspace/.ssh"

# Remove venv
rm -rf "$ROOT_DIR/venv"

echo ""
echo "  Forward observation post decommissioned."
echo ""
