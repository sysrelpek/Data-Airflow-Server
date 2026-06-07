# =============================================================================
# src/business_lib/core/dag_factory.py
# Pure core logic for creating Airflow DAGs from manifests
# =============================================================================

from typing import Any, Dict, List, Optional
import importlib
from pathlib import Path
from datetime import datetime
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator

def get_class(path: str):
    """Dynamically import a class or function from a string path."""
    module_path, attr_name = path.rsplit(".", 1)
    module = importlib.import_module(module_path)
    return getattr(module, attr_name)

def task_wrapper(
    business_module: str,
    business_function: str,
    inject_map: dict = None,
    resources: dict = None,
    depends_on: list = None,
    **context
) -> Any:
    """
    Universal task wrapper with proper XCom data passing between dependent tasks.
    """
    ti = context.get("ti")
    inject_map = inject_map or {}
    resources = resources or {}
    depends_on = depends_on or []

    injected_resources = {}

    # 1. Inject resources (storage, etc.)
    for arg_name, res_id in inject_map.items():
        if res_id in resources:
            res_cfg = resources[res_id]
            AdapterClass = get_class(res_cfg["type"])
            injected_resources[arg_name] = AdapterClass(**res_cfg.get("config", {}))

    # 2. Pull data from upstream task via XCom (if this task depends on others)
    data = None
    if depends_on and ti:
        upstream_task_id = depends_on[-1]  # take the last upstream task
        data = ti.xcom_pull(task_ids=upstream_task_id, key="return_value")

    call_kwargs = {**injected_resources}
    if data is not None:
        call_kwargs["data"] = data

    # 3. Load and execute the target (class method or function)
    if "." in business_function:
        class_name, method_name = business_function.split(".", 1)
        ServiceClass = get_class(f"{business_module}.{class_name}")
        service_instance = ServiceClass(**injected_resources)
        func = getattr(service_instance, method_name)
    else:
        func = get_class(f"{business_module}.{business_function}")

    # 4. Execute
    result = func(**call_kwargs)

    # 5. Push result to XCom so downstream tasks can use it
    if ti:
        ti.xcom_push(key="return_value", value=result)

    return result

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