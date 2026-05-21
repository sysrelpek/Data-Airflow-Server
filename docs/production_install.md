# ToDO: Production Install (First-time initialization)

# Future installation tasks (ToDO)
    - Set up PostgreSQL databases (airflow_metadata_db, airflow_db, warehouse_db)
    - Configure proper secrets / JWT keys
    - Set up proper logging rotation
    - Configure backup strategy
    - Add monitoring (Prometheus / Grafana)
    - Set up SSL / reverse proxy (nginx)

This document contains all the **one-time installation tasks** that are only needed the very first time the server is set up.

## First-time initialization steps

```bash
# 1. Go to the project folder
cd /home/etluser/ai-projects/data_airflow_server

# 2. Initialize Airflow metadata database (only once)
airflow db init

# 3. Create the first admin user (only once)
airflow users create \
  --username admin \
  --password admin \
  --firstname Admin \
  --lastname User \
  --role Admin \
  --email admin@example.com



## ReInstallation (If needed)

# 1. cd /home/etluser/ai-projects/data_airflow_server
./scripts/prod/install/tools/remove_services.sh

# 2. cd /home/etluser/ai-projects/data_airflow_server
./scripts/prod/install/setup_services.sh