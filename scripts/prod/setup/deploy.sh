#!/usr/bin/env bash
# =============================================================================
# scripts/prod/setup/deploy.sh
# SINGLE COMMAND to run after every sync_to_server.sh
# Official post-sync deployment step
# =============================================================================

set -euo pipefail

# Trap errors and show friendly message
trap 'echo "❌ Deployment failed at $(date "+%Y-%m-%d %H:%M:%S")"' ERR

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd -P)"

# Load production environment
if [ -f "${PROJECT_ROOT}/.env.prod" ]; then
    set -a
    source "${PROJECT_ROOT}/.env.prod"
    set +a
else
    echo "❌ Error: .env.prod not found in ${PROJECT_ROOT}!"
    exit 1
fi

echo "🚀 === DEPLOYMENT STARTED at $(date "+%Y-%m-%d %H:%M:%S") ==="
echo "   Project root: ${PROJECT_ROOT}"

# 1. Make all production scripts executable
echo "🔧 Making all production scripts executable..."
chmod +x "${PROJECT_ROOT}"/scripts/prod/admin/*.sh \
         "${PROJECT_ROOT}"/scripts/prod/setup/*.sh \
         "${PROJECT_ROOT}"/scripts/prod/system_services/*.sh \
         "${PROJECT_ROOT}"/scripts/prod/install/*.sh \
         "${PROJECT_ROOT}"/scripts/prod/install/tools/*.sh 2>/dev/null || true

# 2. Rebuild DAGs
echo "🔨 Rebuilding all DAGs from manifests..."
"${PROJECT_ROOT}/scripts/prod/admin/build_dags.sh"

# 3. Restart services
echo "🔄 Restarting Airflow services..."
"${PROJECT_ROOT}/scripts/prod/system_services/restart_server.sh"

# 4. Show status
echo "📊 Final status:"
"${PROJECT_ROOT}/scripts/prod/system_services/status_server.sh"

echo ""
echo "🎉 === DEPLOYMENT FINISHED SUCCESSFULLY at $(date "+%Y-%m-%d %H:%M:%S") ==="
echo "   You can now open the Airflow UI."