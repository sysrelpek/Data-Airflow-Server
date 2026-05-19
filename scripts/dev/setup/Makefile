# =============================================
# Development Makefile - Data Airflow Server
# =============================================

.PHONY: help setup

help:
	@echo "Available commands:"
	@echo "  make setup     - Setup development environment locally"

setup:
	@echo "=== Setting up development environment ==="
	@pip install -r requirements.txt
	@mkdir -p dags/manifests config/envs
	@echo "Development setup completed."