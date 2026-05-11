import json
from pathlib import Path
from business_lib.domain.interfaces import StoragePort


class FileStorageAdapter(StoragePort):
    def __init__(self, base_path: str = "./local_db"):
        self.path = Path(base_path)
        self.path.mkdir(exist_ok=True)
        self.outbox_file = self.path / "outbox.jsonl"

    def save(self, entity_id: str, data: dict):
        # Spara data som JSON-fil
        file_path = self.path / f"{entity_id}.json"
        file_path.write_text(json.dumps(data, indent=4))

        # Simulera Outbox genom att lägga till en rad i en textfil
        with open(self.outbox_file, "a") as f:
            f.write(json.dumps({"id": entity_id, "data": data}) + "\n")

    def get_by_id(self, entity_id: str):
        file_path = self.path / f"{entity_id}.json"
        return json.loads(file_path.read_text()) if file_path.exists() else None

    def get_pending_messages(self, limit=50):
        # Enkel simulering: läser de sista raderna i outbox-filen
        if not self.outbox_file.exists(): return []
        return [{"id": "mock", "payload": "local_data"}]  # Förenklat för test
