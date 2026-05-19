#!/usr/bin/env bash
# =============================================================================
# scripts/prod/system_services/stop_all_services.sh
# Stop all Airflow systemd services
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd -P)"

if [ -f "${PROJECT_ROOT}/.env.prod" ]; then
    set -a
    source "${PROJECT_ROOT}/.env.prod"
    set +a
fi

echo "🛑 Stopping all Airflow services..."
sudo systemctl stop airflow-webserver airflow-scheduler
echo "✅ Services stopped."