#!/bin/bash
echo "📊 Status of all Airflow services:"
sudo systemctl status airflow-scheduler.service airflow-api.service data_airflow_server.service --no-pager