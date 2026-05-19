#!/usr/bin/env bash
# =============================================================================
# scripts/prod/system_services/restart_all_services.sh
# Restart all Airflow systemd services
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd -P)"

if [ -f "${PROJECT_ROOT}/.env.prod" ]; then
    set -a
    source "${PROJECT_ROOT}/.env.prod"
    set +a
fi

echo "🔄 Restarting all Airflow services..."
sudo systemctl restart airflow-webserver airflow-scheduler
echo "✅ Services restarted."