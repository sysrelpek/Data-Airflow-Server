# Production Setup (One-time)

This document describes how to set up the Data Airflow Server on the production machine for the first time.

## Prerequisites
- Server is running Ubuntu/Debian (or compatible Linux)
- Git, Python 3.11+, PostgreSQL are installed
- You have sudo access as the `etluser` (or equivalent service user)

## Step-by-step setup

```bash
# 1. Clone the repository (if not already done)
cd /home/etluser/ai-projects
git clone https://github.com/sysrelpek/Data-Airflow-Server.git
cd Data-Airflow-Server

# 2. Copy and configure production environment
cp .env.prod.example .env.prod
# ← Edit .env.prod (set real passwords, secrets, paths)


chmod +x scripts/prod/setup/*.sh scripts/prod/system_services/*.sh

# 3. Run the production setup scripts (will be in scripts/prod/setup/)
./scripts/prod/setup/setup_services.sh


# 4. Initialize Airflow database (first time only)
airflow db init

# 5. Create admin user (if needed)
airflow users create --username admin --password admin --firstname Admin --lastname User --role Admin --email admin@example.com