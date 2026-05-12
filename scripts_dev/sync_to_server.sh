#!/usr/bin/env bash
# =============================================================================
# scripts_dev/sync_to_server.sh
# =============================================================================

set -euo pipefail

SERVER_USER="etluser"
SERVER_HOST="192.168.1.218"
SERVER_PORT="22"

REMOTE_BASE_DIR="/home/etluser/ai-projects"
PROJECT_NAME="data_airflow_server"
REMOTE_DIR="${REMOTE_BASE_DIR}/${PROJECT_NAME}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
LOCAL_PROJECT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd -P)"

echo "🔄 Syncing project to server..."
echo "   Local  → ${LOCAL_PROJECT_DIR}"
echo "   Remote → ${REMOTE_DIR}"

ssh -p "${SERVER_PORT}" "${SERVER_USER}@${SERVER_HOST}" "mkdir -p '${REMOTE_DIR}'"

rsync -az --delete \
  -e "ssh -p ${SERVER_PORT}" \
  --exclude-from="${SCRIPT_DIR}/.rsync-exclude" \
  "${LOCAL_PROJECT_DIR}/" \
  "${SERVER_USER}@${SERVER_HOST}:${REMOTE_DIR}/"

# Switch to production environment on server
echo "🔧 Setting ENV=prod on server..."
ssh -p "${SERVER_PORT}" "${SERVER_USER}@${SERVER_HOST}" "
  cd '${REMOTE_DIR}' &&
  sed -i 's/^ENV=.*/ENV=prod/' .env
"

# Make scripts executable
ssh -p "${SERVER_PORT}" "${SERVER_USER}@${SERVER_HOST}" "
  cd '${REMOTE_DIR}' &&
  chmod +x build_dags.sh run_airflow_service.sh restart_airflow_service.sh 2>/dev/null || true
"

# Rebuild DAGs
echo "🔨 Rebuilding DAGs on server..."
ssh -p "${SERVER_PORT}" "${SERVER_USER}@${SERVER_HOST}" "
  cd '${REMOTE_DIR}' &&
  ./build_dags.sh
"

echo "🎉 Sync completed successfully!"
echo "   ENV set to 'prod' on server"