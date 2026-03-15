from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from app.db.database import Base

class SecurityEvent(Base):
    __tablename__ = "security_events"
    id           = Column(Integer, primary_key=True, index=True)
    ip_address   = Column(String, index=True, nullable=False)
    event_type   = Column(String, index=True, nullable=False)
    description  = Column(String, nullable=False)
    severity     = Column(String, default="LOW")
    country      = Column(String, default="Unknown")
    city         = Column(String, default="Unknown")
    acknowledged = Column(Boolean, default=False)
    timestamp    = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id, "ip_address": self.ip_address,
            "event_type": self.event_type, "description": self.description,
            "severity": self.severity, "country": self.country, "city": self.city,
            "acknowledged": self.acknowledged,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
        }