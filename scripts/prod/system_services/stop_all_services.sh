#!/usr/bin/env bash
# =============================================================================
# scripts/prod/system_services/stop_all_services.sh
# Stop all Airflow systemd services
# =============================================================================

set -euo pipefail

echo "🛑 Stopping all Airflow services..."

sudo systemctl stop airflow-api.service
sudo systemctl stop airflow-scheduler.service

echo "✅ Services stopped."