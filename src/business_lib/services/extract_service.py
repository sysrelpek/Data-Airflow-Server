from typing import Any, Dict, List
import logging

logger = logging.getLogger(__name__)


class ExtractService:
    """
    Responsible for extracting data from a source.
    In a real implementation this could connect to APIs, databases, files, etc.
    """

    def __init__(self, storage: Any = None):
        self.storage = storage

    def extract_data(self, data: Any = None, **kwargs) -> Dict[str, Any]:
        """
        Extract data. Returns sample data if no input is provided.
        """
        try:
            if isinstance(data, dict) and "data" in data:
                data = data["data"]

            if not isinstance(data, list) or len(data) == 0:
                # Simulate extraction from an external source
                data = [
                    {"id": 1, "value": "raw_value_1"},
                    {"id": 2, "value": "raw_value_2"},
                    {"id": 3, "value": "raw_value_3"},
                ]
                logger.info("No input data received. Using simulated extracted data.")

            logger.info(f"Extracted {len(data)} records")

            return {
                "status": "success",
                "extracted_count": len(data),
                "data": data
            }

        except Exception as e:
            logger.exception("Error during data extraction")
            return {
                "status": "error",
                "message": str(e),
                "data": []
            }