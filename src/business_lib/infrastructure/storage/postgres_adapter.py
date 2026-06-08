import json
from typing import Any, Dict, List, Optional

import psycopg2
from psycopg2.extras import RealDictCursor

from business_lib.domain.interfaces import StoragePort


class PostgresAdapter(StoragePort):
    """
    PostgreSQL implementation of the StoragePort interface.
    """

    def __init__(self, connection_string: str):
        self.conn = psycopg2.connect(connection_string)
        self._ensure_tables_exist()

    def _ensure_tables_exist(self):
        """Create required tables if they don't exist."""
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS storage (
                    id TEXT PRIMARY KEY,
                    tmp_db JSONB
                );

                CREATE TABLE IF NOT EXISTS outbox (
                    id SERIAL PRIMARY KEY,
                    payload JSONB,
                    status TEXT DEFAULT 'PENDING',
                    created_at TIMESTAMP DEFAULT NOW()
                );
            """)
        self.conn.commit()

    # ============================================================
    # StoragePort Implementation
    # ============================================================

    def save(self, entity_id: str, data: dict):
        """Save or update a record in the storage table and add to outbox."""
        with self.conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO storage (id, tmp_db)
                VALUES (%s, %s)
                ON CONFLICT (id) DO UPDATE SET tmp_db = EXCLUDED.tmp_db
                """,
                (entity_id, json.dumps(data))
            )
            # Also write to outbox
            cur.execute(
                "INSERT INTO outbox (payload) VALUES (%s)",
                (json.dumps(data),)
            )
        self.conn.commit()

    def get_by_id(self, entity_id: str) -> Optional[dict]:
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT tmp_db FROM storage WHERE id = %s", (entity_id,))
            result = cur.fetchone()
            return result["tmp_db"] if result else None

    def count_all(self) -> int:
        with self.conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM storage")
            result = cur.fetchone()
            return result[0] if result else 0

    def get_pending_messages(self, limit: int = 50) -> List[dict]:
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "SELECT * FROM outbox WHERE status = 'PENDING' ORDER BY id LIMIT %s",
                (limit,)
            )
            return cur.fetchall()

    def update_outbox_status(self, message_id: int, status: str) -> None:
        with self.conn.cursor() as cur:
            cur.execute(
                "UPDATE outbox SET status = %s WHERE id = %s",
                (status, message_id)
            )
        self.conn.commit()

    def store_data(self, data: List[Dict[str, Any]]) -> None:
        """
        Store multiple records. Required to satisfy the abstract StoragePort interface.
        """
        if not data:
            return

        with self.conn.cursor() as cur:
            for item in data:
                if not isinstance(item, dict):
                    continue

                entity_id = str(item.get("id", hash(str(item))))
                cur.execute(
                    """
                    INSERT INTO storage (id, tmp_db)
                    VALUES (%s, %s)
                    ON CONFLICT (id) DO UPDATE SET tmp_db = EXCLUDED.tmp_db
                    """,
                    (entity_id, json.dumps(item))
                )
        self.conn.commit()