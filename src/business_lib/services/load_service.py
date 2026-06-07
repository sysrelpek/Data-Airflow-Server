from typing import Any, Dict, List
import logging

logger = logging.getLogger(__name__)


class LoadService:
    """
    Responsible for loading transformed data into the target system (warehouse/storage).
    """

    def __init__(self, storage: Any = None):
        self.storage = storage

    def load_to_warehouse(self, data: Any = None, **kwargs) -> Dict[str, Any]:
        """
        Persist data using the injected storage adapter.
        """
        try:
            if isinstance(data, dict) and "data" in data:
                data = data["data"]

            if not isinstance(data, list):
                data = []

            loaded_count = 0

            if self.storage:
                for item in data:
                    if isinstance(item, dict):
                        entity_id = str(item.get("id", hash(str(item))))
                        self.storage.save(entity_id, item)
                        loaded_count += 1
            else:
                logger.warning("No storage adapter was injected. Data will not be persisted.")

            logger.info(f"Loaded {loaded_count} records into storage")

            return {
                "status": "success",
                "loaded_count": loaded_count,
                "message": f"Successfully loaded {loaded_count} records"
            }

        except Exception as e:
            logger.exception("Error during data loading")
            return {
                "status": "error",
                "message": str(e),
                "loaded_count": 0
            }