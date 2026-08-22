"""Not: 'Enveter Sablonu -> SPOFF analizi, SIA|RPO|ETO -> Veri modeli/Sozlesme API, Dock,
Faz-1 -> Notlarda guncellestir eklenti olustur'.

SIA/RPO/ETO uretim/tedarik siniflandirmasi: Stocked, Assembled-to-order /
Repeat-Purchase-Order / Engineer/Purchase-to-order gibi envanter tipleri icin alan tutuyoruz.
"""
import enum

from sqlalchemy import Enum, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class InventoryClassification(str, enum.Enum):
    sia = "SIA"   # Stok / hazir urun
    rpo = "RPO"   # Tekrar siparis
    eto = "ETO"   # Siparise ozel muhendislik/uretim


class InventoryItem(Base):
    __tablename__ = "inventory_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    sku: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    classification: Mapped[InventoryClassification] = mapped_column(
        Enum(InventoryClassification), default=InventoryClassification.sia
    )
    quantity: Mapped[int] = mapped_column(Integer, default=0)
    unit_cost: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    supplier_contract_ref: Mapped[str] = mapped_column(String(255), default="")  # "sozlesme API" referansi
    dock_location: Mapped[str] = mapped_column(String(100), default="")  # "Dock" notu
    notes: Mapped[str] = mapped_column(Text, default="")

    def __repr__(self) -> str:  # pragma: no cover
        return f"<InventoryItem {self.sku} qty={self.quantity}>"
