from typing import Any, Dict, List
import logging

logger = logging.getLogger(__name__)


class LoadService:
    """
    Loads transformed data into the storage adapter.
    """

    def __init__(self, storage: Any = None):
        self.storage = storage

    def load_to_warehouse(self, data: Any = None, **kwargs) -> Dict[str, Any]:
        try:
            if isinstance(data, dict) and "data" in data:
                data = data["data"]

            if not isinstance(data, list) or len(data) == 0:
                logger.warning("LoadService received no data to load.")
                return {
                    "status": "success",
                    "loaded_count": 0,
                    "message": "No data to load"
                }

            logger.info(f"Loading {len(data)} records into storage...")

            loaded_count = 0
            if self.storage:
                for item in data:
                    if isinstance(item, dict):
                        self.storage.insert_record(item)
                        loaded_count += 1
            else:
                logger.warning("No storage adapter provided. Data not persisted.")

            logger.info(f"Successfully loaded {loaded_count} records into storage")

            return {
                "status": "success",
                "loaded_count": loaded_count,
                "message": f"Successfully loaded {loaded_count} records"
            }

        except Exception as e:
            logger.error(f"Error during loading: {e}")
            return {
                "status": "error",
                "message": str(e),
                "loaded_count": 0
            }