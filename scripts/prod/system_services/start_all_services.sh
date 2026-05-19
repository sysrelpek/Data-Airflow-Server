#!/usr/bin/env bash
# =============================================================================
# scripts/prod/system_services/start_all_services.sh
# Start all Airflow systemd services
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd -P)"

if [ -f "${PROJECT_ROOT}/.env.prod" ]; then
    set -a
    source "${PROJECT_ROOT}/.env.prod"
    set +a
fi

echo "🚀 Starting all Airflow services..."
sudo systemctl start airflow-webserver airflow-scheduler
echo "✅ Services started."