import os

os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")

from app.database import SessionLocal, init_db
from app.models.investor import Investor
from app.models.meeting import PartnerMeeting
from scripts.seed_partners import seed

init_db()


def test_seed_creates_notebook_partners_and_meetings():
    seed()
    seed()  # idempotent olmali, ikinci calistirmada duplike kayit olusturmamali

    db = SessionLocal()
    try:
        names = {investor.name for investor in db.query(Investor).all()}
        assert {"KWORKS", "Turk Telekom Ventures", "Sabanci", "Ore Chase", "Aston Martin"} <= names

        aston_martin = db.query(Investor).filter_by(name="Aston Martin").first()
        assert aston_martin is not None
        # Gizlilik nedeniyle gercek iletisim bilgisi seed script'inde tutulmaz;
        # admin panelden ayrica girilmesi beklenir.
        assert aston_martin.contact_email == ""

        meetings = db.query(PartnerMeeting).filter_by(title="GUCA").all()
        assert len(meetings) == 1
    finally:
        db.close()
