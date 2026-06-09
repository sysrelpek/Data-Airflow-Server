from typing import Any, Dict, List
import logging

logger = logging.getLogger(__name__)


class LoadService:
    """
    Loads transformed data into storage using the new StoragePort interface.
    """

    def __init__(self, storage: Any = None):
        self.storage = storage

    def load_to_warehouse(self, data: Any = None, **kwargs) -> Dict[str, Any]:
        try:
            if isinstance(data, dict) and "data" in data:
                data = data["data"]

            if not isinstance(data, list):
                data = []

            loaded_count = 0

            if self.storage:
                for item in data:
                    if isinstance(item, dict):
                        # No more entity_id — just pass the full dict
                        self.storage.insert_record(item)
                        loaded_count += 1
            else:
                logger.warning("No storage adapter provided. Data not persisted.")

            logger.info(f"Loaded {loaded_count} records into storage")

            return {
                "status": "success",
                "loaded_count": loaded_count,
                "message": f"Successfully loaded {loaded_count} records"
            }

        except Exception as e:
            logger.error(f"Error in load_to_warehouse: {e}")
            return {
                "status": "error",
                "message": str(e),
                "loaded_count": 0
            }