"""MCP 'Gozlem & Log Katmani' notu icin basit entegrasyon log tablosu."""
from datetime import datetime

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class IntegrationLog(Base):
    __tablename__ = "integration_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    source: Mapped[str] = mapped_column(String(100))   # ornegin "mcp.decision_layer", "bank.nordea"
    level: Mapped[str] = mapped_column(String(16), default="INFO")
    message: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:  # pragma: no cover
        return f"<IntegrationLog {self.source} {self.level}>"
