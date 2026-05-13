# Data Airflow Server - Production Command List

This is the official command reference for production operations.

---

## Server Root Commands (Main Entry Point)

Use these as your primary commands.

| Command                        | Description                                      | Run from |
|-------------------------------|--------------------------------------------------|----------|
| `./start_server.sh`           | Start the entire Data Airflow Server             | system_services/ |
| `./stop_server.sh`            | Stop the entire Data Airflow Server              | system_services/ |
| `./restart_server.sh`         | Restart the entire Data Airflow Server           | system_services/ |
| `./status_server.sh`          | Show full status + recent logs                   | system_services/ |

---

## Service-Level Commands

| Command                          | Description                                      | Run from |
|----------------------------------|--------------------------------------------------|----------|
| `./start_all_services.sh`        | Start only Airflow services                      | system_services/ |
| `./stop_all_services.sh`         | Stop only Airflow services                       | system_services/ |
| `./restart_all_services.sh`      | Restart only Airflow services                    | system_services/ |
| `./status_all_services.sh`       | Detailed status of all services                  | system_services/ |

---

## Setup & Maintenance

| Command                            | Description                                              | Run from |
|------------------------------------|----------------------------------------------------------|----------|
| `./setup/setup_services.sh`        | Copy services, enable on boot, start everything         | project root |
| `./setup/remove_services.sh`       | Stop, disable and delete all services (with legacy cleanup) | project root |

> **Important**: Review `remove_services.sh` the first time you run it.

---

## Direct Systemd Commands (Advanced)

| Command | Description |
|---------|-------------|
| `systemctl status data_airflow_server.service` | Check master service |
| `systemctl status airflow-scheduler.service` | Check scheduler |
| `journalctl -u data_airflow_server.service -f` | Follow live logs |
| `systemctl cat data_airflow_server.service` | Show service definition |

---

**Last updated:** 2026-05-13  
**Structure:** Server Root → Services → Setup

You now have full control with a clean hierarchy.