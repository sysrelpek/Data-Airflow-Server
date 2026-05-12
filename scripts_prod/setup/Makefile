# =============================================
# Production Makefile - Data Airflow Server
# =============================================

.PHONY: help setup deploy

help:
	@echo "Available commands:"
	@echo "  make setup     - Setup production environment on server"
	@echo "  make deploy    - Deploy updated manifests + configs to server"

setup:
	@echo "=== Setting up production environment ==="
	@ssh ${USER}@${SERVER} 'mkdir -p ${AIRFLOW_HOME}/dags/manifests ${AIRFLOW_HOME}/config'
	@rsync -avz --delete --exclude-from=scripts_dev/.rsync_exclude . ${USER}@${SERVER}:${AIRFLOW_HOME}/
	@echo "Production setup completed."

deploy:
	@echo "=== Deploying to production server ==="
	@rsync -avz --delete --exclude-from=scripts_dev/.rsync_exclude . ${USER}@${SERVER}:${AIRFLOW_HOME}/
	@ssh ${USER}@${SERVER} 'cd ${AIRFLOW_HOME} && docker compose restart airflow-scheduler airflow-webserver'
	@echo "Deployment completed - Airflow restarted."