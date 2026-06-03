#!/usr/bin/env bash
# =============================================================================
# scripts/prod/system_services/stop_server.sh
# Quick stop of the entire Data Airflow Server
# =============================================================================

set -euo pipefail

echo "=== Data Airflow Server - STOP ==="
echo ""

exec "$(dirname "$0")/stop_all_services.sh"