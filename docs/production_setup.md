# Production Setup (Post-Sync Deployment)

This document describes what should be done **after** running `sync_to_server.sh`.

> Many steps that previously required manual work are now handled **automatically** during the sync process.


### What Happens Automatically

When you run `sync_to_server.sh`, the following actions are performed automatically on the server:

- Files are synced from your development machine
- `pip install -e .` is executed
- Production scripts are made executable
- JSON manifests are rebuilt from YAML files (`build_all_manifests.py`)
- All DAGs are rebuilt (`build_dags.sh`)
- Virtual environment is activated with the correct path

#
## Recommended Post-Sync Steps

After `sync_to_server.sh` completes, perform the following verification steps:

___
### 1. Verify that DAGs were rebuilt successfully

You should see output similar to this at the end of the sync:
🔨 Building JSON manifests from YAML configs...
✓ example_ingest_pipeline.yaml → example_ingest_pipeline.json
🚀 Rebuilding all DAGs from manifests...
✅ DAGs successfully rebuilt.


If you see errors here, run manually on the server:
```
./scripts/prod/admin/build_dags.sh
```

___
### 2. Check that the main Airflow services are running

systemctl status airflow-api.service airflow-scheduler.service --no-pager

Both services should show Active: active (running).


___
### 3. Ensure old/broken services are masked
The following services should be masked (they are no longer used):
```
systemctl status data_airflow_server.service airflow.service --no-pager
```
If they are not masked, run once:
```
sudo systemctl mask --now data_airflow_server.service
sudo systemctl mask --now airflow.service
sudo systemctl daemon-reload
```
___
### 4. Verify your DAGs in the Airflow UI
After syncing, open the Airflow web interface and confirm that:
- Your DAGs appear (especially example_ingest_pipeline)
- They have the latest code and manifests
- Tasks are running without errors

When to Run Commands Manually
You only need to run commands manually in these situations:

- build_dags.sh reported errors during sync
- You made changes directly on the production server
- You are troubleshooting an issue
- You want to rebuild DAGs without doing a full sync

In normal day-to-day work, running sync_to_server.sh from your development machine is usually sufficient.


```
Important Notes

- The old deploy.sh script has been removed. Its functionality is now built into sync_to_server.sh and build_dags.sh.
- Always use the class-based style in your YAML manifests (ExtractService.extract_data, TransformService.transform_data, etc.).
- build_dags.sh now automatically converts YAML configuration files into JSON manifests.
- Do not start the old data_airflow_server.service or legacy airflow.service — they have been replaced.
```
```
Action                                  Command                                                         When to use
---------------------------------------------------------------------------------------------------------------------------------
Sync code from development machine,     ./scripts/dev/sync_to_server.sh,                                After making changes
Rebuild manifests and DAGs,             ./scripts/prod/admin/build_dags.sh,                             After YAML changes or errors
Check main Airflow services,            systemctl status airflow-api.service airflow-scheduler.service, After sync or issues
Mask old/broken services (one time),    sudo systemctl mask --now <service>,                            During initial setup
```
