from abc import ABC, abstractmethod
from typing import Any, Dict, List


class StoragePort(ABC):
    """
    Clean storage interface used by the system.
    Only contains the methods we actually use.
    """

    @abstractmethod
    def insert_record(self, data: dict) -> None:
        """Insert or update a single record. Must contain an 'id' field."""
        pass

    @abstractmethod
    def insert_record_list(self, data: List[Dict[str, Any]]) -> None:
        """Bulk insert multiple records. Each record must contain an 'id' field."""
        pass