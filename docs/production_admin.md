# Production Administration

This document contains daily operations, commands, and tools for managing the live Data Airflow Server.

---

### Quick Start

```
# Go to project root
cd /home/etluser/ai-projects/data_airflow_server

# Load production environment variables
set -a
source .env.prod
set +a
```
Rebuild DAGs and Manifests. After making changes to code or YAML manifests, rebuild everything:
```
./scripts/prod/admin/build_dags.sh
```
This command automatically:
- Converts YAML configs → JSON manifests
- Rebuilds all dynamic DAGs

---

## Managing Airflow Services
### Main Services
The production server uses two primary systemd services:
```
Service                     Purpose                         Status Check Command
-------------------------------------------------------------------------------------------------------
airflow-api.service,        Airflow API Server (Web UI),    systemctl status airflow-api.service
airflow-scheduler.service,  Airflow Scheduler,              systemctl status airflow-scheduler.service
```
Useful Service Commands:
```
# Check status of all relevant services
./scripts/prod/system_services/status_all_services.sh

# Restart all services
./scripts/prod/system_services/restart_all_services.sh

# Start all services
./scripts/prod/system_services/start_all_services.sh

# Stop all services
./scripts/prod/system_services/stop_all_services.sh
```

Individual Service Shortcuts
```
./scripts/prod/system_services/status_server.sh
./scripts/prod/system_services/restart_server.sh
./scripts/prod/system_services/stop_server.sh
```

Running Airflow Manually (Debugging)
```
# Start Airflow API + Scheduler in normal mode
./scripts/prod/admin/run.sh

# Start in debug mode (useful for troubleshooting)
./scripts/prod/admin/run_debug.sh
```
Note: In normal operation you should use the systemd services instead of running manually.

Logs and Monitoring
Airflow Web UI
http://<server-ip>:8080



Task Logs
Task logs are available in two ways:

1. Via Airflow UI (recommended)
    - Go to the DAG → Task → Log tab


2. Directly on the filesystem
```
cd /home/etluser/ai-projects/data_airflow_server
tail -f logs/dag_id=<dag_id>/run_id=<run_id>/task_id=<task_id>/attempt=1.log
```

Systemd Service Logs
```
# Follow logs for API server
journalctl -u airflow-api.service -f

# Follow logs for Scheduler
journalctl -u airflow-scheduler.service -f
```


Important Notes

    - Always use the class-based style in your manifests (ExtractService.extract_data, etc.).
    - Old services (data_airflow_server.service and the legacy airflow.service) should remain masked.
    - build_dags.sh now automatically handles manifest conversion from YAML to JSON.


---
### Quick Command Reference
```
Task                            Command
---------------------------------------------------------------------------------------------------
Rebuild manifests + DAGs,       ./scripts/prod/admin/build_dags.sh
Check main services status,     ./scripts/prod/system_services/status_all_services.sh
Restart all services,           ./scripts/prod/system_services/restart_all_services.sh
Start Airflow manually,         ./scripts/prod/admin/run.sh
Start Airflow in debug mode,    ./scripts/prod/admin/run_debug.sh
View scheduler logs,            journalctl -u airflow-scheduler.service -f
View API server logs,           journalctl -u airflow-api.service -f
```
---
## Airflow Web UI

The Airflow web interface is the main way to monitor and manage your DAGs.

**URL:**
http://<your-server-ip>:8080

Example: http://192.168.1.218:8080
