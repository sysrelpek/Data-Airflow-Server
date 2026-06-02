# Daily Development

## Daily workflow

```bash
# 1. Go to project root
cd /path/to/Data-Airflow-Server

# 2. Activate virtual environment
source .venv/bin/activate

# 3. Develop
#    • Edit DAG definitions in dags/configs/          (YAML - human friendly)
#    • Run ./scripts/dev/build_manifest.py            (generates JSON in dags/manifests/)
#    • Add/edit code in src/business_lib/
#    • Update tests in tests/

# 4. Test locally
./scripts/test/run_tests.sh

# 5. Deploy changes to production server
./scripts/dev/sync_to_server.sh