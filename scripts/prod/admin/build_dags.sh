#!/usr/bin/env bash
# =============================================================================
# scripts/prod/admin/build_dags.sh
# Rebuild all dynamic DAGs from manifests (main production command)
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd -P)"

if [ -f "${PROJECT_ROOT}/.env.prod" ]; then
    set -a
    source "${PROJECT_ROOT}/.env.prod"
    set +a
else
    echo "❌ Error: .env.prod not found!"
    exit 1
fi

echo "🔨 Rebuilding all DAGs from manifests..."
cd "${PROJECT_ROOT}"

# Activate virtual environment
source .venv/bin/activate

# Run the DAG factory (the core of the dynamic DAG system)
python -m dags.dag_factory

echo "✅ DAGs successfully rebuilt and ready for Airflow scheduler."