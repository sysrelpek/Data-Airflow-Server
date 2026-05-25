# =============================================================================
# tests/conftest.py
# Shared fixtures for ALL tests
# Forces SQLite mock environment (dev/test)
# =============================================================================

import os
from pathlib import Path

import pytest
from dotenv import load_dotenv

# ----------------------------------------------------------------------
# 1. Auto-load .env.test for every test session (SQLite mock)
# ----------------------------------------------------------------------
@pytest.fixture(scope="session", autouse=True)
def load_test_environment():
    """Automatically load .env.test at the start of every test run."""
    project_root = Path(__file__).parent.parent
    env_file = project_root / ".env.test"

    if env_file.exists():
        load_dotenv(env_file, override=True)
        print(f"✅ Test environment loaded → ENV={os.getenv('ENV')} (SQLite mock)")
        print(f"   AIRFLOW_HOME = {os.getenv('AIRFLOW_HOME')}")
    else:
        pytest.fail(f"❌ .env.test not found at {env_file}! "
                    "Tests must run with SQLite mock.")

# ----------------------------------------------------------------------
# 2. Project root fixture (very useful)
# ----------------------------------------------------------------------
@pytest.fixture(scope="session")
def project_root() -> Path:
    """Return the absolute path to the project root."""
    return Path(__file__).parent.parent


# ----------------------------------------------------------------------
# 3. Example business logic / adapter fixtures
#    (you can expand these as needed)
# ----------------------------------------------------------------------
@pytest.fixture
def storage_adapter():
    """Return a FileStorageAdapter (or your SQLite mock adapter)."""
    # Import here so we don't break if the module changes
    from business_lib.infrastructure.storage.file_adapter import FileStorageAdapter
    return FileStorageAdapter(base_path="tests/tmp_db")


# You can add more shared fixtures here later (e.g. manifest loader, DAG factory, etc.)

print("🧪 conftest.py loaded — all tests will use SQLite mock")