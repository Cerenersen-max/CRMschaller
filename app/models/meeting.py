"""Not: 'GUCA: Pazartesi- 24.Agustos.26 | 10:00 - haftalik ... veri tabani
mimarisinin ilerleyerek tam yaklasimi gerceklestir. website Design gelistirme
odna 11:00. AI website Generator uygulamasi incelyelim 20 dk.'

Haftalik tekrarlanan ekip toplantilarinin gundemini (ajanda maddeleri ve
saatleri) takip eden basit bir model."""
import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class MeetingCadence(str, enum.Enum):
    once = "once"
    weekly = "weekly"


class PartnerMeeting(Base):
    """Ornegin 'GUCA' haftalik ekip toplantisi: veri tabani mimarisi ilerleme
    kontrolu, website tasarim gelistirme, AI website generator incelemesi gibi
    ajanda maddelerini tutar."""

    __tablename__ = "partner_meetings"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))  # "GUCA" gibi
    cadence: Mapped[MeetingCadence] = mapped_column(Enum(MeetingCadence), default=MeetingCadence.weekly)
    day_of_week: Mapped[str] = mapped_column(String(20), default="")  # "Monday" / "Pazartesi"
    time_of_day: Mapped[str] = mapped_column(String(10), default="")  # "10:00"
    agenda: Mapped[str] = mapped_column(Text, default="")
    next_run_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    def __repr__(self) -> str:  # pragma: no cover
        return f"<PartnerMeeting {self.title} ({self.cadence})>"
