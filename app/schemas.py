"""Pydantic siniflari - API giris/cikis semalari (tum modeller tek dosyada, kapsam kucuk)."""
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.bank import BankProvider
from app.models.inventory import InventoryClassification
from app.models.investor import InvestorStage
from app.models.logistics import LogisticsFileStatus


# ---- Investor ----
class InvestorBase(BaseModel):
    name: str
    category: str = ""
    stage: InvestorStage = InvestorStage.lead
    notes: str = ""
    documents_pending: bool = False


class InvestorCreate(InvestorBase):
    pass


class InvestorOut(InvestorBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


# ---- Inventory ----
class InventoryItemBase(BaseModel):
    sku: str
    name: str
    classification: InventoryClassification = InventoryClassification.sia
    quantity: int = 0
    unit_cost: float = 0
    supplier_contract_ref: str = ""
    dock_location: str = ""
    notes: str = ""


class InventoryItemCreate(InventoryItemBase):
    pass


class InventoryItemOut(InventoryItemBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


# ---- Logistics ----
class LogisticsFileBase(BaseModel):
    title: str
    status: LogisticsFileStatus = LogisticsFileStatus.created
    bank_contacts: str = ""
    notes: str = ""


class LogisticsFileCreate(LogisticsFileBase):
    pass


class LogisticsFileOut(LogisticsFileBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    updated_at: datetime


# ---- Bank ----
class BankAccountBase(BaseModel):
    provider: BankProvider
    iban: str
    currency: str = "EUR"
    label: str = ""


class BankAccountCreate(BankAccountBase):
    pass


class BankAccountOut(BankAccountBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class BankTransactionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    account_id: int
    external_ref: str
    amount: float
    currency: str
    fx_rate: float | None
    description: str
    booked_at: datetime
