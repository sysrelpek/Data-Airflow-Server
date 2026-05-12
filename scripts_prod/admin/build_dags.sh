#!/usr/bin/env bash
# =============================================================================
# build_dags.sh - Build real Airflow DAG files from pipelines/
# =============================================================================

set -euo pipefail

echo "🔨 Building Airflow DAGs from pipelines..."

# === Activate virtual environment ===
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
    echo "✅ Virtual environment activated"
else
    echo "❌ Error: .venv not found. Please run from project root."
    exit 1
fi

# === Clean old generated DAGs ===
rm -f dags/ml/*.py 2>/dev/null || true

# === Run the factory ===
python -m dags.factory

echo "✅ All DAGs generated successfully in dags/ml/"
echo ""
echo "Next step: Restart Airflow so it picks up the new DAGs:"
echo "   ./restart_airflow_service.sh"