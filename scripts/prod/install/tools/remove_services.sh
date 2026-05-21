#!/usr/bin/env bash
# =============================================================================
# scripts/prod/setup/remove_services.sh
# Cleanup: stops and removes all systemd services
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd -P)"

if [ -f "${PROJECT_ROOT}/.env.prod" ]; then
    set -a
    source "${PROJECT_ROOT}/.env.prod"
    set +a
fi

echo "🧹 Removing Data Airflow Server systemd services..."

sudo systemctl stop airflow-webserver airflow-scheduler airflow-worker 2>/dev/null || true
sudo systemctl disable airflow-webserver airflow-scheduler airflow-worker 2>/dev/null || true
sudo rm -f /etc/systemd/system/airflow-*.service
sudo systemctl daemon-reload

echo "✅ All services removed."