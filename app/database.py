"""SQLAlchemy engine / session kurulumu."""
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.config import get_settings

settings = get_settings()

is_sqlite = settings.database_url.startswith("sqlite")
is_sqlite_memory = is_sqlite and ":memory:" in settings.database_url
connect_args = {"check_same_thread": False} if is_sqlite else {}
# :memory:'de her baglanti ayri bir bos veritabani acar; testlerde tek bir
# paylasilan baglanti kullanmak icin StaticPool gerekir.
engine = create_engine(
    settings.database_url,
    connect_args=connect_args,
    poolclass=StaticPool if is_sqlite_memory else None,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Tum modelleri import edip tablolari olusturur (gelistirme icin; prod'da Alembic onerilir)."""
    from app.models import bank, integration_log, inventory, investor, logistics, meeting  # noqa: F401

    Base.metadata.create_all(bind=engine)
