from datetime import datetime
from airflow.sdk import DAG
from airflow.providers.standard.operators.trigger_dagrun import TriggerDagRunOperator

with DAG(
    dag_id="ml_pipeline_start",
    schedule=None,
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["ml", "orchestrator"],
    is_paused_upon_creation=False,
) as dag:

    # Create trigger tasks and chain them sequentially

    trigger_ml_ingest_features = TriggerDagRunOperator(
        task_id="trigger_ml_ingest_features",
        trigger_dag_id="ml_ingest_features",
        wait_for_completion=True,
        reset_dag_run=True,
    )

    trigger_ml_train_model = TriggerDagRunOperator(
        task_id="trigger_ml_train_model",
        trigger_dag_id="ml_train_model",
        wait_for_completion=True,
        reset_dag_run=True,
    )

    trigger_ml_evaluate_model = TriggerDagRunOperator(
        task_id="trigger_ml_evaluate_model",
        trigger_dag_id="ml_evaluate_model",
        wait_for_completion=True,
        reset_dag_run=True,
    )

    trigger_ml_deploy_model = TriggerDagRunOperator(
        task_id="trigger_ml_deploy_model",
        trigger_dag_id="ml_deploy_model",
        wait_for_completion=True,
        reset_dag_run=True,
    )

    trigger_ml_batch_predict = TriggerDagRunOperator(
        task_id="trigger_ml_batch_predict",
        trigger_dag_id="ml_batch_predict",
        wait_for_completion=True,
        reset_dag_run=True,
    )

    # Enforce sequential execution
    trigger_ml_ingest_features >> trigger_ml_train_model >> trigger_ml_evaluate_model >> trigger_ml_deploy_model >> trigger_ml_batch_predict

