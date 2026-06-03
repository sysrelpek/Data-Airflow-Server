#!/usr/bin/env bash
# =============================================================================
# scripts/prod/system_services/status_server.sh
# Quick status of the entire Data Airflow Server
# =============================================================================

set -euo pipefail

echo "=== Data Airflow Server - STATUS ==="
echo ""

exec "$(dirname "$0")/status_all_services.sh"