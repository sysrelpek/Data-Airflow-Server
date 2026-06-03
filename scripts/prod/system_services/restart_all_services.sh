#!/usr/bin/env bash
# =============================================================================
# scripts/prod/system_services/restart_all_services.sh
# Restart all Airflow systemd services
# =============================================================================

set -euo pipefail

echo "🔄 Restarting all Airflow services..."

sudo systemctl restart airflow-api.service
sudo systemctl restart airflow-scheduler.service

echo "✅ Services restarted."