import json
import uuid
from typing import Any, Dict, List, Optional

import psycopg2

from business_lib.domain.interfaces import StoragePort


class PostgresAdapter(StoragePort):
    """
    PostgreSQL adapter with dynamic schema support.
    """

    def __init__(
        self,
        connection_string: str,
        table_name: Optional[str] = None,
        schema: Optional[Dict[str, str]] = None
    ):
        self.conn = psycopg2.connect(connection_string)
        self.table_name = table_name or "default_table"
        self.schema = schema or {}

        if self.schema:
            self._create_table_from_schema()

    def _map_type_to_postgres(self, dtype: str) -> str:
        mapping = {
            "integer": "INTEGER",
            "int": "INTEGER",
            "float": "DOUBLE PRECISION",
            "string": "TEXT",
            "text": "TEXT",
            "boolean": "BOOLEAN",
            "bool": "BOOLEAN",
            "timestamp": "TIMESTAMP",
            "datetime": "TIMESTAMP",
            "uuid": "UUID",
        }
        return mapping.get(dtype.lower(), "TEXT")

    def _create_table_from_schema(self):
        if not self.schema:
            return

        columns = [f"{col} {self._map_type_to_postgres(dtype)}" for col, dtype in self.schema.items()]

        create_sql = f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                {', '.join(columns)},
                PRIMARY KEY (id)
            )
        """

        with self.conn.cursor() as cur:
            cur.execute(create_sql)
        self.conn.commit()

    def insert_record(self, data: dict) -> None:
        if not data or "id" not in data:
            raise ValueError("Data must contain an 'id' field")

        columns = list(data.keys())
        values = [str(v) if isinstance(v, uuid.UUID) else v for v in data.values()]

        placeholders = ", ".join(["%s"] * len(columns))
        columns_str = ", ".join(columns)
        update_set = ", ".join([f"{col} = EXCLUDED.{col}" for col in columns])

        sql = f"""
            INSERT INTO {self.table_name} ({columns_str})
            VALUES ({placeholders})
            ON CONFLICT (id) DO UPDATE SET {update_set}
        """

        with self.conn.cursor() as cur:
            cur.execute(sql, values)
        self.conn.commit()

    def insert_record_list(self, data: List[Dict[str, Any]]) -> None:
        for item in data:
            if isinstance(item, dict):
                self.insert_record(item)