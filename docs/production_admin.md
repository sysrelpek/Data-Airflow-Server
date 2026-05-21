```markdown
# This document contains a list of all production operations, commands and tools

Daily commands for managing the live Data Airflow Server.

## Quick start commands

```bash
# Go to project root
cd /home/etluser/ai-projects/data_airflow_server

# Load production environment
set -a
source .env.prod
set +a

# Rebuild all dynamic DAGs from manifests (run after every code or manifest change)
./scripts/prod/admin/build_dags.sh

# Start Airflow in normal mode
./scripts/prod/admin/run.sh

# Start Airflow in debug mode (useful during troubleshooting)
./scripts/prod/admin/run_debug.sh


# Quick shortcuts
./scripts/prod/system_services/start_all_services.sh
./scripts/prod/system_services/stop_all_services.sh
./scripts/prod/system_services/restart_all_services.sh
./scripts/prod/system_services/status_all_services.sh

# Individual server shortcuts
./scripts/prod/system_services/restart_server.sh
./scripts/prod/system_services/status_server.sh
./scripts/prod/system_services/stop_server.sh



# Logs & monitoring
Airflow web UI: http://192.168.1.218:8080 (as configured in .env.prod)
Logs are in ${AIRFLOW_HOME}/logs/
Systemd logs: journalctl -u airflow-webserver -f or journalctl -u airflow-scheduler -f