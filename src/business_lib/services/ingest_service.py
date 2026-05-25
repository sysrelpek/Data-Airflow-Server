# =============================================================================
# src/business_lib/services/ingest_service.py
# IngestService - Clean hexagonal service (refactored from old feature_ingest.py)
# =============================================================================

from typing import Any


class IngestService:
    """
    Main business service for ingesting data.
    Receives a storage adapter via dependency injection (hexagonal style).
    """

    def __init__(self, storage_adapter: Any):
        self.storage_adapter = storage_adapter

    def ingest_data(self, data: list[dict], target_table: str) -> dict:
        """
        Ingest a list of records into the target table/storage.

        Args:
            data: List of dictionaries (in-memory test data or real records)
            target_table: Name of the target table/file

        Returns:
            Result dict with status and statistics
        """
        if not data:
            return {
                "status": "success",
                "rows_processed": 0,
                "target_table": target_table,
                "message": "No data to ingest"
            }

        try:
            # Delegate the actual write operation to the injected adapter
            self.storage_adapter.write(data, target_table)

            return {
                "status": "success",
                "rows_processed": len(data),
                "target_table": target_table,
                "message": f"Successfully ingested {len(data)} rows"
            }

        except Exception as e:
            return {
                "status": "error",
                "rows_processed": 0,
                "target_table": target_table,
                "message": f"Ingestion failed: {str(e)}"
            }