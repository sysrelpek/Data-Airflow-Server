#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$PROJECT_DIR/.venv"
LOG_DIR="$PROJECT_DIR/logs"
LOG_FILE="$LOG_DIR/debug_$(date +%Y%m%d_%H%M%S).log"

if [ ! -f "$VENV_DIR/bin/activate" ]; then
  rm -rf "$VENV_DIR"
  python3 -m venv "$VENV_DIR"
fi

source "$VENV_DIR/bin/activate"

python -m pip install --upgrade pip >/dev/null

if [ -f "$PROJECT_DIR/requirements.txt" ]; then
  pip install -r "$PROJECT_DIR/requirements.txt"
fi

mkdir -p "$LOG_DIR"
echo "Debug log: $LOG_FILE"

python -m pdb "$PROJECT_DIR/main.py" "$@" 2>&1 | tee "$LOG_FILE"
