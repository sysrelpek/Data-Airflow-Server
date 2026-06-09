from typing import Any, Dict, List
import random
import uuid
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class GenerateTestDataService:
    """
    Generates test data based on schema from YAML.
    - Requires schema (no default)
    - id can only be: int or uuid
    """

    def __init__(self, storage: Any = None):
        self.storage = storage

    def generate(self, rows: int = 100, schema: Dict[str, str] = None, **kwargs) -> Dict[str, Any]:
        if not schema:
            logger.error("No schema provided in generate_test_data. Skipping data generation.")
            return {"status": "error", "message": "Schema is required"}

        if rows <= 0:
            rows = 100

        logger.info(f"Generating {rows} test records...")

        generated_data = self._generate_data(rows, schema)

        if self.storage:
            try:
                self.storage.insert_record_list(generated_data)
                logger.info(f"Inserted {len(generated_data)} records")
            except Exception as e:
                logger.error(f"Failed to insert data: {e}")
                return {"status": "error", "message": str(e)}

        return {
            "status": "success",
            "rows_created": len(generated_data),
            "schema": schema
        }

    def _generate_data(self, rows: int, schema: Dict[str, str]) -> List[Dict[str, Any]]:
        data = []

        for i in range(rows):
            record = {}
            for column, dtype in schema.items():
                record[column] = self._generate_value(column, dtype, i)
            data.append(record)

        return data

    def _generate_value(self, column: str, dtype: str, index: int) -> Any:
        dtype = dtype.lower()

        # Special handling for 'id' column
        if column == "id":
            if dtype == "uuid":
                return str(uuid.uuid4())
            else:
                # Default to integer if not uuid
                return random.randint(1, 1_000_000)

        # Normal types
        if dtype == "integer":
            return random.randint(1, 1_000_000)
        elif dtype == "float":
            return round(random.uniform(0, 100000), 2)
        elif dtype == "string":
            return f"test_record_{index}"
        elif dtype == "boolean":
            return random.choice([True, False])
        elif dtype in ("timestamp", "datetime"):
            base = datetime(2025, 1, 1)
            return (base + timedelta(days=random.randint(0, 730))).isoformat()
        else:
            return f"unknown_type_{dtype}_{index}"