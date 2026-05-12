SHELL := /bin/bash
.PHONY: help build restart status clean local-deploy logs tail-logs

# ====================== HELP ======================
help:
	@echo "=== Data-Airflow-Server Makefile ==="
	@echo ""
	@echo "  make build          → Build DAGs + reserialize"
	@echo "  make restart        → Restart Airflow services"
	@echo "  make status         → Show Airflow service status"
	@echo "  make logs           → Show recent logs"
	@echo "  make tail-logs      → Follow logs in real-time"
	@echo "  make clean          → Clean generated files"
	@echo "  make local-deploy   → Build + Sync to server (run ONLY on local dev machine)"
	@echo ""

# ====================== COMMANDS ======================
build:
	@echo "🔨 Building DAGs from pipelines..."
	@set -a && source .env && set +a && \
	 source .venv/bin/activate && \
	 ./build_dags.sh && \
	 echo "🔄 Reserializing all DAGs..." && \
	 airflow dags reserialize
	@echo "✅ DAGs built and reserialized successfully."

restart:
	@echo "🔄 Restarting Airflow services..."
	@set -a && source .env && set +a && \
	 ./restart_airflow_service.sh

status:
	@echo "📊 Airflow service status:"
	sudo systemctl status airflow.service --no-pager

logs:
	@echo "📜 Last 100 Airflow logs:"
	sudo journalctl -u airflow.service --no-pager -n 100

tail-logs:
	@echo "📡 Following Airflow logs (Ctrl+C to stop)..."
	sudo journalctl -u airflow.service -f

clean:
	@echo "🧹 Cleaning generated files..."
	rm -rf dags/ml/*.py
	rm -rf logs/*
	rm -rf reporting/*
	@echo "Clean completed."

# Local-only full deploy
local-deploy:
	@echo "🚀 Running full local deploy..."
	@$(MAKE) build
	./sync_to_server.sh

# Quick full cycle
deploy: build restart
	@echo "🚀 Deployed and restarted successfully."