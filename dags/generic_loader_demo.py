# dags/generic_loader.py
import json
from airflow import DAG
from airflow.operators.python import PythonOperator

with open("dags/manifests/onboarding.json", "r") as f:
    config = json.load(f)

with DAG(dag_id=config["dag_id"], ...) as dag:
    for task_cfg in config["workflow"]:
        PythonOperator(
            task_id=task_cfg["id"],
            python_callable=... # Uses the importlib logic we discussed earlier
        )
