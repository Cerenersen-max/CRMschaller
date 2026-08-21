"""Not: 'Gozlem & Log Katmani'. MCP sunucusundaki her arac cagrisini hem Python
logging (syslog'a yonlendirilebilir) hem de veritabanindaki IntegrationLog
tablosuna yazar."""
from __future__ import annotations

import logging
import logging.handlers

from app.config import get_settings
from app.database import SessionLocal
from app.models.integration_log import IntegrationLog

logger = logging.getLogger("crmschaller.mcp")
_handler_attached = False


def _ensure_syslog_handler() -> None:
    """video+voice+light+text notlarindaki 'syslog -> sistem gunlugu' katmanina
    karsilik gelir. SYSLOG_HOST/PORT erisilebilir degilse sessizce yerel
    logging'e devam eder."""
    global _handler_attached
    if _handler_attached:
        return
    settings = get_settings()
    try:
        handler = logging.handlers.SysLogHandler(address=(settings.syslog_host, settings.syslog_port))
        logger.addHandler(handler)
    except OSError:
        # Syslog erisilemiyorsa (ör. yerel gelistirme ortami) sessizce devam et.
        pass
    _handler_attached = True


class ObservabilityLayer:
    """MCP katmanlarinin ortak gozlem/log arayuzu."""

    def __init__(self) -> None:
        _ensure_syslog_handler()

    def log(self, source: str, message: str, level: str = "INFO") -> None:
        logger.log(getattr(logging, level, logging.INFO), "[%s] %s", source, message)
        db = SessionLocal()
        try:
            db.add(IntegrationLog(source=source, level=level, message=message))
            db.commit()
        finally:
            db.close()


observability = ObservabilityLayer()
