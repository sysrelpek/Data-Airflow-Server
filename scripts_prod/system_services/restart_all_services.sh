#!/bin/bash
echo "🔄 Restarting all Airflow services..."
sudo systemctl restart airflow-scheduler.service
sudo systemctl restart airflow-api.service
echo "✅ All services restarted."