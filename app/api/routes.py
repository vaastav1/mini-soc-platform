from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.security_event import SecurityEvent
from app.schemas.event import SecurityEventResponse, AlertSummary
from app.ingestor.log_ingestor import process_log_file_once
from app.detection.engine import reset_counters

router = APIRouter(prefix="/api", tags=["SOC API"])

@router.get("/events", response_model=list[SecurityEventResponse])
def list_events(
    event_type: Optional[str] = None, severity: Optional[str] = None,
    ip_address: Optional[str] = None, acknowledged: Optional[bool] = None,
    limit: int = 200, offset: int = 0, db: Session = Depends(get_db),
):
    q = db.query(SecurityEvent)
    if event_type:   q = q.filter(SecurityEvent.event_type == event_type)
    if severity:     q = q.filter(SecurityEvent.severity == severity)
    if ip_address:   q = q.filter(SecurityEvent.ip_address == ip_address)
    if acknowledged is not None: q = q.filter(SecurityEvent.acknowledged == acknowledged)
    return q.order_by(SecurityEvent.timestamp.desc()).offset(offset).limit(limit).all()

@router.get("/events/{event_id}", response_model=SecurityEventResponse)
def get_event(event_id: int, db: Session = Depends(get_db)):
    ev = db.query(SecurityEvent).filter(SecurityEvent.id == event_id).first()
    if not ev: raise HTTPException(status_code=404, detail="Event not found")
    return ev

@router.post("/events/{event_id}/ack", response_model=SecurityEventResponse)
def ack_event(event_id: int, db: Session = Depends(get_db)):
    ev = db.query(SecurityEvent).filter(SecurityEvent.id == event_id).first()
    if not ev: raise HTTPException(status_code=404, detail="Event not found")
    ev.acknowledged = True
    db.commit()
    db.refresh(ev)
    return ev

@router.get("/stats", response_model=AlertSummary)
def get_stats(db: Session = Depends(get_db)):
    all_events = db.query(SecurityEvent).all()
    return AlertSummary(
        total=len(all_events),
        critical=sum(1 for e in all_events if e.severity == "CRITICAL"),
        high=sum(1 for e in all_events if e.severity == "HIGH"),
        medium=sum(1 for e in all_events if e.severity == "MEDIUM"),
        low=sum(1 for e in all_events if e.severity == "LOW"),
        unacknowledged=sum(1 for e in all_events if not e.acknowledged),
    )

@router.post("/run-detection")
def run_detection():
    return process_log_file_once()

@router.post("/reset-counters")
def reset():
    reset_counters()
    return {"status": "counters reset"}