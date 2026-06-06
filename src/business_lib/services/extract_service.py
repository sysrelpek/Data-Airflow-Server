from typing import Any, Dict, List


class ExtractService:
    def __init__(self, storage_adapter: Any = None):
        self.storage_adapter = storage_adapter

    def extract_data(self, data: List[dict] = None, **kwargs) -> Dict[str, Any]:
        print("Running ExtractService.extract_data()...")

        extracted_data = data or [{"id": 1, "value": "example"}]

        return {
            "status": "success",
            "extracted_count": len(extracted_data),
            "data": extracted_data
        }


# This is what dag_factory.py is actually looking for
def extract_data(data: List[dict] = None, **kwargs) -> Dict[str, Any]:
    """Module-level function that dag_factory calls."""
    service = ExtractService()
    return service.extract_data(data=data, **kwargs)