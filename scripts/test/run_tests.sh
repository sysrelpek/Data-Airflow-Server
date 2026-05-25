#!/usr/bin/env bash
# =============================================================================
# scripts/test/run_tests.sh
# Main test runner - always uses SQLite mock
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd -P)"

# Load test environment (forces SQLite mock)
if [ -f "${PROJECT_ROOT}/.env.test" ]; then
    set -a
    source "${PROJECT_ROOT}/.env.test"
    set +a
else
    echo "❌ Error: .env.test not found!"
    exit 1
fi

echo "🧪 === Starting tests with SQLite mock ==="
echo "   Environment : ${ENV}"
echo "   Airflow home: ${AIRFLOW_HOME}"

# Activate virtual environment
if [ -f "${PROJECT_ROOT}/.venv/bin/activate" ]; then
    source "${PROJECT_ROOT}/.venv/bin/activate"
else
    echo "❌ Error: Virtual environment not found. Run setup first."
    exit 1
fi

# Run pytest
echo "Running pytest..."
python -m pytest tests/ \
    --verbose \
    --cov=src/business_lib \
    --cov-report=term-missing \
    --cov-report=html:htmlcov

echo ""
echo "🎉 === All tests completed successfully with SQLite mock ==="
echo "   Coverage report: htmlcov/index.html"