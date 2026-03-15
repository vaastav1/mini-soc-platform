import time
from collections import defaultdict
from app.core.config import settings

failed_login_counter   = defaultdict(int)
total_event_counter    = defaultdict(int)
had_failed_login       = defaultdict(bool)
sudo_fail_counter      = defaultdict(int)
alert_cooldown_tracker = {}

def _cooldown_ok(ip: str, alert_type: str) -> bool:
    key = (ip, alert_type)
    now = time.time()
    if now - alert_cooldown_tracker.get(key, 0) > settings.alert_cooldown_seconds:
        alert_cooldown_tracker[key] = now
        return True
    return False

def detect_threats(event: dict) -> list:
    ip   = event.get("ip", "0.0.0.0")
    kind = event.get("type", "")
    alerts = []
    total_event_counter[ip] += 1

    if kind == "failed_login":
        failed_login_counter[ip] += 1
        had_failed_login[ip] = True
        if failed_login_counter[ip] >= settings.brute_force_threshold and _cooldown_ok(ip, "brute_force"):
            alerts.append({"ip": ip, "event_type": "brute_force",
                "description": f"Brute force from {ip} ({failed_login_counter[ip]} failures)",
                "severity": "HIGH"})

    elif kind == "successful_login":
        if had_failed_login[ip] and _cooldown_ok(ip, "impossible_login"):
            alerts.append({"ip": ip, "event_type": "impossible_login",
                "description": f"Successful login after failures from {ip}",
                "severity": "CRITICAL"})

    elif kind == "sudo_failure":
        sudo_fail_counter[ip] += 1
        if sudo_fail_counter[ip] >= 3 and _cooldown_ok(ip, "privilege_escalation"):
            alerts.append({"ip": ip, "event_type": "privilege_escalation",
                "description": f"Privilege escalation attempt from {ip}",
                "severity": "HIGH"})

    if total_event_counter[ip] >= settings.suspicious_ip_threshold and _cooldown_ok(ip, "suspicious_ip"):
        alerts.append({"ip": ip, "event_type": "suspicious_ip",
            "description": f"High volume from {ip} ({total_event_counter[ip]} events)",
            "severity": "MEDIUM"})

    return alerts

def reset_counters():
    failed_login_counter.clear()
    total_event_counter.clear()
    had_failed_login.clear()
    sudo_fail_counter.clear()
    alert_cooldown_tracker.clear()