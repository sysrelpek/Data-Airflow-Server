import requests


def relay_outbox_messages(storage_adapter, remote_endpoint):
    """
    1. Fetches PENDING messages from local DB.
    2. Sends them to the Central API/Redis.
    3. Updates status to SENT or FAILED.
    """
    messages = storage_adapter.get_pending_messages(limit=50)

    for msg in messages:
        try:
            # Update status to PROCESSING to avoid race conditions
            storage_adapter.update_outbox_status(msg['id'], 'PROCESSING')

            # The actual network call
            response = requests.post(remote_endpoint, json=msg['payload'], timeout=10)

            if response.status_code == 200:
                storage_adapter.update_outbox_status(msg['id'], 'SENT')
            else:
                storage_adapter.update_outbox_status(msg['id'], 'FAILED')

        except Exception as e:
            # If network is down, we revert to PENDING and stop the loop
            storage_adapter.update_outbox_status(msg['id'], 'PENDING')
            print(f"Network down, stopping relay: {e}")
            break
