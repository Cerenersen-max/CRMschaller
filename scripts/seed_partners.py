"""El yazisi defter sayfalarindaki tum ortak/yatirimci ve toplanti notlarini
tek seferde veritabanina isler ('kodlari ust kodlarla birlestir' -> onceki
oturumda islenen KWORKS/Turk Telekom Ventures/Sabanci/Techstars notlari ile bu
oturumda eklenen Aston Martin ortakligi ve GUCA haftalik toplantisi burada
birlesir).

Kullanim:
    python -m scripts.seed_partners
"""
from __future__ import annotations

from datetime import datetime

from app.database import SessionLocal, init_db
from app.models.investor import Investor, InvestorStage
from app.models.meeting import MeetingCadence, PartnerMeeting

# Not: 'KWORKS (Stratejik ortakliklar)', 'Turk Telekom Ventures (Emin degilim
# ama bulut sistem destegi veri tabani sunumuna odaklanma)', 'Sabanci (Yatirimci
# sunumu genel degerlendirme)', 'PARTNER - Ore Chase - Techstars sureci yapildi
# fizda inceleme ile devam edecek, dosyalar yuklenecek'.
NOTEBOOK_PARTNERS = [
    dict(
        name="KWORKS",
        category="Stratejik ortakliklar",
        stage=InvestorStage.lead,
    ),
    dict(
        name="Turk Telekom Ventures",
        category="Bulut sistem destegi / veri tabani sunumu",
        stage=InvestorStage.due_diligence,
        notes="Emin degilim ama bulut sistem destegi veri tabani sunumuna odaklanma.",
    ),
    dict(
        name="Sabanci",
        category="Yatirimci sunumu genel degerlendirme",
        stage=InvestorStage.due_diligence,
    ),
    dict(
        name="Ore Chase",
        category="Partner",
        stage=InvestorStage.due_diligence,
        notes="Techstars sureci yapildi, fizda inceleme ile devam edecek.",
        documents_pending=True,
    ),
    # Not: 'Outlook/Partnership ... lifestyle collaboration - Partner (Toronto
    # Operations) x Aston Martin, nathan.hoyt@astonmartin.com'.
    dict(
        name="Aston Martin",
        category="Lifestyle collaboration",
        stage=InvestorStage.lead,
        notes="Toronto Operations uzerinden ilk temas (Thu 16 Jul '26).",
        contact_name="Nathan Hoyt",
        contact_email="nathan.hoyt@astonmartin.com",
    ),
]

# Not: 'GUCA: Pazartesi- 24.Agustos.26 | 10:00 - haftalik ... veri tabani
# mimarisinin ilerleyerek tam yaklasimi gerceklestir. website Design gelistirme
# odna 11:00. AI website Generator uygulamasi incelyelim 20 dk.'
NOTEBOOK_MEETINGS = [
    dict(
        title="GUCA",
        cadence=MeetingCadence.weekly,
        day_of_week="Pazartesi",
        time_of_day="10:00",
        agenda=(
            "10:00 - Veri tabani mimarisinin ilerleyen adimlarini tam "
            "yaklasimla gozden gecir.\n"
            "11:00 - Website design gelistirme.\n"
            "+20 dk - AI website generator uygulamasini inceleyelim."
        ),
        next_run_at=datetime(2026, 8, 24, 10, 0),
    ),
]


def seed() -> None:
    init_db()
    db = SessionLocal()
    try:
        for data in NOTEBOOK_PARTNERS:
            exists = db.query(Investor).filter_by(name=data["name"]).first()
            if not exists:
                db.add(Investor(**data))

        for data in NOTEBOOK_MEETINGS:
            exists = db.query(PartnerMeeting).filter_by(title=data["title"]).first()
            if not exists:
                db.add(PartnerMeeting(**data))

        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    seed()
    print("Defter notlarindaki ortaklar ve toplantilar veritabanina islendi.")
