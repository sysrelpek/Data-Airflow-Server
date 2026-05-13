
from pathlib import Path

from business_lib.infrastructure.storage.file_adapter import FileStorageAdapter
from business_lib.services.ingest.feature_ingest import collect_data, clean_and_transform, store_data


def test_full_yaml_flow_locally(tmp_path):
    # Setup: Använd FileAdapter för lokalt test istället för Postgres
    mock_storage = FileStorageAdapter(base_path=str(tmp_path))

    # Simulera CSV
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("id,score\n1,85\n2,90")

    # Kör stegen i ordning (som definierat i YAML)
    raw = collect_data(str(csv_file))
    processed = clean_and_transform(raw)
    count = store_data(processed, storage=mock_storage, logger=None)

    assert count == 2
    assert mock_storage.get_by_id("1")["score"] == 0.85

def test_save_data_to_file():
    adapter = FileStorageAdapter(base_path="./tests/tmp_db")
    data = {"id": "user_1", "score": 0.85}
    adapter.save(entity_id="user_1", data=data)
    assert adapter.get_by_id("user_1") is not None


def test_ingest():
    # Vi injicerar FileStorageAdapter istället för Postgres!
    adapter = FileStorageAdapter(base_path="./tests/tmp_db")
    assert adapter.get_by_id("user_1") is not None

def test_remove_json_():

    target_json_files_path = Path("./tests/tmp_db")
    if target_json_files_path.exists():
        for file_path in target_json_files_path.glob("*.json"):
            file_path.unlink()

