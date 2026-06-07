from typing import Any, Dict, List
import logging

logger = logging.getLogger(__name__)


class TransformService:
    """
    Responsible for transforming/cleaning/enriching data.
    """

    def __init__(self, storage: Any = None):
        self.storage = storage

    def transform_data(self, data: Any = None, **kwargs) -> Dict[str, Any]:
        """
        Transform the data: add flags, normalize values, filter invalid records.
        """
        try:
            if isinstance(data, dict) and "data" in data:
                data = data["data"]

            if not isinstance(data, list):
                data = []

            transformed = []
            for item in data:
                if not isinstance(item, dict):
                    continue

                transformed_item = {
                    **item,
                    "transformed": True,
                    "value_upper": str(item.get("value", "")).upper(),
                    "processed_at": "2026-06-07T19:00:00Z"  # example enrichment
                }
                transformed.append(transformed_item)

            logger.info(f"Transformed {len(transformed)} records")

            return {
                "status": "success",
                "transformed_count": len(transformed),
                "data": transformed
            }

        except Exception as e:
            logger.exception("Error during data transformation")
            return {
                "status": "error",
                "message": str(e),
                "data": []
            }