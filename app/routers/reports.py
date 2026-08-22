from fastapi import APIRouter, Depends
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.integration_log import IntegrationLog
from app.services.report_scheduler import generate_daily_report

router = APIRouter(prefix="/reports", tags=["reports"])


@router.post("/daily/run")
def run_daily_report_now():
    """Zamanlanmis raporu beklemeden manuel tetikler."""
    return generate_daily_report()


@router.get("/daily/latest")
def latest_daily_report(db: Session = Depends(get_db)):
    entry = (
        db.query(IntegrationLog)
        .filter(IntegrationLog.source == "reports.daily")
        .order_by(desc(IntegrationLog.created_at))
        .first()
    )
    if not entry:
        return {"message": "Henuz rapor uretilmedi"}
    return {"created_at": entry.created_at, "message": entry.message}
