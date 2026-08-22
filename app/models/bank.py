"""Not: 'Banka Statemleri - Nordea/Open Banking API -> anlik SEPA odemeleri, Hesap bilgisi
statemleri - Is Bankasi // Kuveyt Turk (Arap Emirates) <- FX oran entegrasyonu'."""
import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class BankProvider(str, enum.Enum):
    nordea = "nordea"            # Nordea / Open Banking API
    isbank = "isbank"            # Is Bankasi
    kuveytturk = "kuveytturk"    # Kuveyt Turk (Arap Emirates FX)


class BankAccount(Base):
    __tablename__ = "bank_accounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    provider: Mapped[BankProvider] = mapped_column(Enum(BankProvider))
    iban: Mapped[str] = mapped_column(String(64), unique=True)
    currency: Mapped[str] = mapped_column(String(8), default="EUR")
    label: Mapped[str] = mapped_column(String(255), default="")

    transactions: Mapped[list["BankTransaction"]] = relationship(
        back_populates="account", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"<BankAccount {self.provider}:{self.iban}>"


class BankTransaction(Base):
    __tablename__ = "bank_transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("bank_accounts.id"))
    account: Mapped["BankAccount"] = relationship(back_populates="transactions")

    external_ref: Mapped[str] = mapped_column(String(128), default="")  # SEPA/banka islem referansi
    amount: Mapped[float] = mapped_column(Numeric(14, 2))
    currency: Mapped[str] = mapped_column(String(8), default="EUR")
    fx_rate: Mapped[float | None] = mapped_column(Numeric(14, 6), nullable=True)  # FX oran entegrasyonu
    description: Mapped[str] = mapped_column(Text, default="")
    booked_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:  # pragma: no cover
        return f"<BankTransaction {self.amount} {self.currency}>"
