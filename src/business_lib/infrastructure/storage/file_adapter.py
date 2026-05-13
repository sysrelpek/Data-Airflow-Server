import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from business_lib.domain.interfaces import StoragePort


class FileStorageAdapter(StoragePort):
    def __init__(self, base_path: str = "./local_db"):
        self.path = Path(base_path)
        self.path.mkdir(exist_ok=True)
        self.outbox_file = self.path / "outbox.jsonl"

    def save(self, entity_id: str, data: dict):
        # Spara tmp_db som JSON-fil
        file_path = self.path / f"{entity_id}.json"
        file_path.write_text(json.dumps(data, indent=4))

        # Simulera Outbox genom att lägga till en rad i en textfil
        with open(self.outbox_file, "a") as f:
            f.write(json.dumps({"id": entity_id, "tmp_db": data}) + "\n")

    def get_by_id(self, entity_id: str):
        file_path = self.path / f"{entity_id}.json"
        return json.loads(file_path.read_text()) if file_path.exists() else None

    def count_all(self) -> int:
        return len(list(self.path.glob("*.json")))

    def get_pending_messages(self, limit=50):
        # Enkel simulering: läser de sista raderna i outbox-filen
        if not self.outbox_file.exists(): return []
        return [{"id": "mock", "payload": "local_data"}]  # Förenklat för test

    def update_outbox_status(self, message_id: int, status: str) -> None:
        with open(self.outbox_file, "r") as f:
            lines = f.readlines()

        with open(self.outbox_file, "w") as f:
            for line in lines:
                message = json.loads(line)
                if message["id"] == message_id:
                    message["status"] = status
                f.write(json.dumps(message) + "\n")

            f.flush()
            f.seek(0)

            f.truncate()

        return None

    def store_data(self, data: Dict[str, Any]) -> None:
        """Saves data to the storage system."""
        file_path = self.path / f"{data['id']}.json"
        file_path.write_text(json.dumps(data, indent=4))




