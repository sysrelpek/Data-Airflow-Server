SHELL := /bin/bash
.PHONY: help build restart status clean logs tail-logs

help:
	@echo "=== DEV Makefile ==="
	@echo "  make build     → Build DAGs"
	@echo "  make restart   → Restart services"
	@echo "  make status    → Show status"
	@echo "  make logs      → Show logs"
	@echo "  make tail-logs → Follow logs"
	@echo "  make clean     → Clean generated files"

# Safety check
check-env:
	@set -a && source ../../.env && set +a && \
	 if [ "$$ENV" != "dev" ]; then \
	   echo "❌ ERROR: This Makefile can only run when ENV=dev"; \
	   exit 1; \
	 fi

build: check-env
	@set -a && source ../../.env && set +a && \
	 source ../../.venv/bin/activate && \
	 ../../build_dags.sh && \
	 airflow dags reserialize

restart: check-env
	@set -a && source ../../.env && set +a && \
	 ../../restart_airflow_service.sh

status:
	sudo systemctl status airflow.service --no-pager

logs:
	sudo journalctl -u airflow.service --no-pager -n 100

tail-logs:
	sudo journalctl -u airflow.service -f

