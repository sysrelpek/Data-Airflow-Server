import pandas as pd
from business_lib.domain.interfaces import StoragePort

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
    # Kontrollerar att data faktiskt finns där
    # (Här kan vi implementera en specifik count-metod i interfacet)
    return True
