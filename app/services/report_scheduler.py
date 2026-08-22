"""Not: 'Hergun sistem raporlamasi gun sonu otomatik.' APScheduler ile her gun
sistem ozetini olusturup IntegrationLog'a yazan basit bir zamanlayici."""
from __future__ import annotations

import logging

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from app.database import SessionLocal
from app.models.bank import BankTransaction
from app.models.integration_log import IntegrationLog
from app.models.inventory import InventoryItem
from app.models.investor import Investor
from app.models.logistics import LogisticsFile

logger = logging.getLogger("crmschaller.reports")

_scheduler: BackgroundScheduler | None = None


def generate_daily_report() -> dict:
    db = SessionLocal()
    try:
        summary = {
            "investors": db.query(Investor).count(),
            "inventory_items": db.query(InventoryItem).count(),
            "logistics_files": db.query(LogisticsFile).count(),
            "bank_transactions": db.query(BankTransaction).count(),
        }
        log_entry = IntegrationLog(
            source="reports.daily",
            level="INFO",
            message=f"Gunluk sistem raporu: {summary}",
        )
        db.add(log_entry)
        db.commit()
        logger.info("Gunluk sistem raporu olusturuldu: %s", summary)
        return summary
    finally:
        db.close()


def start_scheduler(hour: int = 23, minute: int = 55) -> BackgroundScheduler:
    """Uygulama basladiginda cagirilir; her gun belirtilen saatte rapor uretir."""
    global _scheduler
    if _scheduler is not None:
        return _scheduler

    _scheduler = BackgroundScheduler(timezone="Europe/Istanbul")
    _scheduler.add_job(
        generate_daily_report,
        trigger=CronTrigger(hour=hour, minute=minute),
        id="daily_system_report",
        replace_existing=True,
    )
    _scheduler.start()
    return _scheduler


def stop_scheduler() -> None:
    global _scheduler
    if _scheduler is not None:
        _scheduler.shutdown(wait=False)
        _scheduler = None
