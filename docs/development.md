# Development Workflow

## 1. Initial Setup (once)

```bash
# 1. Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements-dev.txt
pip install -r requirements-test.txt
pip install -e .

# 3. Make key scripts executable
chmod +x scripts/dev/sync_to_server.sh
chmod +x scripts/dev/build_manifest.py
chmod +x scripts/test/run_tests.sh

# 4. (Optional but recommended) Build initial manifests from YAML
./scripts/dev/build_manifest.py