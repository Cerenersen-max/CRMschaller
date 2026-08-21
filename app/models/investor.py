"""Not: 'Partner - Ore Chase', 'Techstars streci yapildi fizda inceleme ile devam edecek',
KWORKS, Turk Telekom Ventures, Sabanci gibi yatirimci/partner takibi icin model."""
import enum

from sqlalchemy import Enum, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class InvestorStage(str, enum.Enum):
    lead = "lead"                    # ilk temas
    due_diligence = "due_diligence"  # inceleme / durum tespiti asamasi
    term_sheet = "term_sheet"        # sartlar belgelenecek / bekleniyor
    closed = "closed"                # anlasma tamamlandi
    passed = "passed"                # goruskme bitti, olumsuz


class Investor(Base):
    __tablename__ = "investors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    category: Mapped[str] = mapped_column(String(100), default="")  # ornegin: "Strategic partnerships"
    stage: Mapped[InvestorStage] = mapped_column(
        Enum(InvestorStage), default=InvestorStage.lead
    )
    notes: Mapped[str] = mapped_column(Text, default="")
    documents_pending: Mapped[bool] = mapped_column(default=False)  # "belgeler yuklenecek"

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Investor {self.name} ({self.stage})>"
