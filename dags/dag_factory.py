# =============================================================================
# dags/dag_factory.py
# Airflow entry point - scans manifests and registers DAGs
# (Thin wrapper only  -  core logic lives in business_lib)
# =============================================================================

import json
from pathlib import Path
from business_lib.core.dag_factory import create_dag_from_manifest

MANIFEST_DIR = Path(__file__).parent / "manifests"

# --- LOADER LOGIC ---
for manifest_file in MANIFEST_DIR.glob("*.json"):
    with open(manifest_file, "r") as f:
        config = json.load(f)

    dag = create_dag_from_manifest(config)

    # Register DAG globally so Airflow can find it
    globals()[config["dag_id"]] = dag