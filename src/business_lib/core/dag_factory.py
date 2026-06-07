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
    data: Any = None,
    **kwargs
) -> Any:
    """
    Universal task wrapper used by all dynamic DAGs.
    Supports both:
      - Module-level functions (old style)
      - Class methods (new recommended style, e.g. ExtractService.extract_data)
    """
    inject_map = inject_map or {}
    resources = resources or {}

    injected_resources = {}

    # ============================================================
    # 1. Handle resource injection (storage, cache, etc.)
    # ============================================================
    for arg_name, res_id in inject_map.items():
        if res_id in resources:
            res_cfg = resources[res_id]
            try:
                AdapterClass = get_class(res_cfg["type"])
                injected_resources[arg_name] = AdapterClass(**res_cfg.get("config", {}))
            except Exception as e:
                raise RuntimeError(f"Failed to instantiate resource '{res_id}': {e}") from e

    # Merge injected resources into kwargs
    call_kwargs = {**kwargs, **injected_resources}

    # If previous task data is available, pass it
    if data is not None:
        call_kwargs["data"] = data

    # ============================================================
    # 2. Load the target function or class method
    # ============================================================
    if "." in business_function:
        # Class-based style: "ExtractService.extract_data"
        class_name, method_name = business_function.split(".", 1)
        ServiceClass = get_class(f"{business_module}.{class_name}")

        # Instantiate the service class with injected dependencies
        try:
            service_instance = ServiceClass(**injected_resources)
        except TypeError as e:
            # Fallback if the class doesn't accept the injected args in __init__
            service_instance = ServiceClass()

        # Get the method from the instance
        func = getattr(service_instance, method_name)
    else:
        # Old module-level function style
        func = get_class(f"{business_module}.{business_function}")

    # ============================================================
    # 3. Execute the function/method
    # ============================================================
    try:
        result = func(**call_kwargs)
        return result
    except Exception as e:
        print(f"Error executing {business_module}.{business_function}: {e}")
        raise


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