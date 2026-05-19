#!/bin/bash
echo "🚀 Starting all Airflow services..."
sudo systemctl start airflow-scheduler.service
sudo systemctl start airflow-api.service
echo "✅ All services started."