from app.models.security_event import SecurityEvent
from app.detection.geoip import enrich_ip

def save_alert(db, alert: dict) -> SecurityEvent:
    geo = enrich_ip(alert["ip"])
    ev = SecurityEvent(
        ip_address=alert["ip"], event_type=alert["event_type"],
        description=alert["description"], severity=alert["severity"],
        country=geo["country"], city=geo["city"],
    )
    db.add(ev)
    db.commit()
    db.refresh(ev)
    return ev