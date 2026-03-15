# models.py
# Defines database tables

from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from .db.database import Base

class SecurityEvent(Base):

    __tablename__ = "security_events"

    id = Column(Integer, primary_key=True, index=True)

    ip_address = Column(String)

    event_type = Column(String)

    description = Column(String)

    timestamp = Column(DateTime, default=datetime.utcnow)