# =============================================================================
# src/business_lib/core/dag_factory.py
# Pure core logic for creating Airflow DAGs from manifests
# =============================================================================

import importlib
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator


def get_class(path: str):
    """Dynamically import a class or function from a string path."""
    module_path, attr_name = path.rsplit(".", 1)
    module = importlib.import_module(module_path)
    return getattr(module, attr_name)


def task_wrapper(business_module: str, business_function: str, inject_map: dict, resources: dict, **context):
    """Bridge that runs inside Airflow worker."""
    injected_resources = {}
    for arg_name, res_id in inject_map.items():
        res_cfg = resources[res_id]
        AdapterClass = get_class(res_cfg["type"])
        injected_resources[arg_name] = AdapterClass(**res_cfg.get("config", {}))

    func = get_class(f"{business_module}.{business_function}")

    ti = context['ti']
    upstream_ids = context['task'].upstream_task_ids
    if upstream_ids:
        input_data = ti.xcom_pull(task_ids=list(upstream_ids)[0])
        return func(input_data, **injected_resources)

    return func(**injected_resources)


def create_dag_from_manifest(manifest_config: dict):
    """Core function: Creates a complete Airflow DAG from a manifest."""
    dag = DAG(
        dag_id=manifest_config["dag_id"],
        start_date=datetime(2023, 1, 1),
        schedule=None,           # ← Fixed for current Airflow version
        catchup=False
    )

    tasks = {}

    for step in manifest_config.get("workflow", []):
        t = PythonOperator(
            task_id=step["id"],
            python_callable=task_wrapper,
            op_kwargs={
                "business_module": step["business_module"],
                "business_function": step["business_function"],
                "inject_map": step.get("inject", {}),
                "resources": manifest_config.get("resources", {})
            },
            dag=dag
        )
        tasks[step["id"]] = t

    for step in manifest_config.get("workflow", []):
        for dep_id in step.get("depends_on", []):
            tasks[dep_id] >> tasks[step["id"]]

    return dag