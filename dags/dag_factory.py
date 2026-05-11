import json
import importlib
from pathlib import Path
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

# Inställningar
MANIFEST_DIR = Path(__file__).parent / "manifests"


def get_class(path: str):
    """Hämtar en klass eller funktion dynamiskt baserat på sträng-sökväg."""
    module_path, attr_name = path.rsplit(".", 1)
    module = importlib.import_module(module_path)
    return getattr(module, attr_name)


def task_wrapper(business_module, business_function, inject_map, resources, **context):
    """
    En brygga som körs i Airflow-worker.
    Den hämtar resurser (adaptrar) och skickar in dem i affärsfunktionen.
    """
    # 1. Instansiera de resurser (adaptrar) som behövs för denna task
    injected_resources = {}
    for arg_name, res_id in inject_map.items():
        res_cfg = resources[res_id]
        AdapterClass = get_class(res_cfg["type"])
        # Skapar adaptern med dess specifika konfiguration (t.ex. connection_string)
        injected_resources[arg_name] = AdapterClass(**res_cfg.get("config", {}))

    # 2. Hämta själva affärsfunktionen
    func = get_class(f"{business_module}.{business_function}")

    # 3. Hantera data-flödet (XCom)
    # Vi hämtar resultatet från föregående steg om det finns
    ti = context['ti']
    upstream_ids = context['task'].upstream_task_ids
    if upstream_ids:
        # För enkelhetens skull hämtar vi data från det första uppströms-steget
        input_data = ti.xcom_pull(task_ids=list(upstream_ids)[0])
        return func(input_data, **injected_resources)

    # Om det är första steget (inget input_data)
    return func(**injected_resources)


# --- LOADER LOGIC ---
# Vi loopar igenom alla JSON-filer i manifests-mappen
for manifest_file in MANIFEST_DIR.glob("*.json"):
    with open(manifest_file, "r") as f:
        config = json.load(f)

    dag = DAG(
        dag_id=config["dag_id"],
        start_date=datetime(2023, 1, 1),
        schedule_interval=None,  # Triggeras manuellt eller via sensor
        catchup=False
    )

    tasks = {}

    # Skapa alla tasks
    for step in config["workflow"]:
        t = PythonOperator(
            task_id=step["id"],
            python_callable=task_wrapper,
            op_kwargs={
                "business_module": step["business_module"],
                "business_function": step["business_function"],
                "inject_map": step.get("inject", {}),
                "resources": config["resources"]
            },
            dag=dag
        )
        tasks[step["id"]] = t

    # Sätt upp beroenden (pilarna i DAGen)
    for step in config["workflow"]:
        for dep_id in step.get("depends_on", []):
            tasks[dep_id] >> tasks[step["id"]]

    # Registrera DAGen globalt i Airflow
    globals()[config["dag_id"]] = dag
