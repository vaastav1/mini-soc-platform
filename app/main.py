from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.logging import setup_logging
from app.db.database import init_db, get_db
from app.ingestor.log_ingestor import start_monitor, stop_monitor
from app.api.routes import router as api_router
from app.models.security_event import SecurityEvent

setup_logging("DEBUG" if settings.debug else "INFO")

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    start_monitor()
    yield
    stop_monitor()

app = FastAPI(title=settings.app_name, lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
app.include_router(api_router)

@app.get("/")
async def dashboard(request: Request):
    db: Session = next(get_db())
    try:
        events = db.query(SecurityEvent).order_by(SecurityEvent.timestamp.desc()).limit(200).all()
        all_events = db.query(SecurityEvent).all()
        stats = {
            "total":          len(all_events),
            "critical":       sum(1 for e in all_events if e.severity == "CRITICAL"),
            "high":           sum(1 for e in all_events if e.severity == "HIGH"),
            "medium":         sum(1 for e in all_events if e.severity == "MEDIUM"),
            "low":            sum(1 for e in all_events if e.severity == "LOW"),
            "unacknowledged": sum(1 for e in all_events if not e.acknowledged),
        }
    finally:
        db.close()
    return templates.TemplateResponse("dashboard.html", {
        "request": request, "events": events, "stats": stats, "app_name": settings.app_name,
    })