#!/bin/bash
# =============================================
# stop_airflow_service.sh
# =============================================

echo "🛑 Stopping Airflow services..."

sudo systemctl stop airflow-api.service
sudo systemctl stop airflow-scheduler.service

echo "✅ Airflow services stopped."