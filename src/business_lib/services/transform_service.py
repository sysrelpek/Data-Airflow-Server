from typing import Any, Dict, List
import logging

logger = logging.getLogger(__name__)


class TransformService:
    """
    Service responsible for transforming data in the example pipeline.
    """

    def __init__(self, storage_adapter: Any = None):
        self.storage_adapter = storage_adapter

    def transform_data(self, data: Any = None, **kwargs) -> Dict[str, Any]:
        """
        Transform incoming data. Adds a 'transformed' flag and uppercases 'value'.
        """
        try:
            if isinstance(data, dict):
                data = data.get("data", data)

            if not isinstance(data, list):
                data = []

            transformed = []
            for item in data:
                if isinstance(item, dict):
                    transformed_item = {
                        **item,
                        "transformed": True,
                        "value_upper": str(item.get("value", "")).upper()
                    }
                    transformed.append(transformed_item)
                else:
                    transformed.append({"original": item, "transformed": True})

            logger.info(f"Transformed {len(transformed)} records")

            return {
                "status": "success",
                "transformed_count": len(transformed),
                "data": transformed
            }

        except Exception as e:
            logger.error(f"Error in transform_data: {e}")
            return {
                "status": "error",
                "message": str(e),
                "data": []
            }