# ToDO: Production Install (First-time initialization)

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