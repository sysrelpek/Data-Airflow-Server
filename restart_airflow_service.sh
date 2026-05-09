#!/bin/bash
# =============================================
# restart_airflow_service.sh
# =============================================

echo "🔄 Restarting Airflow services..."

sudo systemctl restart airflow-scheduler.service
sudo systemctl restart airflow-api.service

echo "✅ Airflow services restarted"
echo "🔄 DAGs reserialized automatically by the service"
echo "🌐 UI: http://192.168.1.218:8080"