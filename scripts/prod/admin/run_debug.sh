#!/usr/bin/env bash
# =============================================================================
# scripts/prod/admin/run_debug.sh
# Quick start Airflow with debug logging
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd -P)"

if [ -f "${PROJECT_ROOT}/.env.prod" ]; then
    set -a
    source "${PROJECT_ROOT}/.env.prod"
    set +a
fi

echo "🐞 Starting Data Airflow Server in DEBUG mode..."
cd "${PROJECT_ROOT}"
source .venv/bin/activate
export LOG_LEVEL=DEBUG
exec airflow webserver --port "${AIRFLOW__API__PORT:-8080}" --debug