import json
import uuid
from typing import Any, Dict, List, Optional

import psycopg2
from psycopg2.extras import RealDictCursor

from business_lib.domain.interfaces import StoragePort


class PostgresAdapter(StoragePort):
    """
    PostgreSQL storage adapter with dynamic table creation from schema.
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
        """Convert simple schema types to PostgreSQL column types."""
        dtype = dtype.lower()
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
        return mapping.get(dtype, "TEXT")

    def _create_table_from_schema(self):
        """Create the table dynamically based on the schema from YAML."""
        if not self.schema:
            return

        columns = []
        for column_name, data_type in self.schema.items():
            pg_type = self._map_type_to_postgres(data_type)
            columns.append(f"{column_name} {pg_type}")

        create_sql = f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                {', '.join(columns)}
            )
        """

        with self.conn.cursor() as cur:
            cur.execute(create_sql)
        self.conn.commit()

    # ============================================================
    # StoragePort Implementation (no entity_id)
    # ============================================================

    def insert_record(self, data: dict) -> None:
        """Insert or update a single record. 'id' must be inside the dict."""
        if not data or "id" not in data:
            raise ValueError("Data must contain an 'id' field")

        columns = list(data.keys())
        values = []
        for v in data.values():
            if isinstance(v, uuid.UUID):
                values.append(str(v))
            else:
                values.append(v)

        placeholders = ", ".join(["%s"] * len(columns))
        columns_str = ", ".join(columns)

        sql = f"""
            INSERT INTO {self.table_name} ({columns_str})
            VALUES ({placeholders})
            ON CONFLICT (id) DO UPDATE SET {', '.join([f"{col} = EXCLUDED.{col}" for col in columns])}
        """

        with self.conn.cursor() as cur:
            cur.execute(sql, values)
        self.conn.commit()

    def insert_record_list(self, data: List[Dict[str, Any]]) -> None:
        """Bulk insert multiple records."""
        if not data:
            return

        for item in data:
            if isinstance(item, dict):
                self.insert_record(item)