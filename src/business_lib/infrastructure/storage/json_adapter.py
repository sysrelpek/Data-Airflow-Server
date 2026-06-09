import json
import os
import uuid
from pathlib import Path
from typing import List, Dict, Any, Optional

from business_lib.domain.interfaces import StoragePort


class JsonAdapter(StoragePort):
    """
    JSON file-based storage.
    Path is controlled via FILE_STORAGE_PATH environment variable.
    """

    ENV_DEFAULT_PATH = "FILE_STORAGE_PATH"

    def __init__(
        self,
        base_path: Optional[str] = None,
        file_name: str = "data"
    ):
        if base_path:
            path = base_path
        else:
            path = os.getenv(self.ENV_DEFAULT_PATH)
            if not path:
                raise ValueError(
                    f"JsonAdapter requires a path. "
                    f"Set environment variable '{self.ENV_DEFAULT_PATH}' or pass base_path."
                )

        self.path = Path(path)
        self.path.mkdir(exist_ok=True)
        self.file_path = self.path / f"{file_name}.json"

    def insert_record(self, data: dict) -> None:
        if not isinstance(data, dict) or "id" not in data:
            raise ValueError("Data must contain an 'id' field")

        existing = {}
        if self.file_path.exists():
            existing = json.loads(self.file_path.read_text())

        # Convert UUID to string for JSON
        record = {k: str(v) if isinstance(v, uuid.UUID) else v for k, v in data.items()}
        existing[data["id"]] = record

        self.file_path.write_text(json.dumps(existing, indent=4))

    def insert_record_list(self, data: List[Dict[str, Any]]) -> None:
        for item in data:
            if isinstance(item, dict):
                self.insert_record(item)