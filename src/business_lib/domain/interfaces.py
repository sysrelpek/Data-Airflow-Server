from abc import ABC, abstractmethod
from typing import Any, Dict, List


class StoragePort(ABC):
    """
    Storage interface used by the system.
    """

    @abstractmethod
    def insert_record(self, data: dict) -> None:
        """Insert or update a single record."""
        pass

    @abstractmethod
    def insert_record_list(self, data: List[Dict[str, Any]]) -> None:
        """Bulk insert multiple records."""
        pass

    @abstractmethod
    def delete_data(self) -> int:
        """
        Delete test data.
        Returns the number of deleted records.
        """
        pass