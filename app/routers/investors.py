from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db
from app.models.investor import Investor

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
