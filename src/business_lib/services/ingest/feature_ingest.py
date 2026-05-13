import pandas as pd
from business_lib.domain.interfaces import StoragePort
from business_lib.domain.interfaces import LoggingPort
from typing import Optional


def collect_data(file_path: str):
    """Airflow skickar in sökvägen till CSV-filen."""
    df = pd.read_csv(file_path)
    return df.to_dict(orient="records")


def clean_and_transform(data):
    df = pd.DataFrame(data)
    # Cleaning: Ta bort rader med saknade värden
    df = df.dropna()
    # Transformation: Normalisera 'score' kolumn
    if 'score' in df.columns:
        df['score'] = df['score'] / 100
    return df.to_dict(orient="records")


def store_data(data, storage: StoragePort, logger: Optional[LoggingPort] = None):
    """Store data with optional logger (None-safe for local tests)."""
    try:
        for record in data:
            storage.save(entity_id=str(record.get('id')), data=record)

        if logger:
            logger.info(f"Successfully stored {len(data)} records.")
        return len(data)

    except Exception as e:
        if logger:
            logger.error("Failed to store data", error_details=e)
        raise


def verify_storage(expected_count, storage: StoragePort, logger: Optional[LoggingPort] = None):
    """Verify storage count with optional logger."""
    actual_count = storage.count_all()
    success = actual_count >= expected_count

    if logger:
        logger.verify(f"Storage count check (Expected: {expected_count}, Actual: {actual_count})", success)
    return success
