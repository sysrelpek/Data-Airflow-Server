# Production Setup – Post-Sync ToDo Checklist

**Run this checklist after every `sync_to_server.sh`  from your development machine.**

This is the mandatory workflow to make sure the production server is updated correctly.

## Post-Sync Checklist (must do)

```bash
# 1. Go to project root on the server
cd /home/etluser/ai-projects/data_airflow_server


# 2. Make all production scripts executable
#    (they get overwritten by every sync)
chmod +x scripts/prod/admin/*.sh \
        scripts/prod/setup/*.sh \
        scripts/prod/system_services/*.sh

# 3. Rebuild all DAGs from the latest manifests
./scripts/prod/admin/build_dags.sh


# 4. Restart all Airflow services
#    (so they pick up the new code and DAGs)
./scripts/prod/system_services/restart_all_services.sh
# or use the shortcut:
./scripts/prod/system_services/restart_server.sh


# 5. Check that everything is running correctly
./scripts/prod/system_services/status_all_services.sh
# or use the shortcut:
./scripts/prod/system_services/status_server.sh