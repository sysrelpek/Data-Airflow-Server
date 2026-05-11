import importlib
from airflow import DAG
from airflow.operators.python import PythonOperator

# Enkel funktion som Airflow-tasken faktiskt kör
def task_wrapper(module_path, function_name, **kwargs):
    module = importlib.import_module(module_path)
    func = getattr(module, function_name)
    return func(**kwargs)

# Här loopar du din JSON-manifest och skapar PythonOperators
# som använder task_wrapper för att anropa ditt bibliotek.
