#!/usr/bin/env bash
# =============================================================================
# scripts/dev/sync_to_server.sh
# Syncs the entire project from local (dev) to production server
# =============================================================================

set -euo pipefail

# Load development environment
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd -P)"

if [ -f "${PROJECT_ROOT}/.env.dev" ]; then
    set -a
    source "${PROJECT_ROOT}/.env.dev"
    set +a
else
    echo "❌ Error: .env.dev not found!"
    exit 1
fi

# Server connection settings (can be overridden in .env.dev)
SERVER_USER="${SERVER_USER:-etluser}"
SERVER_HOST="${SERVER_HOST:-192.168.1.218}"
SERVER_PORT="${SERVER_PORT:-22}"
REMOTE_BASE_DIR="${REMOTE_BASE_DIR:-/home/etluser/ai-projects}"
PROJECT_NAME="${PROJECT_NAME:-data_airflow_server}"
REMOTE_DIR="${REMOTE_BASE_DIR}/${PROJECT_NAME}"

echo "🔄 Syncing project to production server..."
echo "   Local  → ${PROJECT_ROOT}"
echo "   Remote → ${REMOTE_DIR}"
echo "   User   → ${SERVER_USER}@${SERVER_HOST}:${SERVER_PORT}"

# Ensure remote directory exists
ssh -p "${SERVER_PORT}" "${SERVER_USER}@${SERVER_HOST}" "mkdir -p '${REMOTE_DIR}'"

# Perform the sync
rsync -az --delete \
  -e "ssh -p ${SERVER_PORT}" \
  --exclude-from="${PROJECT_ROOT}/.rsync-exclude" \
  "${PROJECT_ROOT}/" \
  "${SERVER_USER}@${SERVER_HOST}:${REMOTE_DIR}/"

echo "✅ Files synced successfully."

# Set production environment on the server
echo "🔧 Setting ENV=prod on server..."
ssh -p "${SERVER_PORT}" "${SERVER_USER}@${SERVER_HOST}" "
    cd '${REMOTE_DIR}' &&
    sed -i 's/^ENV=.*/ENV=prod/' .env.prod 2>/dev/null || true
"

# Make production scripts executable
echo "🔨 Making production scripts executable..."
ssh -p "${SERVER_PORT}" "${SERVER_USER}@${SERVER_HOST}" "
    cd '${REMOTE_DIR}' &&
    chmod +x scripts/prod/admin/*.sh scripts/prod/system_services/*.sh 2>/dev/null || true
"

# Rebuild DAGs on the server
echo "🔨 Rebuilding DAGs on server..."
ssh -p "${SERVER_PORT}" "${SERVER_USER}@${SERVER_HOST}" "
    cd '${REMOTE_DIR}' &&
    ./scripts/prod/admin/build_dags.sh
"

echo "🎉 Sync completed successfully!"
echo "   Project is now live on the server."
echo "   DAGs have been rebuilt."