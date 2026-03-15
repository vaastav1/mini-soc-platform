import threading
import time
import logging
from app.core.config import settings
from app.ingestor.log_parser import parse_log_line
from app.detection.engine import detect_threats, reset_counters
from app.ingestor.alerts import save_alert
from app.db.database import SessionLocal

logger = logging.getLogger(__name__)
_stop_event = threading.Event()
_thread = None

def _tail_log_file():
    logger.info(f"Monitoring: {settings.log_file_path}")
    try:
        with open(settings.log_file_path, "r") as f:
            f.seek(0, 2)
            while not _stop_event.is_set():
                line = f.readline()
                if line:
                    parsed = parse_log_line(line)
                    if parsed:
                        for alert in detect_threats(parsed):
                            db = SessionLocal()
                            try:
                                save_alert(db, alert)
                            finally:
                                db.close()
                else:
                    time.sleep(settings.log_poll_interval)
    except FileNotFoundError:
        logger.error(f"Log file not found: {settings.log_file_path}")

def process_log_file_once() -> dict:
    reset_counters()
    count = 0
    try:
        with open(settings.log_file_path, "r") as f:
            for line in f:
                parsed = parse_log_line(line)
                if parsed:
                    for alert in detect_threats(parsed):
                        db = SessionLocal()
                        try:
                            save_alert(db, alert)
                            count += 1
                        finally:
                            db.close()
    except FileNotFoundError:
        return {"status": "error", "message": f"File not found: {settings.log_file_path}"}
    return {"status": "completed", "alerts_created": count, "file": settings.log_file_path}

def start_monitor():
    global _thread
    _stop_event.clear()
    _thread = threading.Thread(target=_tail_log_file, daemon=True)
    _thread.start()

def stop_monitor():
    _stop_event.set()