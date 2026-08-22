"""Not: 'Admin Panel sistemine bankalari ekledigimiz bir panel yonetim sistemi
olusturuyoruz.' Bu router banka/muhasebe yonetimi icin admin panel API'sidir."""
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.accounting_export import (
    export_transactions_csv,
    export_transactions_excel,
    push_to_accounting_api,
)

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/export/transactions.csv")
def export_csv(db: Session = Depends(get_db)):
    buffer = export_transactions_csv(db)
    return StreamingResponse(
        iter([buffer.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=transactions.csv"},
    )


@router.get("/export/transactions.xlsx")
def export_excel(db: Session = Depends(get_db)):
    buffer = export_transactions_excel(db)
    return StreamingResponse(
        iter([buffer.getvalue()]),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=transactions.xlsx"},
    )


@router.post("/export/accounting-sync")
def sync_to_accounting(db: Session = Depends(get_db)):
    return push_to_accounting_api(db)
