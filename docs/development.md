# Development Setup

This document describes the initial setup required to start developing on the Data Airflow Server project.

## 1. Create and Activate Virtual Environment

```
python -m venv .venv
source .venv/bin/activate
```



## 2. Install Dependencies

```
# Install development dependencies
pip install -r requirements-dev.txt

# Install test dependencies (optional but recommended)
pip install -r requirements-test.txt

# Install the project in editable mode
pip install -e .
```


## 3. Make Scripts Executable
```
chmod +x scripts/dev/sync_to_server.sh
chmod +x scripts/test/run_tests.sh
chmod +x scripts/prod/admin/build_dags.sh
```

## 4. Initial Manifest and DAG Build (Optional but Recommended)
After the first setup, you can generate the initial JSON manifests and DAGs:
```
./scripts/prod/admin/build_dags.sh
```

Note: build_dags.sh now automatically:
     
- Converts all YAML files in dags/configs/ into JSON manifests
- Rebuilds all dynamic DAGs


## 5. Development Workflow
For daily development work, see development_daily.md.
Key Points

- Edit human-readable YAML files in dags/configs/
- Run sync_to_server.sh to deploy changes to production
- build_dags.sh handles manifest conversion and DAG rebuilding automatically
- Services are implemented using a class-based architecture (ExtractService, TransformService, LoadService, etc.)

## Project Structure Overview
```
dags/
├── configs/           # Human-editable YAML manifests (edit these)
└── manifests/         # Generated JSON manifests (auto-generated)

src/business_lib/
├── core/
│   ├── dag_factory.py
│   ├── build_all_manifests.py
│   └── manifest_builder.py
└── services/          # Business logic services (class-based)
```


## Next Steps
After completing the initial setup, you can:

- Start developing new DAGs or services.
  Run tests with:
  ```./scripts/test/run_tests.sh```
- Sync changes to the production server using:
  ```./scripts/dev/sync_to_server.sh```