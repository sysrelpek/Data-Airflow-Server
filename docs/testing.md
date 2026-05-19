# Testing Workflow

## Overview

The test environment uses **SQLite (mock)** and is completely isolated from production.

- Environment file: `.env.test`
- Database: SQLite (auto-created in `airflow_home_test/`)
- Purpose: Run unit tests, integration tests, and manifest validation without touching real data.

## Current State (May 2026)

The test setup is minimal but ready for expansion:
- Only `scripts/test/build_manifest.py` exists (legacy script for manifest validation).
- Full pytest suite and CI will be added in the next phase.

## How to run tests (today)

```bash
# 1. Go to project root
cd /path/to/Data-Airflow-Server

# 2. Activate virtual environment
source .venv/bin/activate

# 3. Load test environment
set -a
source .env.test
set +a

# 4. Run current test script
python scripts/test/build_manifest.py

# 5. (Future) Run full test suite when ready
# ./scripts/test/run_tests.sh