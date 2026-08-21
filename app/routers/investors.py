from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db
from app.models.investor import Investor
from app.services.email_templates import build_partnership_email

router = APIRouter(prefix="/investors", tags=["investors"])


@router.get("", response_model=list[schemas.InvestorOut])
def list_investors(db: Session = Depends(get_db)):
    return db.query(Investor).all()


@router.post("", response_model=schemas.InvestorOut, status_code=201)
def create_investor(payload: schemas.InvestorCreate, db: Session = Depends(get_db)):
    investor = Investor(**payload.model_dump())
    db.add(investor)
    db.commit()
    db.refresh(investor)
    return investor


@router.get("/{investor_id}", response_model=schemas.InvestorOut)
def get_investor(investor_id: int, db: Session = Depends(get_db)):
    investor = db.get(Investor, investor_id)
    if not investor:
        raise HTTPException(status_code=404, detail="Investor not found")
    return investor


@router.get("/{investor_id}/outreach-email-preview")
def preview_outreach_email(
    investor_id: int, subject: str = "Cenora - Partnership", db: Session = Depends(get_db)
):
    """Not: 'Outlook/Partnership ... lifestyle collaboration' e-posta basligi
    formatinda, secili partner icin gonderilecek e-postanin onizlemesini uretir."""
    investor = db.get(Investor, investor_id)
    if not investor:
        raise HTTPException(status_code=404, detail="Investor not found")
    if not investor.contact_email:
        raise HTTPException(status_code=422, detail="Bu partner icin contact_email tanimli degil")

    message = build_partnership_email(
        to_name=investor.contact_name or investor.name,
        to_email=investor.contact_email,
        subject=subject,
        body_text=(
            f"Merhaba {investor.contact_name or investor.name},\n\n"
            f"Cenora olarak {investor.category or 'is birligi'} firsatini "
            "degerlendirmek isteriz.\n\nSaygilarimizla,\nCenora Partnerships"
        ),
    )
    return {"raw_email": message.as_string()}
