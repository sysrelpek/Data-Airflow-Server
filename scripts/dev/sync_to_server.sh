#!/usr/bin/env bash
# =============================================================================
# scripts/dev/sync_to_server.sh
# Syncs the project from local development machine to production server
# =============================================================================

set -euo pipefail

# ------------------------------------------------------------------------------
# 1. Calculate paths
# ------------------------------------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd -P)"

# ------------------------------------------------------------------------------
# 2. Load development environment
# ------------------------------------------------------------------------------
if [ -f "${PROJECT_ROOT}/.env.dev" ]; then
    set -a
    source "${PROJECT_ROOT}/.env.dev"
    set +a
else
    echo "❌ Error: .env.dev not found in project root!"
    exit 1
fi

# ------------------------------------------------------------------------------
# 3. Server connection settings (can be overridden in .env.dev)
# ------------------------------------------------------------------------------
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

# ------------------------------------------------------------------------------
# 4. Safety check: .rsync-exclude must exist
# ------------------------------------------------------------------------------
if [ ! -f "${PROJECT_ROOT}/.rsync-exclude" ]; then
    echo "❌ Error: .rsync-exclude file not found in project root!"
    echo "   Please create it or move it to: ${PROJECT_ROOT}/.rsync-exclude"
    exit 1
fi

# ------------------------------------------------------------------------------
# 5. Ensure remote directory exists
# ------------------------------------------------------------------------------
ssh -p "${SERVER_PORT}" "${SERVER_USER}@${SERVER_HOST}" "mkdir -p '${REMOTE_DIR}'"

# ------------------------------------------------------------------------------
# 6. Perform rsync
#    - Delete files on server that no longer exist locally
#    - Respect .rsync-exclude (protected files/folders on server will not be deleted)
# ------------------------------------------------------------------------------
rsync -az --delete \
    -e "ssh -p ${SERVER_PORT}" \
    --exclude-from="${PROJECT_ROOT}/.rsync-exclude" \
    "${PROJECT_ROOT}/" \
    "${SERVER_USER}@${SERVER_HOST}:${REMOTE_DIR}/"

echo "✅ Files synced successfully."

# ------------------------------------------------------------------------------
# 7. Set ENV=prod on the server (only if .env.prod exists)
# ------------------------------------------------------------------------------
echo "🔧 Setting ENV=prod on server..."
ssh -p "${SERVER_PORT}" "${SERVER_USER}@${SERVER_HOST}" "
    cd '${REMOTE_DIR}' 2>/dev/null || exit 0
    if [ -f .env.prod ]; then
        sed -i 's/^ENV=.*/ENV=prod/' .env.prod
    else
        echo '⚠️  .env.prod not found on server (first time setup?)'
    fi
"

# ------------------------------------------------------------------------------
# 8. Make production scripts executable on the server
# ------------------------------------------------------------------------------
echo "🔨 Making production scripts executable..."
ssh -p "${SERVER_PORT}" "${SERVER_USER}@${SERVER_HOST}" "
    cd '${REMOTE_DIR}' 2>/dev/null || exit 0
    chmod +x scripts/prod/admin/*.sh scripts/prod/system_services/*.sh 2>/dev/null || true
"

# ------------------------------------------------------------------------------
# 9. Rebuild DAGs on the server
# ------------------------------------------------------------------------------
echo "🔨 Rebuilding DAGs on server..."
ssh -p "${SERVER_PORT}" "${SERVER_USER}@${SERVER_HOST}" "
    cd '${REMOTE_DIR}' 2>/dev/null || exit 0
    if [ -x ./scripts/prod/admin/build_dags.sh ]; then
        ./scripts/prod/admin/build_dags.sh
    else
        echo '⚠️  build_dags.sh not found or not executable on server'
    fi
"

echo ""
echo "🎉 Sync completed successfully!"
echo "   Project is now live on the server."