from typing import Any, Dict, List
import logging

logger = logging.getLogger(__name__)


class LoadService:
    """
    Service responsible for loading data into storage/warehouse.
    """

    def __init__(self, storage: Any = None):
        self.storage = storage


    def load_to_warehouse(self, data: Any = None, **kwargs) -> Dict[str, Any]:
        """
        Load data into storage using the injected storage adapter.
        """
        print(f"DEBUG - type of data received: {type(data)}, value preview: {str(data)[:300]}")
        try:
            # Robust data extraction from previous task result
            if isinstance(data, dict):
                if "data" in data:
                    data = data["data"]
                else:
                    data = []

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
                logger.warning("No storage adapter provided. Data not persisted.")

            logger.info(f"Loaded records to storage: {loaded_count}")

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