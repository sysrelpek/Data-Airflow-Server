import pytest
import json
import os
from scripts.build_manifest import ManifestFactory


def test_manifest_generation_structure():
    # Setup
    os.environ["ENV"] = "dev"
    factory = ManifestFactory(env="dev")

    # Execute
    manifest_path = factory.build("ingest_pipeline")

    # Verify
    assert manifest_path.exists()

    with open(manifest_path, "r") as f:
        data = json.load(f)

    # Kontrollera att alla kritiska delar finns med
    assert "dag_id" in data
    assert "resources" in data
    assert "workflow" in data

    # Kontrollera att 'main_db' injiceras korrekt i 'store'-steget
    store_step = next(s for s in data["workflow"] if s["id"] == "store")
    assert store_step["inject"]["storage"] == "main_db"

    # Kontrollera att dev-miljön använder FileAdapter (baserat på din dev_resources.yaml)
    assert "FileStorageAdapter" in data["resources"]["main_db"]["type"]


def test_dependency_integrity():
    # Kontrollera att inga steg har beroenden till icke-existerande steg
    factory = ManifestFactory(env="dev")
    path = factory.build("ingest_pipeline")

    with open(path, "r") as f:
        data = json.load(f)

    all_ids = [step["id"] for step in data["workflow"]]
    for step in data["workflow"]:
        for dep in step["depends_on"]:
            assert dep in all_ids, f"Task {step['id']} depends on missing task {dep}"
