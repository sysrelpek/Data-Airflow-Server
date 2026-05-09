#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$PROJECT_DIR/.venv"

if [ ! -f "$VENV_DIR/bin/activate" ]; then
  rm -rf "$VENV_DIR"
  python3 -m venv "$VENV_DIR"
fi

source "$VENV_DIR/bin/activate"

python -m pip install --upgrade pip >/dev/null

if [ -f "$PROJECT_DIR/requirements.txt" ]; then
  pip install -r "$PROJECT_DIR/requirements.txt"
fi

# python -m pytest -q
python "$PROJECT_DIR/main.py"
