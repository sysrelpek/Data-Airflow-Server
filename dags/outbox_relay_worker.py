"""
This Airflow DAG acts as the "Courier" that syncs the
 local outbox to the central system.
"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
from business_lib.core.config import settings
from business_lib.infrastructure.storage.postgres_adapter import PostgresAdapter


def sync_outbox_to_central():
    # 1. Connect to local storage (The Fallback/Outbox source)
    storage = PostgresAdapter(settings.DATABASE_URL)

    # 2. Get pending messages
    messages = storage.get_pending_messages(limit=20)

    for msg in messages:
        try:
            # 3. Attempt to push to Central API
            response = requests.post(
                settings.CENTRAL_API_URL,
                json=msg['payload'],
                timeout=10
            )

            if response.status_code == 200:
                # 4. Mark as sent in local DB
                storage.update_outbox_status(msg['id'], 'SENT')
                print(f"Successfully synced message {msg['id']}")

        except Exception as e:
            print(f"Sync failed: {e}. Will retry in next run.")
            break  # Stop loop if network is down


with DAG(
        'outbox_relay_worker',
        schedule_interval='*/5 * * * *',  # Runs every 5 minutes
        start_date=datetime(2023, 1, 1),
        catchup=False
) as dag:
    sync_task = PythonOperator(
        task_id='relay_sync',
        python_callable=sync_outbox_to_central
    )
