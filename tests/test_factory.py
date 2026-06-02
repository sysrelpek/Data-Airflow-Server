# =============================================================================
# tests/test_factory.py
# Tests for the dynamic DAG factory (core business logic)
# =============================================================================

from business_lib.core.dag_factory import create_dag_from_manifest


def test_create_dag_from_simple_manifest():
    """Test that a minimal manifest creates a valid Airflow DAG."""
    manifest_data = {
        "dag_id": "test_simple_dag",
        "schedule": "@daily",
        "workflow": [
            {
                "id": "extract_data",
                "business_module": "business_lib.services.extract_service",
                "business_function": "extract_data",
                "depends_on": []
            }
        ],
        "resources": {}
    }

    dag = create_dag_from_manifest(manifest_data)

    assert dag.dag_id == "test_simple_dag"
    assert len(dag.tasks) == 1
    assert dag.tasks[0].task_id == "extract_data"


def test_manifest_with_dependencies():
    """Test that task dependencies are correctly wired."""
    manifest_data = {
        "dag_id": "test_dep_dag",
        "schedule": "@hourly",
        "workflow": [
            {
                "id": "extract",
                "business_module": "business_lib.services.extract_service",
                "business_function": "extract_data",
                "depends_on": []
            },
            {
                "id": "transform",
                "business_module": "business_lib.services.transform_service",
                "business_function": "transform_data",
                "depends_on": ["extract"]
            }
        ],
        "resources": {}
    }

    dag = create_dag_from_manifest(manifest_data)

    assert len(dag.tasks) == 2
    transform_task = next(t for t in dag.tasks if t.task_id == "transform")
    assert len(transform_task.upstream_task_ids) == 1
    assert "extract" in transform_task.upstream_task_ids