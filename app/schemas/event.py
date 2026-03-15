from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class SecurityEventCreate(BaseModel):
    ip_address: str
    event_type: str
    description: str
    severity: str = "LOW"
    country: Optional[str] = "Unknown"
    city: Optional[str] = "Unknown"

class SecurityEventResponse(BaseModel):
    id: int
    ip_address: str
    event_type: str
    description: str
    severity: str
    country: Optional[str]
    city: Optional[str]
    acknowledged: bool
    timestamp: datetime
    model_config = {"from_attributes": True}

class AlertSummary(BaseModel):
    total: int
    critical: int
    high: int
    medium: int
    low: int
    unacknowledged: int