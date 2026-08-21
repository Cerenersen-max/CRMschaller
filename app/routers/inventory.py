from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db
from app.models.inventory import InventoryItem

router = APIRouter(prefix="/inventory", tags=["inventory"])


@router.get("", response_model=list[schemas.InventoryItemOut])
def list_items(db: Session = Depends(get_db)):
    return db.query(InventoryItem).all()


@router.post("", response_model=schemas.InventoryItemOut, status_code=201)
def create_item(payload: schemas.InventoryItemCreate, db: Session = Depends(get_db)):
    if db.query(InventoryItem).filter_by(sku=payload.sku).first():
        raise HTTPException(status_code=409, detail="SKU already exists")
    item = InventoryItem(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.get("/{item_id}", response_model=schemas.InventoryItemOut)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.get(InventoryItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
