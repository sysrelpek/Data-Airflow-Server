from datetime import datetime
from airflow.sdk import DAG, task
from pipelines.ml.train.model_trainer_basic.run import run_pipeline

with DAG(
    dag_id="ml_train_model",
    schedule=None,
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["ml"],
    is_paused_upon_creation=False,
) as dag:

    run_pipeline()
