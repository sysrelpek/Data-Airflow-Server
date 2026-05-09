#!/usr/bin/env bash
# =============================================================================
# sync_to_server.sh - Sync local project to production server (fixed)
# =============================================================================

set -euo pipefail

# --- Configuration ---
SERVER_USER="etluser"
SERVER_HOST="192.168.1.218"
SERVER_PORT="22"

REMOTE_BASE_DIR="/home/etluser/ai-projects"
PROJECT_NAME="data_airflow_server"
REMOTE_DIR="${REMOTE_BASE_DIR}/${PROJECT_NAME}"

# Robust way to get local project directory (no trailing spaces)
LOCAL_PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"

echo "🔄 Syncing project to server..."
echo "   Local  → ${LOCAL_PROJECT_DIR}"
echo "   Remote → ${REMOTE_DIR}"

# Create remote directory
ssh -p "${SERVER_PORT}" "${SERVER_USER}@${SERVER_HOST}" "mkdir -p '${REMOTE_DIR}'"

# Rsync with clean exclusions
rsync -az --delete \
  -e "ssh -p ${SERVER_PORT}" \
  --exclude '.git' \
  --exclude '.venv' \
  --exclude '__pycache__' \
  --exclude '.idea' \
  --exclude '.pytest_cache' \
  --exclude 'logs/' \
  --exclude 'reporting/' \
  --exclude 'models/' \
  --exclude 'app/providers/cache' \
  --exclude '*.log' \
  "${LOCAL_PROJECT_DIR}/" \
  "${SERVER_USER}@${SERVER_HOST}:${REMOTE_DIR}/"

# Make important scripts executable on server
ssh -p "${SERVER_PORT}" "${SERVER_USER}@${SERVER_HOST}" "
  cd '${REMOTE_DIR}' &&
  chmod +x build_dags.sh run_airflow_service.sh restart_airflow_service.sh 2>/dev/null || true
"

# Rebuild DAGs on the server
echo "🔨 Rebuilding DAGs on server..."
ssh -p "${SERVER_PORT}" "${SERVER_USER}@${SERVER_HOST}" "
  cd '${REMOTE_DIR}' &&
  ./build_dags.sh
"

echo "🎉 Sync completed successfully!"
echo "   Remote path: ${REMOTE_DIR}"
echo "   DAGs have been rebuilt on the server."