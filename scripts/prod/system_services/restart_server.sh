#!/usr/bin/env bash
# =============================================================================
# scripts/prod/system_services/restart_server.sh
# Quick restart of the entire Data Airflow Server
# =============================================================================

set -euo pipefail

echo "=== Data Airflow Server - RESTART ==="
echo ""

exec "$(dirname "$0")/restart_all_services.sh"