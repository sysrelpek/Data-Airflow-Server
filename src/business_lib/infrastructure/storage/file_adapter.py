import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from business_lib.domain.interfaces import StoragePort


class FileStorageAdapter(StoragePort):
    def __init__(self, base_path: str = "./local_db"):
        self.path = Path(base_path)
        self.path.mkdir(exist_ok=True)
        self.outbox_file = self.path / "outbox.json"

    def write(self, data: List[Dict[str, Any]], target_table: str) -> None:
        """Main method used by IngestService (added for test compatibility)."""
        if not data:
            return
        # For now we store each item individually (you can improve later)
        for item in data:
            self.store_data(item)

    def save(self, entity_id: str, data: dict):
        file_path = self.path / f"{entity_id}.json"
        file_path.write_text(json.dumps(data, indent=4))
        with open(self.outbox_file, "a") as f:
            f.write(json.dumps({"id": entity_id, "tmp_db": data}) + "\n")

    def get_by_id(self, entity_id: str):
        file_path = self.path / f"{entity_id}.json"
        return json.loads(file_path.read_text()) if file_path.exists() else None

    def count_all(self) -> int:
        return len(list(self.path.glob("*.json")))

    def get_pending_messages(self, limit=50):
        if not self.outbox_file.exists():
            return []
        return [{"id": "mock", "payload": "local_data"}]

    def update_outbox_status(self, message_id: int, status: str) -> None:
        if not self.outbox_file.exists():
            return
        with open(self.outbox_file, "r") as f:
            lines = f.readlines()
        with open(self.outbox_file, "w") as f:
            for line in lines:
                message = json.loads(line)
                if message.get("id") == message_id:
                    message["status"] = status
                f.write(json.dumps(message) + "\n")
            f.flush()

    def store_data(self, data: Dict[str, Any]) -> None:
        """Saves data to the storage system."""
        file_path = self.path / f"{data.get('id', 'unknown')}.json"
        file_path.write_text(json.dumps(data, indent=4))