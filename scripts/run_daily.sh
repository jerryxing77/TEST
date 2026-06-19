#!/usr/bin/env bash
set -euo pipefail
SESSION="${1:-premarket}"
PROVIDER="${PROVIDER:-demo}"
python -m stock_analyzer --session "$SESSION" --provider "$PROVIDER"
