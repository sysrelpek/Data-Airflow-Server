"""
Using Pydantic, we ensure that tmp_db is valid before it touches the database or the outbox.
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class FeatureRecord(BaseModel):
    """Schema for the ingested feature tmp_db."""
    id: str
    score: float = Field(..., ge=0.0, le=1.0)
    status: str = "active"
    processed_at: datetime = Field(default_factory=datetime.now)

class OutboxMessage(BaseModel):
    """Schema for the Transactional Outbox messages."""
    id: Optional[int] = None
    event_type: str
    payload: dict
    status: str = "PENDING"
    created_at: datetime = Field(default_factory=datetime.now)
