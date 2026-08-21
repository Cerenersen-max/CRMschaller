from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db
from app.models.logistics import LogisticsFile

router = APIRouter(prefix="/logistics", tags=["logistics"])


@router.get("", response_model=list[schemas.LogisticsFileOut])
def list_files(db: Session = Depends(get_db)):
    return db.query(LogisticsFile).all()


@router.post("", response_model=schemas.LogisticsFileOut, status_code=201)
def create_file(payload: schemas.LogisticsFileCreate, db: Session = Depends(get_db)):
    logistics_file = LogisticsFile(**payload.model_dump())
    db.add(logistics_file)
    db.commit()
    db.refresh(logistics_file)
    return logistics_file


@router.get("/{file_id}", response_model=schemas.LogisticsFileOut)
def get_file(file_id: int, db: Session = Depends(get_db)):
    logistics_file = db.get(LogisticsFile, file_id)
    if not logistics_file:
        raise HTTPException(status_code=404, detail="Logistics file not found")
    return logistics_file
