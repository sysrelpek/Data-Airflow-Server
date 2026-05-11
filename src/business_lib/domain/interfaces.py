from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class StoragePort(ABC):
    """Port för permanent lagring. Implementeras av t.ex. Postgres eller FileAdapter."""

    @abstractmethod
    def save(self, entity_id: str, data: Dict[str, Any]) -> None:
        """Sparar data och skapar samtidigt ett event i Outbox-tabellen."""
        pass

    @abstractmethod
    def get_by_id(self, entity_id: str) -> Optional[Dict[str, Any]]:
        """Hämtar data för ett specifikt ID."""
        pass

    @abstractmethod
    def get_pending_messages(self, limit: int = 50) -> list:
        """Hämtar osynkade meddelanden från Outbox (används av Relay Worker)."""
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
