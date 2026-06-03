#!/usr/bin/env bash
# =============================================================================
# scripts/prod/admin/build_dags.sh
# Rebuild all dynamic DAGs from manifests
# =============================================================================

set -euo pipefail

# ------------------------------------------------------------------------------
# Find project root by searching upward for a marker file
# ------------------------------------------------------------------------------
find_project_root() {
    local dir="$1"
    while [[ "$dir" != "/" ]]; do
        if [[ -f "$dir/pyproject.toml" || -d "$dir/.git" ]]; then
            echo "$dir"
            return 0
        fi
        dir="$(dirname "$dir")"
    done
    echo "❌ Error: Could not find project root (no pyproject.toml or .git found)"
    exit 1
}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
PROJECT_ROOT="$(find_project_root "$SCRIPT_DIR")"

echo "Starting DAG rebuild..."
echo "  Script location : ${SCRIPT_DIR}"
echo "  Project root    : ${PROJECT_ROOT}"

# ------------------------------------------------------------------------------
# Load .env.prod (non-fatal)
# ------------------------------------------------------------------------------
if [ -f "${PROJECT_ROOT}/.env.prod" ]; then
    set -a
    source "${PROJECT_ROOT}/.env.prod"
    set +a
    echo "  Loaded .env.prod (ENV=${ENV:-not set})"
else
    echo "  ⚠️  .env.prod not found in ${PROJECT_ROOT}"
fi

# ------------------------------------------------------------------------------
# Activate virtual environment
# ------------------------------------------------------------------------------
if [ -f "${PROJECT_ROOT}/.venv/bin/activate" ]; then
    # shellcheck disable=SC1090
    source "${PROJECT_ROOT}/.venv/bin/activate"
    echo "  Virtual environment activated"
else
    echo "  ⚠️  Virtual environment not found"
fi

# ------------------------------------------------------------------------------
# Rebuild DAGs
# ------------------------------------------------------------------------------
echo "Rebuilding DAGs from manifests..."
cd "${PROJECT_ROOT}"

python -m dags.dag_factory

echo ""
echo "DAGs successfully rebuilt."