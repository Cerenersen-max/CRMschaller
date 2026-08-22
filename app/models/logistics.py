"""Not: 'Lojistik dosyasi olusturuldu, bankalara mail iletildi en uygun gorusme yapilacak'."""
import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class LogisticsFileStatus(str, enum.Enum):
    created = "created"
    mail_sent = "mail_sent"                # bankalara mail iletildi
    meeting_scheduled = "meeting_scheduled"  # gorusme ayarlandi
    completed = "completed"


class LogisticsFile(Base):
    __tablename__ = "logistics_files"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    status: Mapped[LogisticsFileStatus] = mapped_column(
        Enum(LogisticsFileStatus), default=LogisticsFileStatus.created
    )
    bank_contacts: Mapped[str] = mapped_column(Text, default="")  # mail gonderilen banka listesi
    notes: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"<LogisticsFile {self.title} ({self.status})>"
