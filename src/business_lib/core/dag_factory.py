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
    **kwargs   # ← This captures rows, schema, etc. from op_kwargs
) -> Any:
    ti = kwargs.get("ti")
    inject_map = inject_map or {}
    resources = resources or {}
    depends_on = depends_on or []

    injected_resources = {}

    # 1. Inject resources
    for arg_name, res_id in inject_map.items():
        if res_id in resources:
            res_cfg = resources[res_id]
            AdapterClass = get_class(res_cfg["type"])
            injected_resources[arg_name] = AdapterClass(**res_cfg.get("config", {}))

    # 2. Pull data from upstream via XCom
    data = None
    if depends_on and ti:
        upstream_task_id = depends_on[-1]
        data = ti.xcom_pull(task_ids=upstream_task_id, key="return_value")

    # 3. Build call arguments
    call_kwargs = {**injected_resources}
    if data is not None:
        call_kwargs["data"] = data

    # === NEW: Forward extra parameters (rows, schema, etc.) ===
    # Remove internal Airflow keys
    internal_keys = {"ti", "task_instance", "dag", "run_id", "dag_run", "params"}
    extra_kwargs = {k: v for k, v in kwargs.items() if k not in internal_keys}
    call_kwargs.update(extra_kwargs)
    # ============================================================

    # 4. Load and call the target function/method
    if "." in business_function:
        class_name, method_name = business_function.split(".", 1)
        ServiceClass = get_class(f"{business_module}.{class_name}")
        service_instance = ServiceClass(**injected_resources)
        func = getattr(service_instance, method_name)
    else:
        func = get_class(f"{business_module}.{business_function}")

    result = func(**call_kwargs)

    # 5. Push result to XCom
    if ti:
        ti.xcom_push(key="return_value", value=result)

    return result

def create_dag_from_manifest(manifest: dict) -> DAG:
    dag_id = manifest["dag_id"]
    schedule = manifest.get("schedule")
    resources = manifest.get("resources", {})

    dag = DAG(
        dag_id=dag_id,
        schedule=schedule,
        start_date=datetime(2025, 1, 1),
        catchup=False,
        tags=["dynamic", "example"],
    )

    tasks = {}

    for step in manifest.get("workflow", []):
        task_id = step["id"]
        depends_on = step.get("depends_on", [])

        # === NEW: Automatically forward all extra keys (rows, schema, etc.) ===
        op_kwargs = {
            "business_module": step["business_module"],
            "business_function": step["business_function"],
            "inject_map": step.get("inject", {}),
            "resources": manifest.get("resources", {}),
            "depends_on": depends_on,
        }

        # Add any extra parameters defined in the task (rows, schema, delay_seconds, etc.)
        reserved_keys = {"id", "business_module", "business_function", "inject", "depends_on"}
        for key, value in step.items():
            if key not in reserved_keys:
                op_kwargs[key] = value
        # =====================================================================

        t = PythonOperator(
            task_id=task_id,
            python_callable=task_wrapper,
            op_kwargs=op_kwargs,
            dag=dag,
        )

        tasks[task_id] = t

        # Set task dependencies
        for upstream_id in depends_on:
            if upstream_id in tasks:
                tasks[upstream_id] >> t
    return dag