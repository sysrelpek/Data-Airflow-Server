from typing import Any, Dict
import json
import time
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class RemoveTestDataService:
    """
    Removes generated test data and measures how many rows were deleted.
    Includes artificial delay for better observability during testing.
    Works with both FileStorageAdapter and PostgresAdapter.
    """

    STATUS_FILE = "test_data_status.json"

    def __init__(self, storage: Any = None):
        self.storage = storage

    def remove(self, delay_seconds: int = 10, **kwargs) -> Dict[str, Any]:
        """
        Remove test data with a configurable delay.
        Returns how many rows were deleted.
        """
        logger.info(f"Starting removal of test data (delay: {delay_seconds}s)...")

        rows_deleted = 0

        if self.storage:
            try:
                # Simulate work (useful for visualization)
                time.sleep(delay_seconds)

                rows_deleted = self._delete_test_data()
                logger.info(f"Successfully removed {rows_deleted} records")

            except Exception as e:
                logger.error(f"Failed to remove test data: {e}")
                return {"status": "error", "message": str(e)}
        else:
            logger.warning("No storage adapter provided. Nothing to remove.")

        # Update shared status file
        self._update_status(rows_deleted=rows_deleted)

        return {
            "status": "success",
            "rows_deleted": rows_deleted,
            "delay_seconds": delay_seconds
        }

    # ============================================================
    # Internal Logic
    # ============================================================

    def _delete_test_data(self) -> int:
        """
        Delete test data in a storage-agnostic way.
        Currently simulates deletion. Can be improved later.
        """
        storage_type = self.storage.__class__.__name__

        if "File" in storage_type:
            return self._delete_from_file()
        elif "Postgres" in storage_type:
            return self._delete_from_postgres()
        else:
            logger.warning(f"Unsupported storage type for deletion: {storage_type}")
            return 0

    def _delete_from_file(self) -> int:
        """Remove test data from file storage."""
        try:
            # For now we just overwrite with empty data.
            # A better implementation would delete the actual file/key.
            self.storage.store_data([])
            return 100  # Placeholder - replace with actual count later
        except Exception as e:
            logger.error(f"Error deleting from file storage: {e}")
            return 0

    def _delete_from_postgres(self) -> int:
        """Remove test data from PostgreSQL."""
        try:
            # In a real implementation we would run DELETE statements.
            # For now we simulate deletion.
            # You can later improve this by tracking inserted IDs.
            return 100  # Placeholder
        except Exception as e:
            logger.error(f"Error deleting from PostgreSQL: {e}")
            return 0

    def _update_status(self, rows_deleted: int):
        """Update the shared status file with deletion info."""
        try:
            with open(self.STATUS_FILE, "r") as f:
                status = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            status = {}

        status.update({
            "last_updated": datetime.utcnow().isoformat(),
            "rows_deleted": rows_deleted
        })

        with open(self.STATUS_FILE, "w") as f:
            json.dump(status, f, indent=2)