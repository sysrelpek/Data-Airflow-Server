# Production Setup (One-time)

This document describes how to set up the Data Airflow Server on the production machine **after** you have run `sync_to_server.sh` from your development machine.

## Prerequisites
- The project code is already on the server (via `sync_to_server.sh`)
- Server is running Ubuntu/Debian (or compatible Linux)
- Git, Python 3.11+, PostgreSQL and systemd are installed
- You are logged in as the `etluser` (or equivalent service user)

## Step-by-step setup

```bash
# 1. Go to the project folder on the server
cd /home/etluser/ai-projects/data_airflow_server

# 2. Make sure all production scripts are executable
#    (they are overwritten on every sync_to_server.sh)
chmod +x scripts/prod/admin/*.sh scripts/prod/setup/*.sh scripts/prod/system_services/*.sh

# 3. Run the production setup scripts
./scripts/prod/setup/setup_services.sh