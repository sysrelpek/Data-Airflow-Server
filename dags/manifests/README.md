# Manifests

This folder contains **generated JSON manifests** used by `dag_factory.py`.

> **Important:** These files are **auto-generated**. Do not edit them manually.

## How Manifests Are Generated

1. Edit the human-readable source files in `dags/configs/*.yaml`
2. Run `./scripts/prod/admin/build_dags.sh` (or it runs automatically during `sync_to_server.sh`)
3. `build_all_manifests.py` converts YAML → JSON
4. `dag_factory.py` loads the JSON files to create the DAGs

## Expected Structure of a Generated Manifest

Each JSON file should contain:

```json
{
  "_meta": {
    "source_file": "example_ingest_pipeline.yaml",
    "generated_at": "2026-06-08T21:20:00Z",
    "generated_by": "build_all_manifests.py"
  },
  "dag_id": "example_ingest_pipeline",
  "schedule": "@daily",
  "resources": {
    "storage": {
      "type": "business_lib.infrastructure.storage.file_adapter.FileStorageAdapter",
      "config": {
        "base_path": "./local_db"
      }
    }
  },
  "workflow": [
    {
      "id": "extract",
      "business_module": "business_lib.services.extract_service",
      "business_function": "ExtractService.extract_data",
      "depends_on": [],
      "inject": {
        "storage": "storage"
      }
    },
    {
      "id": "transform",
      "business_module": "business_lib.services.transform_service",
      "business_function": "TransformService.transform_data",
      "depends_on": ["extract"],
      "inject": {
        "storage": "storage"
      }
    },
    {
      "id": "load",
      "business_module": "business_lib.services.load_service",
      "business_function": "LoadService.load_to_warehouse",
      "depends_on": ["transform"],
      "inject": {
        "storage": "storage"
      }
    }
  ]
}