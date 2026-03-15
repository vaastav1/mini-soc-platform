# detection_engine.py
# Applies detection rules to parsed logs

from collections import defaultdict

failed_login_tracker = defaultdict(int)

BRUTE_FORCE_THRESHOLD = 5

def detect_threat(event):

    ip = event["ip"]

    if event["event_type"] == "failed_login":

        failed_login_tracker[ip] += 1

        if failed_login_tracker[ip] >= BRUTE_FORCE_THRESHOLD:

            return {
                "type": "Brute Force Attack",
                "ip": ip,
                "description": f"Multiple failed logins from {ip}"
            }

    return None