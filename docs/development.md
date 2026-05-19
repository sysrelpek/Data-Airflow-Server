# Development Workflow

## 1. Initial Setup (once)

```bash
cd Data-Airflow-Server
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pip install -e .
cp .env.dev.example .env.dev
# Edit .env.dev