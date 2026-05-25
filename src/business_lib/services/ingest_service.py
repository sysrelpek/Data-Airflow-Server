# =============================================================================
# src/business_lib/services/ingest_service.py
# IngestService - Clean hexagonal service (refactored from old feature_ingest.py)
# =============================================================================

import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class IngestService:
    """
    Main business service responsible for ingesting data.

    This is a pure hexagonal service:
    - It receives its storage adapter via dependency injection.
    - It contains only business logic, no infrastructure details.
    """

    def __init__(self, storage_adapter: Any):
        """
        Args:
            storage_adapter: Any adapter that implements .write(data, target_table)
        """
        self.storage_adapter = storage_adapter

    def ingest_data(self, data: List[dict], target_table: str) -> Dict[str, Any]:
        """
        Ingest a list of records into the target storage.

        Args:
            data: List of dictionaries to be ingested (in-memory test data or real records)
            target_table: Name of the target table / file / collection

        Returns:
            Dict with status, statistics and message
        """
        if not data:
            logger.info("No data to ingest for table '%s'", target_table)
            return {
                "status": "success",
                "rows_processed": 0,
                "target_table": target_table,
                "message": "No data to ingest"
            }

        try:
            logger.debug("Ingesting %d rows into '%s'", len(data), target_table)

            # Delegate the actual storage operation to the injected adapter
            self.storage_adapter.write(data, target_table)

            logger.info("Successfully ingested %d rows into '%s'", len(data), target_table)

            return {
                "status": "success",
                "rows_processed": len(data),
                "target_table": target_table,
                "message": f"Successfully ingested {len(data)} rows"
            }

        except Exception as e:  # pylint: disable=broad-except
            logger.error("Ingestion failed for table '%s': %s", target_table, e)
            return {
                "status": "error",
                "rows_processed": 0,
                "target_table": target_table,
                "message": f"Ingestion failed: {str(e)}"
            }