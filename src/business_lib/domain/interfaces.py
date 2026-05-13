"""

"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class StoragePort(ABC):
    """
    The Port (Interface) for all storage operations.
    Updated to support the 'verify' step in the ingest pipeline.
    """

    @abstractmethod
    def save(self, entity_id: str, data: Dict[str, Any]) -> None:
        """Saves tmp_db and creates a Transactional Outbox entry."""
        pass

    @abstractmethod
    def get_by_id(self, entity_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves a single record by its ID."""
        pass

    @abstractmethod
    def count_all(self) -> int:
        """
        New: Returns the total number of records.
        Used by 'verify_storage' to check if the ingestion count is correct.
        """
        pass

    @abstractmethod
    def get_pending_messages(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Retrieves unsynced messages from the local Outbox."""
        pass

    @abstractmethod
    def update_outbox_status(self, message_id: int, status: str) -> None:
        """Updates the status of an outbox message (e.g., to 'SENT')."""
        pass

    @abstractmethod
    def store_data(self, data: Dict[str, Any]) -> None:
        """Saves data to the storage system."""
        pass



class CachePort(ABC):
    """Gränssnitt för snabbmeddelanden och cache (Redis/In-memory)"""

    @abstractmethod
    def set(self, key: str, value: Any, expire: int = 3600) -> None:
        pass

    @abstractmethod
    def get(self, key: str) -> Any:
        pass


class EventPort(ABC):
    """Gränssnitt för att skicka händelser till andra system."""

    @abstractmethod
    def emit(self, event_name: str, payload: Dict[str, Any]) -> None:
        pass



# Define a Logging Port (Interface) in the core so the business logic
# can log events without knowing how they are stored,
# and then create Adapters to send those logs to Airflow
class LoggingPort(ABC):
    @abstractmethod
    def info(self, message: str):
        pass

    @abstractmethod
    def error(self, message: str, error_details: Optional[Exception] = None):
        pass

    @abstractmethod
    def verify(self, action: str, status: bool):
        """Specifically for the 'verify' steps in your YAML."""
        pass
