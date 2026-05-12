import psycopg2
from psycopg2.extras import RealDictCursor
import json
from business_lib.domain.interfaces import StoragePort

class PostgresAdapter(StoragePort):
    def __init__(self, connection_string: str):
        self.conn = psycopg2.connect(connection_string)
        self._create_tables()

    def _create_tables(self):
        """Säkerställer att tabeller finns (Next-Gen Auto-setup)."""
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS storage (id TEXT PRIMARY KEY, data JSONB);
                CREATE TABLE IF NOT EXISTS outbox (
                    id SERIAL PRIMARY KEY, 
                    payload JSONB, 
                    status TEXT DEFAULT 'PENDING'
                );
            """)
        self.conn.commit()

    def save(self, entity_id: str, data: dict):
        with self.conn.cursor() as cur:
            # Spara data
            cur.execute(
                "INSERT INTO storage (id, data) VALUES (%s, %s) ON CONFLICT (id) DO UPDATE SET data = EXCLUDED.data",
                (entity_id, json.dumps(data))
            )
            # Spara till Outbox (Samma transaktion!)
            cur.execute("INSERT INTO outbox (payload) VALUES (%s)", (json.dumps(data),))
        self.conn.commit()

    def get_by_id(self, entity_id: str):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT data FROM storage WHERE id = %s", (entity_id,))
            res = cur.fetchone()
            return res['data'] if res else None

    def get_pending_messages(self, limit=50):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM outbox WHERE status = 'PENDING' LIMIT %s", (limit,))
            return cur.fetchall()

    def count_all(self) -> int:
        """Returns the total number of records in storage."""
        with self.conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM storage")
            res = cur.fetchone()
            return res[0] if res else 0

    def update_outbox_status(self, message_id: int, status: str) -> None:
        """Updates the status of an outbox message."""
        with self.conn.cursor() as cur:
            cur.execute(
                "UPDATE outbox SET status = %s WHERE id = %s",
                (status, message_id)
            )
        self.conn.commit()
