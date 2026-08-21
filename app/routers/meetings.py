"""Not: 'GUCA' haftalik toplanti ajandasi icin router."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db
from app.models.meeting import PartnerMeeting

router = APIRouter(prefix="/meetings", tags=["meetings"])


@router.get("", response_model=list[schemas.PartnerMeetingOut])
def list_meetings(db: Session = Depends(get_db)):
    return db.query(PartnerMeeting).all()


@router.post("", response_model=schemas.PartnerMeetingOut, status_code=201)
def create_meeting(payload: schemas.PartnerMeetingCreate, db: Session = Depends(get_db)):
    meeting = PartnerMeeting(**payload.model_dump())
    db.add(meeting)
    db.commit()
    db.refresh(meeting)
    return meeting


@router.get("/{meeting_id}", response_model=schemas.PartnerMeetingOut)
def get_meeting(meeting_id: int, db: Session = Depends(get_db)):
    meeting = db.get(PartnerMeeting, meeting_id)
    if not meeting:
        raise HTTPException(status_code=404, detail="Toplanti bulunamadi")
    return meeting
