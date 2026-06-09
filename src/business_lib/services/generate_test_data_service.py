from typing import Any, Dict, List
import random
from datetime import datetime, timedelta
import json
import time
import logging

logger = logging.getLogger(__name__)


class GenerateTestDataService:
    """
    Generates test data and tracks how many rows were created.
    Updates a status file and pushes metrics via XCom.
    """

    STATUS_FILE = "test_data_status.json"

    def __init__(self, storage: Any = None):
        self.storage = storage

    def generate(self, rows: int = 100, schema: Dict[str, str] = None, **kwargs) -> Dict[str, Any]:
        if not schema:
            schema = {"id": "integer", "value": "string"}

        if rows <= 0:
            rows = 100

        logger.info(f"Generating {rows} test records...")

        generated_data = self._generate_data(rows, schema)

        rows_created = 0
        if self.storage:
            try:
                self.storage.store_data(generated_data)
                rows_created = len(generated_data)
                logger.info(f"Successfully created {rows_created} records")
            except Exception as e:
                logger.error(f"Failed to store test data: {e}")
                return {"status": "error", "message": str(e)}

        # Update status file + push to XCom
        self._update_status(rows_created=rows_created)
        self._push_xcom(rows_created=rows_created)

        return {
            "status": "success",
            "rows_created": rows_created,
            "schema": schema
        }

    def _generate_data(self, rows: int, schema: Dict[str, str]) -> List[Dict[str, Any]]:
        data = []
        for i in range(rows):
            record = {}
            for column, dtype in schema.items():
                record[column] = self._generate_value(dtype, i)
            data.append(record)
        return data

    def _generate_value(self, dtype: str, index: int) -> Any:
        dtype = dtype.lower()
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
            return f"unknown_{dtype}_{index}"

    def _update_status(self, rows_created: int):
        status = {
            "last_updated": datetime.utcnow().isoformat(),
            "rows_created": rows_created,
            "rows_deleted": 0
        }
        with open(self.STATUS_FILE, "w") as f:
            json.dump(status, f, indent=2)

    def _push_xcom(self, rows_created: int):
        # This will be used by task_wrapper via context
        pass  # XCom is pushed from task_wrapper in current design