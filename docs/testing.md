# Testing Workflow

The test environment is fully isolated and always uses **SQLite mock** (never touches production data).

## Overview

- Environment file: `.env.test`
- Database: SQLite (auto-created in `airflow_home_test/`)
- Test runner: `scripts/test/run_tests.sh`
- All tests are written with in-memory data (no real files needed)

## How to run tests

```bash
# 1. Go to project root
cd /path/to/Data-Airflow-Server

# 2. Run the full test suite (recommended)
./scripts/test/run_tests.sh