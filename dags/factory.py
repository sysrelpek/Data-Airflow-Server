from pathlib import Path
from datetime import datetime
import yaml

from airflow.sdk import DAG
from airflow.providers.standard.operators.trigger_dagrun import TriggerDagRunOperator

def build_all_dags():
    """Generate real Airflow DAG files from pipelines/ml/ml_pipelines.yaml"""
    config_path = Path("pipelines/ml/ml_pipelines.yaml")
    config = yaml.safe_load(config_path.read_text())

    pipelines = config["ml_pipelines"]

    for pipeline in pipelines:
        dag_id = pipeline["dag_id"]
        dag_file = Path(f"dags/ml/{dag_id}.py")
        dag_file.parent.mkdir(parents=True, exist_ok=True)

        if pipeline.get("type") == "orchestrator":
            # === Master Orchestrator - sequential triggering ===
            content = f'''from datetime import datetime
from airflow.sdk import DAG
from airflow.providers.standard.operators.trigger_dagrun import TriggerDagRunOperator

with DAG(
    dag_id="{dag_id}",
    schedule=None,
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["ml", "orchestrator"],
    is_paused_upon_creation=False,
) as dag:

    # Create trigger tasks and chain them sequentially
'''

            # Build list of trigger tasks
            trigger_tasks = []
            for p in pipelines[1:]:   # skip the orchestrator itself
                trigger_id = f"trigger_{p['dag_id']}"
                content += f'''
    {trigger_id} = TriggerDagRunOperator(
        task_id="{trigger_id}",
        trigger_dag_id="{p["dag_id"]}",
        wait_for_completion=True,
        reset_dag_run=True,
    )
'''
                trigger_tasks.append(trigger_id)

            # Chain them: trigger1 >> trigger2 >> trigger3 ...
            if trigger_tasks:
                chain = " >> ".join(trigger_tasks)
                content += f'''
    # Enforce sequential execution
    {chain}
'''

            content += "\n"
            dag_file.write_text(content)
            print(f"   Generated orchestrator → {dag_file}")

        else:
            # === Normal ML pipeline ===
            content = f'''from datetime import datetime
from airflow.sdk import DAG, task
from pipelines.ml.{pipeline["module"]}.run import run_pipeline

with DAG(
    dag_id="{dag_id}",
    schedule={repr(pipeline.get("schedule"))},
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["ml"],
    is_paused_upon_creation=False,
) as dag:

    run_pipeline()
'''
            dag_file.write_text(content)
            print(f"   Generated → {dag_file}")

if __name__ == "__main__":
    build_all_dags()