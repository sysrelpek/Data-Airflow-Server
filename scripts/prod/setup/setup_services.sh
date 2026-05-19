#!/bin/bash
echo "=============================================="
echo "   Data Airflow Server - Full Service Setup"
echo "=============================================="
echo ""
echo "📁 Copying service files to /etc/systemd/system/..."
sudo cp ../system_services/systemd/*.service /etc/systemd/system/

echo "🔄 Reloading systemd daemon..."
sudo systemctl daemon-reload

SERVICES=("airflow-scheduler.service" "airflow-api.service" "data_airflow_server.service")

echo "✅ Enabling services to start on boot..."
for service in "${SERVICES[@]}"; do
    sudo systemctl enable "$service"
done

echo "🚀 Starting services..."
for service in "${SERVICES[@]}"; do
    sudo systemctl start "$service"
done

echo ""
echo "📊 Current Status:"
sudo systemctl status "${SERVICES[@]}" --no-pager

echo ""
echo "✅ Setup completed successfully!"
echo "All services are now enabled and running."