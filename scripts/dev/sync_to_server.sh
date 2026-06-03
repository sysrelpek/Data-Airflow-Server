#!/usr/bin/env bash
# =============================================================================
# scripts/dev/sync_to_server.sh
# Sync project from local development machine to production server
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd -P)"

# Load development environment
if [ -f "${PROJECT_ROOT}/.env.dev" ]; then
    set -a
    source "${PROJECT_ROOT}/.env.dev"
    set +a
else
    echo "❌ Error: .env.dev not found!"
    exit 1
fi

# Server connection settings
SERVER_USER="${SERVER_USER:-etluser}"
SERVER_HOST="${SERVER_HOST:-192.168.1.218}"
SERVER_PORT="${SERVER_PORT:-22}"
REMOTE_BASE_DIR="${REMOTE_BASE_DIR:-/home/etluser/ai-projects}"
PROJECT_NAME="${PROJECT_NAME:-data_airflow_server}"
REMOTE_DIR="${REMOTE_BASE_DIR}/${PROJECT_NAME}"

echo "🔄 Syncing project to production server..."
echo "   Local  → ${PROJECT_ROOT}"
echo "   Remote → ${REMOTE_DIR}"

# Safety check for exclude file
if [ ! -f "${PROJECT_ROOT}/.rsync-exclude" ]; then
    echo "❌ Error: .rsync-exclude file not found in project root!"
    exit 1
fi

# Create remote directory if it doesn't exist
ssh -p "${SERVER_PORT}" "${SERVER_USER}@${SERVER_HOST}" "mkdir -p '${REMOTE_DIR}'"

# Perform rsync
# --ignore-times = always transfer files if content differs (more reliable)
# --prune-empty-dirs = helps reduce some "cannot delete" warnings
rsync -az --delete --prune-empty-dirs --ignore-times \
    -e "ssh -p ${SERVER_PORT}" \
    --exclude-from="${PROJECT_ROOT}/.rsync-exclude" \
    "${PROJECT_ROOT}/" \
    "${SERVER_USER}@${SERVER_HOST}:${REMOTE_DIR}/"

echo "✅ Files synced successfully."

# ------------------------------------------------------------
# Post-sync tasks on the server (made defensive)
# ------------------------------------------------------------
echo "🔧 Running post-sync tasks on server..."

ssh -p "${SERVER_PORT}" "${SERVER_USER}@${SERVER_HOST}" "
    set +e
    cd '${REMOTE_DIR}'

    # Set ENV=prod if .env.prod exists
    if [ -f .env.prod ]; then
        sed -i 's/^ENV=.*/ENV=prod/' .env.prod
        echo '   → Set ENV=prod in .env.prod'
    else
        echo '   ⚠️  .env.prod not found on server yet'
    fi

    # Make production scripts executable
    chmod +x scripts/prod/admin/*.sh scripts/prod/system_services/*.sh scripts/prod/install/*.sh 2>/dev/null || true
    echo '   → Made production scripts executable'

    # Install package in editable mode (required for build_dags.sh)
    if [ -f .venv/bin/activate ]; then
        source .venv/bin/activate
        echo '   → Virtual environment activated'

        if [ -f pyproject.toml ]; then
            pip install -e . --quiet
            echo '   → Package installed in editable mode'
        fi
    else
        echo '   ⚠️  Virtual environment not found on server'
    fi

    # Rebuild DAGs
    if [ -x ./scripts/prod/admin/build_dags.sh ]; then
        ./scripts/prod/admin/build_dags.sh
        echo '   → DAGs rebuilt'
    else
        echo '   ⚠️  build_dags.sh not found or not executable yet'
    fi

    echo '✅ Post-sync tasks completed on server.'
"