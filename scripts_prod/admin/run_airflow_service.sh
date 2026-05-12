#!/bin/bash
# =============================================
# run_airflow_service.sh
# =============================================

echo "🚀 Starting Airflow services (via systemd)..."

sudo systemctl start airflow-scheduler.service
sudo systemctl start airflow-api.service

echo "✅ Services started"
echo "📊 Check status with: sudo systemctl status airflow-api.service"
echo "🌐 UI should be available at: http://192.168.1.218:8080"