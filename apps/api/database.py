import os
from collections.abc import Generator
from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./farmassist.db")
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class ObservationRecord(Base):
    __tablename__ = "observations"

    observation_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    timestamp_utc: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    site_code: Mapped[str] = mapped_column(String(32), index=True)
    temperature_c: Mapped[float] = mapped_column(Float)
    relative_humidity_pct: Mapped[float] = mapped_column(Float)
    soil_moisture_pct: Mapped[float] = mapped_column(Float)
    crop_stage: Mapped[str] = mapped_column(String(50))
    crop_type: Mapped[str | None] = mapped_column(String(80))
    observation_source: Mapped[str] = mapped_column(String(20))
    consent_status: Mapped[str] = mapped_column(String(30))
    synchronization_status: Mapped[str] = mapped_column(String(20))
    approximate_region: Mapped[str | None] = mapped_column(String(80))
    notes: Mapped[str | None] = mapped_column(String(280))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )


def create_tables() -> None:
    Base.metadata.create_all(bind=engine)


def get_session() -> Generator[Session, None, None]:
    with SessionLocal() as session:
        yield session
