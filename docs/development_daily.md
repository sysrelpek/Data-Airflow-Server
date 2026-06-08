# Daily Development Workflow

This document describes the typical daily workflow when developing on the Data Airflow Server.

---

## 1. Start Your Development Session

```bash
cd /path/to/data_airflow_server
source .venv/bin/activate
```
---

## 2. Daily Development Cycle
### Step 1: Develop / Modify Code
You can work on:

- YAML Manifests → dags/configs/*.yaml (human-readable DAG definitions)
- Business Logic → src/business_lib/services/ (class-based services)
- DAG Factory / Core → src/business_lib/core/
- Tests → tests/

### Step 2: Test Locally (Recommended)
Before syncing to production, run the tests:
```./scripts/test/run_tests.sh```

### Step 3: Deploy Changes to Production Server
When you're ready to test on the production server:
```./scripts/dev/sync_to_server.sh```

This will:

- Sync your changes
- Install the package in editable mode
- Automatically rebuild JSON manifests from YAML
- Rebuild all DAGs

### Step 4: Verify on the Server (Optional)
After syncing, you can SSH to the server and verify:
```
ssh etluser@<production-server>

cd /home/etluser/ai-projects/data_airflow_server

# Check that DAGs were rebuilt successfully
./scripts/prod/admin/build_dags.sh

# Check service status
./scripts/prod/system_services/status_all_services.sh
```


Key Principles

- Edit YAML first: DAG structure is defined in ```dags/configs/```
- Use class-based services: Business logic lives in ```src/business_lib/services/``` (e.g. ExtractService, TransformService, LoadService)
- Let automation do the work: ```sync_to_server.sh + build_dags.sh``` handle manifest conversion and DAG rebuilding
- Test before syncing: Run ```./scripts/test/run_tests.sh``` locally when possible

```
Task                                        Command
--------------------------------------------------------------------------------------------------------------
Run local tests                             ./scripts/test/run_tests.sh
Sync changes to production                  ./scripts/dev/sync_to_server.sh
Rebuild manifests + DAGs (server)           ./scripts/prod/admin/build_dags.sh
Check production services                   ./scripts/prod/system_services/status_all_services.sh
```

### Tips

- Changes to YAML manifests are automatically picked up after running sync_to_server.sh
- You can develop and test new services locally before deploying
- Use the Airflow UI on the production server to inspect DAGs and task logs after syncing

