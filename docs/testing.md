# Testing

This document describes how testing is set up and how to run tests in the Data Airflow Server project.


## Overview

- All tests run against a **SQLite mock database** (never against production data).
- Tests are located in the `tests/` directory.
- The test runner script is: `./scripts/test/run_tests.sh`
- We use **pytest** with coverage reporting.

---

## Running Tests

### Run the full test suite

```bash
./scripts/test/run_tests.sh
```
This script:

Activates the virtual environment
Loads the test environment (.env.test)
Runs pytest with coverage enabled
Generates both terminal and HTML coverage reports

Run specific tests
```
# Run all tests in a specific file
python -m pytest tests/test_factory.py -v

# Run a specific test function
python -m pytest tests/test_factory.py::test_create_dag_from_simple_manifest -v

# Run tests matching a keyword
python -m pytest -k "ingest" -v
```

### Test Configuration

- Environment file: .env.test
- Database: SQLite (in-memory or file-based in airflow_home_test/)
- Coverage: Enabled via pytest-cov
- Configuration: Defined in pyproject.toml under [tool.pytest.ini_options]

### Test Structure
```
tests/
├── conftest.py              # Shared fixtures (SQLite mock, etc.)
├── test_factory.py          # Tests for dag_factory and manifest handling
└── test_ingest_pipeline.py  # Tests for ingest/transform/load services
```

### Key Fixtures (in conftest.py)

- mock_sqlite_db: Provides an isolated SQLite database for each test
- Automatic mocking of storage adapters when needed
---
## Coverage Reports
After running tests, coverage reports are generated in two formats:

```
Format      Location            Description
---------------------------------------------------------------
Terminal    Console output,     Quick overview during CI/dev
HTML        htmlcov/index.html  Detailed interactive report
```

Open the HTML report with:
```
open htmlcov/index.html        # macOS
xdg-open htmlcov/index.html    # Linux
```
---

## Writing Tests
When writing new tests:

1. Place them in the tests/ folder
2. Use fixtures from conftest.py when possible
3. Prefer the SQLite mock over real databases
4. Keep tests fast and isolated

Example structure:
```
def test_something(mock_sqlite_db):
    # test logic here
    assert result == expected
```
---
## Continuous Integration
Tests are expected to pass with:

- Minimum coverage threshold (defined in pyproject.toml)
- All tests using the SQLite mock
- No external dependencies (except what's in requirements-test.txt)
---
## Troubleshooting
```
Problem                             Possible Solution
--------------------------------------------------------------------------------------------
Tests fail with database errors     Make sure you're using the SQLite mock from conftest.py
Coverage not updating               Delete htmlcov/ and .coverage then re-run tests
Import errors                       Ensure pip install -e . was run
Environment not loaded              Check that .env.test exists and is being sourced
```

Tip: Always run ./scripts/test/run_tests.sh before pushing changes to ensure everything still works with the SQLite mock.