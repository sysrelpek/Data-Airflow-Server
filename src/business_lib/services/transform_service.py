from typing import Any, Dict, List
import logging

logger = logging.getLogger(__name__)


class TransformService:
    """
    Transforms data received from ExtractService.
    """

    def __init__(self, storage: Any = None):
        self.storage = storage  # kept for potential future use

    def transform_data(self, data: Any = None, **kwargs) -> Dict[str, Any]:
        try:
            if isinstance(data, dict) and "data" in data:
                data = data["data"]

            if not isinstance(data, list) or len(data) == 0:
                logger.warning("TransformService received no data to transform.")
                return {
                    "status": "success",
                    "transformed_count": 0,
                    "data": []
                }

            logger.info(f"Transforming {len(data)} records...")

            transformed_data = []
            for item in data:
                if isinstance(item, dict):
                    transformed_item = {
                        **item,
                        "transformed": True,
                        "value_upper": str(item.get("value", "")).upper()
                    }
                    transformed_data.append(transformed_item)

            logger.info(f"Successfully transformed {len(transformed_data)} records")

            return {
                "status": "success",
                "transformed_count": len(transformed_data),
                "data": transformed_data
            }

        except Exception as e:
            logger.error(f"Error during transformation: {e}")
            return {
                "status": "error",
                "message": str(e),
                "data": []
            }