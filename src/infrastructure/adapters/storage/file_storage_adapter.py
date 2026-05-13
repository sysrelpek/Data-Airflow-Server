from pathlib import Path
import json
from datetime import datetime
from typing import List, Dict, Any, Optional

from src.business_lib.ports.storage_port import StoragePort
from src.business_lib.domain.models import DataRecord


class FileStorageAdapter(StoragePort):
    """File-based storage adapter for development and local testing.
    
    Fully implements the StoragePort interface.
    Uses JSONL files for simple, append-only storage.
    """

    def __init__(self, base_path: str = "tests/tmp_db"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        self.outbox_path = self.base_path / "outbox"
        self.outbox_path.mkdir(exist_ok=True)

    def save(self, entity_id: str, data: Dict[str, Any]) -> None:
        """Save data to a JSONL file named after the table/entity."""
        # For simplicity in dev, we'll use a single file per entity type
        # In real usage, entity_id might indicate the table
        file_path = self.base_path / "data.jsonl"
        record = {"id": entity_id, "data": data, "timestamp": datetime.now().isoformat()}
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")

    def get_by_id(self, entity_id: str) -> Optional[Dict[str, Any]]:
        """Get a record by ID from the data file."""
        file_path = self.base_path / "data.jsonl"
        if not file_path.exists():
            return None
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                record = json.loads(line)
                if record.get("id") == entity_id:
                    return record.get("data")
        return None

    def count_all(self) -> int:
        """Count all records in the storage."""
        file_path = self.base_path / "data.jsonl"
        if not file_path.exists():
            return 0
        count = 0
        with open(file_path, "r", encoding="utf-8") as f:
            for _ in f:
                count += 1
        return count

    def get_pending_messages(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get pending messages from outbox (dev mode uses file-based outbox)."""
        outbox_file = self.outbox_path / "outbox.jsonl"
        if not outbox_file.exists():
            return []
        messages = []
        with open(outbox_file, "r", encoding="utf-8") as f:
            for line in f:
                msg = json.loads(line)
                if msg.get("status", "PENDING") == "PENDING":
                    messages.append(msg)
                    if len(messages) >= limit:
                        break
        return messages

    def update_outbox_status(self, message_id: int, status: str) -> None:
        """Update outbox message status (dev mode: simple file update)."""
        outbox_file = self.outbox_path / "outbox.jsonl"
        if not outbox_file.exists():
            return
        
        # Read all messages
        messages = []
        with open(outbox_file, "r", encoding="utf-8") as f:
            for line in f:
                msg = json.loads(line)
                if msg.get("id") == message_id:
                    msg["status"] = status
                messages.append(msg)
        
        # Write back
        with open(outbox_file, "w", encoding="utf-8") as f:
            for msg in messages:
                f.write(json.dumps(msg) + "\n")

    def store_data(self, data: List[DataRecord], table_name: str) -> None:
        """Store a list of DataRecord objects (convenience method for tests)."""
        file_path = self.base_path / f"{table_name}.jsonl"
        with open(file_path, "a", encoding="utf-8") as f:
            for record in data:
                f.write(json.dumps(record.to_dict() if hasattr(record, 'to_dict') else record) + "\n")
        print(f"[DEV FileStorage] Stored {len(data)} records to {table_name}.jsonl")
