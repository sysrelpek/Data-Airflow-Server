from typing import Any, Dict, List


class TransformService:
    """
    Transform service for the example_ingest_pipeline.
    """

    def __init__(self, storage_adapter: Any = None):
        self.storage_adapter = storage_adapter

    def transform_data(self, data: List[dict] = None, **kwargs) -> Dict[str, Any]:
        print("Running TransformService.transform_data()...")

        if not data:
            data = []

        # Simple example transformation
        transformed = []
        for item in data:
            transformed_item = {
                **item,
                "transformed": True,
                "value_upper": str(item.get("value", "")).upper() if "value" in item else None
            }
            transformed.append(transformed_item)

        return {
            "status": "success",
            "transformed_count": len(transformed),
            "data": transformed
        }


# Module-level function that dag_factory.py calls
def transform_data(data: List[dict] = None, storage: Any = None, **kwargs) -> Dict[str, Any]:
    """
    Entry point called by the DAG factory.
    `storage` is injected automatically via the `inject` section in the manifest.
    """
    service = TransformService(storage_adapter=storage)
    return service.transform_data(data=data, **kwargs)