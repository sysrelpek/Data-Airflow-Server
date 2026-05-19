#!/usr/bin/env bash
# =============================================================================
# scripts/prod/system_services/status_server.sh
# Quick status of the entire Data Airflow Server
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd -P)"

if [ -f "${PROJECT_ROOT}/.env.prod" ]; then
    set -a
    source "${PROJECT_ROOT}/.env.prod"
    set +a
fi

echo "=== Data Airflow Server - STATUS ==="
exec "${PROJECT_ROOT}/scripts/prod/system_services/status_all_services.sh"