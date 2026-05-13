#!/bin/bash

# ============================================================
# WARNING: First time running this script on a server
# ============================================================
# This script will STOP, DISABLE and DELETE the following services:
#   - airflow-scheduler.service
#   - airflow-api.service
#   - data_airflow_server.service
#
# It will ALSO remove the old legacy file:
#   - airflow.service   (if it still exists)
#
# Please review this script before running it the first time.
# ============================================================

echo "=============================================="
echo "   Data Airflow Server - Remove Services"
echo "=============================================="
echo ""

SERVICES=("airflow-scheduler.service" "airflow-api.service" "data_airflow_server.service")

echo "🛑 Stopping services..."
for service in "${SERVICES[@]}"; do
    sudo systemctl stop "$service" 2>/dev/null || true
done

echo "❌ Disabling services..."
for service in "${SERVICES[@]}"; do
    sudo systemctl disable "$service" 2>/dev/null || true
done

echo "🗑️ Removing service files..."
sudo rm -f /etc/systemd/system/airflow-scheduler.service
sudo rm -f /etc/systemd/system/airflow-api.service
sudo rm -f /etc/systemd/system/data_airflow_server.service

# Remove legacy service file (safe to keep)
sudo rm -f /etc/systemd/system/airflow.service

echo "🔄 Reloading systemd daemon..."
sudo systemctl daemon-reload

echo ""
echo "✅ All Data Airflow Server services have been removed."