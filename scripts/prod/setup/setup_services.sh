#!/usr/bin/env bash
# =============================================================================
# scripts/prod/setup/setup_services.sh
# One-time setup: copies and enables all systemd services
# =============================================================================

set -euo pipefail

# Load production environment
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd -P)"

if [ -f "${PROJECT_ROOT}/.env.prod" ]; then
    set -a
    source "${PROJECT_ROOT}/.env.prod"
    set +a
else
    echo "❌ Error: .env.prod not found in ${PROJECT_ROOT}!"
    exit 1
fi

echo "🔧 Setting up systemd services for Data Airflow Server..."

# Copy service files (create them in system_services/ if missing)
sudo cp "${PROJECT_ROOT}/scripts/prod/system_services/"*.service /etc/systemd/system/ 2>/dev/null || echo "⚠️  No .service files found yet"

sudo systemctl daemon-reload

echo "✅ Services installed."
echo "   Run './scripts/prod/system_services/start_all_services.sh' to start them."