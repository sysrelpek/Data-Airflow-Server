#!/usr/bin/env bash
# =============================================================================
# scripts/prod/install/setup_services.sh
# One-time setup: copies and enables all systemd services
# =============================================================================

set -euo pipefail

# ------------------------------------------------------------------------------
# Robust PROJECT_ROOT detection
# ------------------------------------------------------------------------------
find_project_root() {
    local dir="$1"
    while [[ "$dir" != "/" ]]; do
        if [[ -f "$dir/pyproject.toml" || -d "$dir/.git" ]]; then
            echo "$dir"
            return 0
        fi
        dir="$(dirname "$dir")"
    done
    echo "❌ Error: Could not find project root"
    exit 1
}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
PROJECT_ROOT="$(find_project_root "$SCRIPT_DIR")"

echo "Setting up systemd services for Data Airflow Server..."
echo "  Project root: ${PROJECT_ROOT}"

# ------------------------------------------------------------------------------
# Load .env.prod
# ------------------------------------------------------------------------------
if [ -f "${PROJECT_ROOT}/.env.prod" ]; then
    set -a
    source "${PROJECT_ROOT}/.env.prod"
    set +a
else
    echo "❌ Error: .env.prod not found in ${PROJECT_ROOT}"
    exit 1
fi

echo "Copying systemd service files..."

SERVICE_SOURCE_DIR="${PROJECT_ROOT}/scripts/prod/system_services/systemd"

if compgen -G "${SERVICE_SOURCE_DIR}/*.service" > /dev/null; then
    sudo cp "${SERVICE_SOURCE_DIR}"/*.service /etc/systemd/system/
    sudo systemctl daemon-reload

    # Enable services to start on boot
    sudo systemctl enable airflow-api.service
    sudo systemctl enable airflow-scheduler.service
    sudo systemctl enable data_airflow_server.service 2>/dev/null || true

    echo "Services copied, enabled and daemon reloaded."
else
    echo "⚠️  No .service files found in ${SERVICE_SOURCE_DIR}"
fi

echo ""
echo "Setup completed."
echo "Run this to start services:"
echo "   ./scripts/prod/system_services/start_all_services.sh"