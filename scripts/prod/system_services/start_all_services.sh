#!/usr/bin/env bash
# =============================================================================
# scripts/prod/system_services/start_all_services.sh
# Start all Airflow systemd services
# =============================================================================

set -euo pipefail

echo "🚀 Starting all Airflow services..."

sudo systemctl start airflow-api.service
sudo systemctl start airflow-scheduler.service

echo "✅ Services started."