#!/usr/bin/env bash
# =============================================================================
# scripts/prod/system_services/status_all_services.sh
# Show status of all Airflow services
# =============================================================================

set -euo pipefail

echo "📊 Airflow services status:"
echo ""

sudo systemctl status airflow-api.service --no-pager
echo ""
sudo systemctl status airflow-scheduler.service --no-pager