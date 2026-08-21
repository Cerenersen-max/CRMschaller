from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db
from app.models.bank import BankAccount, BankTransaction
from app.services.bank_integration import fetch_fx_rates, get_bank_client

router = APIRouter(prefix="/banks", tags=["banks"])


@router.get("/accounts", response_model=list[schemas.BankAccountOut])
def list_accounts(db: Session = Depends(get_db)):
    return db.query(BankAccount).all()


@router.post("/accounts", response_model=schemas.BankAccountOut, status_code=201)
def create_account(payload: schemas.BankAccountCreate, db: Session = Depends(get_db)):
    if db.query(BankAccount).filter_by(iban=payload.iban).first():
        raise HTTPException(status_code=409, detail="IBAN already exists")
    account = BankAccount(**payload.model_dump())
    db.add(account)
    db.commit()
    db.refresh(account)
    return account


@router.post("/accounts/{account_id}/sync", response_model=list[schemas.BankTransactionOut])
def sync_statement(account_id: int, db: Session = Depends(get_db)):
    """Ilgili bankanin API'sinden ekstre satirlarini cekip veritabanina isler."""
    account = db.get(BankAccount, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    client = get_bank_client(account.provider.value)
    lines = client.fetch_statement(account.iban)

    created: list[BankTransaction] = []
    for line in lines:
        exists = (
            db.query(BankTransaction)
            .filter_by(account_id=account.id, external_ref=line.external_ref)
            .first()
        )
        if exists:
            continue
        tx = BankTransaction(
            account_id=account.id,
            external_ref=line.external_ref,
            amount=line.amount,
            currency=line.currency,
            fx_rate=line.fx_rate,
            description=line.description,
            booked_at=line.booked_at,
        )
        db.add(tx)
        created.append(tx)

    db.commit()
    for tx in created:
        db.refresh(tx)
    return created


@router.get("/fx-rates")
def get_fx_rates(base: str = "EUR"):
    return fetch_fx_rates(base_currency=base)
