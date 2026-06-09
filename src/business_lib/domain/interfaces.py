from abc import ABC, abstractmethod
from typing import Any, Dict, List


class StoragePort(ABC):
    """
    Abstract base class for storage adapters.

    This interface defines the minimal set of methods
    required by the current system (GenerateTestDataService, LoadService, etc.).
    """

    @abstractmethod
    def insert_record(self, data: dict) -> None:
        """
        Insert or update a single record.
        The record must contain an 'id' field which is used as the primary key.
        """
        pass

    @abstractmethod
    def insert_record_list(self, data: List[Dict[str, Any]]) -> None:
        """
        Bulk insert multiple records.
        Each record in the list must contain an 'id' field.
        """
        pass