import pandas as pd
from business_lib.domain.interfaces import StoragePort
from business_lib.domain.interfaces import LoggingPort


def collect_data(file_path: str):
    # Airflow skickar in sökvägen till CSV-filen
    df = pd.read_csv(file_path)
    return df.to_dict(orient="records")

def clean_and_transform(data):
    df = pd.DataFrame(data)
    # Cleaning: Ta bort rader med saknade värden
    df = df.dropna()
    # Transformation: Normalisera 'score' kolumn (exempel)
    if 'score' in df.columns:
        df['score'] = df['score'] / 100
    return df.to_dict(orient="records")

def store_data(data, storage: StoragePort):
    # Sparar till Postgres via adaptern
    for record in data:
        storage.save(entity_id=str(record.get('id')), data=record)
    return len(data)

def verify_storage(expected_count, storage: StoragePort):
    actual_count = storage.count_all()
    return actual_count >= expected_count

def store_data(data, storage: StoragePort, logger: LoggingPort):
    try:
        for record in data:
            storage.save(entity_id=str(record.get('id')), data=record)

        logger.info(f"Successfully stored {len(data)} records.")
        return len(data)
    except Exception as e:
        logger.error("Failed to store data", error_details=e)
        raise

def verify_storage(expected_count, storage: StoragePort, logger: LoggingPort):
    actual_count = storage.count_all()
    success = actual_count >= expected_count
    logger.verify(f"Storage count check (Expected: {expected_count}, Actual: {actual_count})", success)
    return success
