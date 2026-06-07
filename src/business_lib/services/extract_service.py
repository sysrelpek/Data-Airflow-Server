from typing import Any, Dict, List
import logging

logger = logging.getLogger(__name__)


class ExtractService:
    """
    Service responsible for extracting data in the example pipeline.
    """

    def __init__(self, storage_adapter: Any = None):
        self.storage_adapter = storage_adapter

    def extract_data(self, data: Any = None, **kwargs) -> Dict[str, Any]:
        """
        Extract data. If no data is provided, returns sample data.
        """
        try:
            if isinstance(data, dict):
                data = data.get("data", data)

            if not isinstance(data, list) or len(data) == 0:
                # Return sample data if nothing was provided
                data = [
                    {"id": 1, "value": "example_1"},
                    {"id": 2, "value": "example_2"},
                ]
                logger.info("No input data provided. Using sample data.")

            logger.info(f"Extracted {len(data)} records")

            return {
                "status": "success",
                "extracted_count": len(data),
                "data": data
            }

        except Exception as e:
            logger.error(f"Error in extract_data: {e}")
            return {
                "status": "error",
                "message": str(e),
                "data": []
            }