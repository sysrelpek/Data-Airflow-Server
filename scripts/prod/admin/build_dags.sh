#!/usr/bin/env bash
# =============================================================================
# scripts/prod/admin/build_dags.sh
# Rebuild all dynamic DAGs from YAML manifests
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../../.." && pwd -P)"

if [ -f "${PROJECT_ROOT}/.env.prod" ]; then
    set -a
    source "${PROJECT_ROOT}/.env.prod"
    set +a
fi

# Use full path to Python from the virtual environment
PYTHON_BIN="${PROJECT_ROOT}/.venv/bin/python"

if [ ! -f "$PYTHON_BIN" ]; then
    echo "❌ Error: Virtual environment Python not found at $PYTHON_BIN"
    exit 1
fi

echo "🔨 Building JSON manifests from YAML configs..."
"$PYTHON_BIN" -m business_lib.core.build_all_manifests

echo ""
echo "🚀 Rebuilding all DAGs from manifests..."
cd "${PROJECT_ROOT}"

"$PYTHON_BIN" -m dags.dag_factory

echo ""
echo "✅ DAGs successfully rebuilt."