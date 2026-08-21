"""Not: 'Admin Panel sistemine bankalari ekledigimiz bir panel yonetim sistemi
olusturuyoruz. CSV/Excel export, muhasebe API entegrasyonu'."""
from __future__ import annotations

import csv
import io

import httpx
from openpyxl import Workbook
from sqlalchemy.orm import Session

from app.config import get_settings
from app.models.bank import BankTransaction


def _transactions_rows(db: Session) -> list[dict]:
    transactions = db.query(BankTransaction).all()
    return [
        {
            "id": tx.id,
            "account_id": tx.account_id,
            "external_ref": tx.external_ref,
            "amount": float(tx.amount),
            "currency": tx.currency,
            "fx_rate": float(tx.fx_rate) if tx.fx_rate is not None else "",
            "description": tx.description,
            "booked_at": tx.booked_at.isoformat(),
        }
        for tx in transactions
    ]


def export_transactions_csv(db: Session) -> io.StringIO:
    rows = _transactions_rows(db)
    buffer = io.StringIO()
    fieldnames = list(rows[0].keys()) if rows else [
        "id", "account_id", "external_ref", "amount", "currency", "fx_rate",
        "description", "booked_at",
    ]
    writer = csv.DictWriter(buffer, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
    buffer.seek(0)
    return buffer


def export_transactions_excel(db: Session) -> io.BytesIO:
    rows = _transactions_rows(db)
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Transactions"

    fieldnames = list(rows[0].keys()) if rows else [
        "id", "account_id", "external_ref", "amount", "currency", "fx_rate",
        "description", "booked_at",
    ]
    sheet.append(fieldnames)
    for row in rows:
        sheet.append([row.get(field, "") for field in fieldnames])

    buffer = io.BytesIO()
    workbook.save(buffer)
    buffer.seek(0)
    return buffer


def push_to_accounting_api(db: Session) -> dict:
    """Muhasebe API entegrasyonu: islemleri harici muhasebe sistemine gonderir.

    ACCOUNTING_API_URL / ACCOUNTING_API_KEY tanimli degilse gercek cagri
    yapilmaz, sadece kac kaydin gonderilecegi doner (dry-run).
    """
    settings = get_settings()
    rows = _transactions_rows(db)

    if not settings.accounting_api_url:
        return {"status": "dry-run", "would_send": len(rows)}

    with httpx.Client(timeout=15) as client:
        response = client.post(
            settings.accounting_api_url,
            json={"transactions": rows},
            headers={"Authorization": f"Bearer {settings.accounting_api_key}"},
        )
        response.raise_for_status()
        return {"status": "sent", "count": len(rows), "response": response.json()}
