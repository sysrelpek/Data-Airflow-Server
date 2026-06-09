from typing import Any, Dict
import time
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class RemoveTestDataService:
    """
    Removes test data created by GenerateTestDataService.
    Does NOT know anything about JsonAdapter, Postgres, or files.
    Only calls the generic delete_data() method on the storage.
    """

    def __init__(self, storage: Any = None):
        self.storage = storage

    def remove(self, delay_seconds: int = 10, **kwargs) -> Dict[str, Any]:
        logger.info(f"Starting removal of test data (delay: {delay_seconds}s)...")

        rows_deleted = 0

        if self.storage:
            try:
                time.sleep(delay_seconds)

                if hasattr(self.storage, "delete_data"):
                    rows_deleted = self.storage.delete_data()
                else:
                    logger.warning("Storage adapter does not support delete_data()")

                logger.info(f"Successfully removed {rows_deleted} records")

            except Exception as e:
                logger.error(f"Failed to remove test data: {e}")
                return {"status": "error", "message": str(e)}

        return {
            "status": "success",
            "rows_deleted": rows_deleted,
            "delay_seconds": delay_seconds
        }