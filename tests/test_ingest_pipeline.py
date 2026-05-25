# =============================================================================
# tests/test_ingest_pipeline.py
# Tests for the ingest business logic (in-memory data)
# =============================================================================

import pytest
from business_lib.services.ingest_service import IngestService


def test_ingest_service_with_in_memory_data(storage_adapter):
    """Test full ingest pipeline with simple in-memory test data."""
    test_data = [
        {"id": 1, "name": "Alice", "value": 100},
        {"id": 2, "name": "Bob",   "value": 200},
        {"id": 3, "name": "Carol", "value": 300},
    ]

    service = IngestService(storage_adapter=storage_adapter)

    result = service.ingest_data(
        data=test_data,
        target_table="test_ingest_table"
    )

    assert result["status"] == "success"
    assert result["rows_processed"] == 3
    assert result["target_table"] == "test_ingest_table"


def test_ingest_service_empty_data(storage_adapter):
    """Test graceful handling of empty input."""
    service = IngestService(storage_adapter=storage_adapter)

    result = service.ingest_data(
        data=[],
        target_table="empty_table"
    )

    assert result["status"] == "success"
    assert result["rows_processed"] == 0