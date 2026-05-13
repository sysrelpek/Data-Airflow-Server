#!/bin/bash
echo "🛑 Stopping all Airflow services..."
sudo systemctl stop airflow-api.service
sudo systemctl stop airflow-scheduler.service
echo "✅ All services stopped."