#!/usr/bin/env bash
# =============================================================================
# scripts/prod/admin/run.sh
# Quick start Airflow in normal mode (manual run)
# =============================================================================

set -euo pipefail

# Robust project root detection
find_project_root() {
    local dir="$1"
    while [[ "$dir" != "/" ]]; do
        if [[ -f "$dir/pyproject.toml" || -d "$dir/.git" ]]; then
            echo "$dir"
            return 0
        fi
        dir="$(dirname "$dir")"
    done
    echo "❌ Error: Could not find project root"
    exit 1
}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
PROJECT_ROOT="$(find_project_root "$SCRIPT_DIR")"

echo "🚀 Starting Data Airflow Server (normal mode)..."
echo "   Project root: ${PROJECT_ROOT}"

cd "${PROJECT_ROOT}"

if [ ! -f ".venv/bin/activate" ]; then
    echo "❌ Error: Virtual environment not found at .venv/"
    exit 1
fi

source .venv/bin/activate

# Use port from environment or default to 8080
PORT="${AIRFLOW__API__PORT:-8080}"

exec airflow api-server --host 0.0.0.0 --port "$PORT"