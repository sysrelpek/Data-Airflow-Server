from typing import Any, Dict, List
import logging
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator

logger = logging.getLogger(__name__)


def get_class(full_path: str):
    """Dynamically import a class or function from a string path."""
    module_path, class_name = full_path.rsplit(".", 1)
    module = __import__(module_path, fromlist=[class_name])
    return getattr(module, class_name)


def task_wrapper(
    business_module: str,
    business_function: str,
    inject_map: dict = None,
    resources: dict = None,
    depends_on: list = None,
    **kwargs
) -> Any:
    ti = kwargs.get("ti")
    inject_map = inject_map or {}
    resources = resources or {}
    depends_on = depends_on or []

    injected_resources = {}

    # === Create and inject resources (with table_name + schema support) ===
    for arg_name, res_id in inject_map.items():
        if res_id in resources:
            res_cfg = resources[res_id]
            adapter_config = res_cfg.get("config", {}).copy()

            # Forward table_name and schema from the current task if present
            if "table_name" in kwargs:
                adapter_config["table_name"] = kwargs["table_name"]
            if "schema" in kwargs:
                adapter_config["schema"] = kwargs["schema"]

            AdapterClass = get_class(res_cfg["type"])
            injected_resources[arg_name] = AdapterClass(**adapter_config)

    # === Pull data from upstream task via XCom (smart extraction) ===
    data = None
    if depends_on and ti:
        upstream_task_id = depends_on[-1]
        upstream_result = ti.xcom_pull(task_ids=upstream_task_id, key="return_value")

        if isinstance(upstream_result, dict) and "data" in upstream_result:
            data = upstream_result["data"]
        else:
            data = upstream_result

    # === Build call arguments ===
    call_kwargs = {}
    if data is not None:
        call_kwargs["data"] = data

    # Forward extra parameters (rows, schema, delay_seconds, etc.)
    internal_keys = {"ti", "task_instance", "dag", "run_id", "dag_run", "params"}
    extra_kwargs = {k: v for k, v in kwargs.items() if k not in internal_keys}
    call_kwargs.update(extra_kwargs)

    # === Load and execute target function/method ===
    if "." in business_function:
        class_name, method_name = business_function.split(".", 1)
        ServiceClass = get_class(f"{business_module}.{class_name}")
        service_instance = ServiceClass(**injected_resources)
        func = getattr(service_instance, method_name)
    else:
        func = get_class(f"{business_module}.{business_function}")

    result = func(**call_kwargs)

    # Push result to XCom
    if ti:
        ti.xcom_push(key="return_value", value=result)

    return result


def create_dag_from_manifest(manifest: Dict[str, Any]) -> DAG:
    dag_id = manifest["dag_id"]
    schedule = manifest.get("schedule")

    dag = DAG(
        dag_id=dag_id,
        schedule=schedule,
        catchup=False,
        tags=["example", "test-data"],
    )

    tasks = {}

    for step in manifest.get("workflow", []):
        task_id = step["id"]
        depends_on = step.get("depends_on", [])

        # Build op_kwargs and forward all extra parameters (rows, schema, etc.)
        op_kwargs = {
            "business_module": step["business_module"],
            "business_function": step["business_function"],
            "inject_map": step.get("inject", {}),
            "resources": manifest.get("resources", {}),
            "depends_on": depends_on,
        }

        # Automatically pass extra keys defined in the task (rows, schema, etc.)
        reserved_keys = {"id", "business_module", "business_function", "inject", "depends_on"}
        for key, value in step.items():
            if key not in reserved_keys:
                op_kwargs[key] = value

        t = PythonOperator(
            task_id=task_id,
            python_callable=task_wrapper,
            op_kwargs=op_kwargs,
            dag=dag,
        )

        tasks[task_id] = t

        for upstream_id in depends_on:
            if upstream_id in tasks:
                tasks[upstream_id] >> t

    return dag