from typing import Any, Dict
import logging

logger = logging.getLogger(__name__)


class ExtractService:
    """
    Strict Extract Service.
    Only processes data received via XCom.
    If no valid data is received → logs error and fails.
    """

    def __init__(self, storage: Any = None):
        self.storage = storage   # kept for future use if needed, but not used for reading here

    def extract_data(self, data: Any = None, **kwargs) -> Dict[str, Any]:
        try:
            # Only accept real record data passed via XCom
            if data and isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
                logger.info(f"Received {len(data)} records via XCom")
                return {
                    "status": "success",
                    "extracted_count": len(data),
                    "data": data
                }

            # No valid data received → fail
            logger.error("ExtractService received no valid data via XCom. Task cannot continue.")
            return {
                "status": "error",
                "message": "No input data received via XCom",
                "data": []
            }

        except Exception as e:
            logger.error(f"Error in extract_data: {e}")
            return {
                "status": "error",
                "message": str(e),
                "data": []
            }