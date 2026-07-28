from datetime import UTC, datetime
from enum import StrEnum
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, field_validator


class Source(StrEnum):
    MOBILE = "mobile"
    IOT = "iot"
    SYNTHETIC = "synthetic"


class ConsentStatus(StrEnum):
    NOT_REQUIRED_SYNTHETIC = "not_required_synthetic"
    OBTAINED = "obtained"


class SyncStatus(StrEnum):
    LOCAL = "local"
    QUEUED = "queued"
    SYNCHRONIZED = "synchronized"


class ObservationBase(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    observation_id: UUID = Field(default_factory=uuid4)
    timestamp_utc: datetime = Field(default_factory=lambda: datetime.now(UTC))
    site_code: str = Field(pattern=r"^[A-Z0-9][A-Z0-9-]{2,31}$")
    temperature_c: float = Field(ge=-30, le=65)
    relative_humidity_pct: float = Field(ge=0, le=100)
    soil_moisture_pct: float = Field(ge=0, le=100)
    crop_stage: str = Field(min_length=1, max_length=50)
    crop_type: str | None = Field(default=None, max_length=80)
    observation_source: Source
    consent_status: ConsentStatus
    synchronization_status: SyncStatus
    approximate_region: str | None = Field(default=None, max_length=80)
    notes: str | None = Field(default=None, max_length=280)

    @field_validator("timestamp_utc")
    @classmethod
    def require_timezone(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("timestamp_utc must include a UTC offset")
        return value.astimezone(UTC)

    @field_validator("notes")
    @classmethod
    def reject_personal_notes(cls, value: str | None) -> str | None:
        if value and any(token in value.lower() for token in ("phone", "address", "child name")):
            raise ValueError("notes must be non-personal")
        return value


class ObservationCreate(ObservationBase):
    pass


class ObservationRead(ObservationBase):
    created_at: datetime


class RiskAssessment(BaseModel):
    heat_stress_risk: str
    water_stress_risk: str
    humidity_disease_risk: str
    combined_risk_level: str
    risk_score: int = Field(ge=0, le=100)
    reasons: list[str]
    suggested_next_checks: list[str]
    disclaimer: str
