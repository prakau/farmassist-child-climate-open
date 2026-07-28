from contextlib import asynccontextmanager
from datetime import timezone
from typing import Any

from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from apps.api.database import ObservationRecord, create_tables, get_session
from apps.api.schemas import ObservationCreate, ObservationRead, RiskAssessment
from packages.risk_engine import assess_risk, get_thresholds


@asynccontextmanager
async def lifespan(_: FastAPI):
    create_tables()
    yield


app = FastAPI(
    title="FarmAssist Child Climate & Nutrition Intelligence API",
    version="0.1.0-alpha",
    description="Early, non-medical environmental-risk reference implementation.",
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def _read(record: ObservationRecord) -> ObservationRead:
    payload = {column.name: getattr(record, column.name) for column in record.__table__.columns}
    return ObservationRead.model_validate(payload)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "version": "0.1.0-alpha"}


@app.post("/v1/observations", response_model=ObservationRead, status_code=status.HTTP_201_CREATED)
def create_observation(
    payload: ObservationCreate, session: Session = Depends(get_session)
) -> ObservationRead:
    values = payload.model_dump()
    values["observation_id"] = str(payload.observation_id)
    record = ObservationRecord(**values)
    session.add(record)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=409, detail="observation_id already exists") from None
    session.refresh(record)
    return _read(record)


@app.get("/v1/observations", response_model=list[ObservationRead])
def list_observations(
    site_code: str | None = None,
    limit: int = Query(100, ge=1, le=500),
    session: Session = Depends(get_session),
) -> list[ObservationRead]:
    query = select(ObservationRecord).order_by(ObservationRecord.timestamp_utc.desc()).limit(limit)
    if site_code:
        query = query.where(ObservationRecord.site_code == site_code)
    return [_read(record) for record in session.scalars(query)]


@app.post("/v1/risk/assess", response_model=RiskAssessment)
def risk_assessment(payload: ObservationCreate) -> RiskAssessment:
    return assess_risk(payload)


@app.get("/v1/sites/{site_code}/summary")
def site_summary(site_code: str, session: Session = Depends(get_session)) -> dict[str, Any]:
    records = list(
        session.scalars(
            select(ObservationRecord)
            .where(ObservationRecord.site_code == site_code)
            .order_by(ObservationRecord.timestamp_utc.desc())
        )
    )
    if not records:
        raise HTTPException(status_code=404, detail="site not found")
    latest = records[0]
    return {
        "site_code": site_code,
        "observation_count": len(records),
        "latest_observation": _read(latest),
        "latest_risk": assess_risk(_read(latest)),
    }


@app.get("/v1/public/indicators")
def public_indicators(session: Session = Depends(get_session)) -> dict[str, Any]:
    count, sites, first, last = session.execute(
        select(
            func.count(ObservationRecord.observation_id),
            func.count(func.distinct(ObservationRecord.site_code)),
            func.min(ObservationRecord.timestamp_utc),
            func.max(ObservationRecord.timestamp_utc),
        )
    ).one()
    # Intentionally no rows, notes, coordinates, crop types, or small-group breakdowns.
    return {
        "valid_environmental_observations": count,
        "active_non_identifying_sites": sites,
        "period_start_utc": first.replace(tzinfo=timezone.utc) if first else None,
        "period_end_utc": last.replace(tzinfo=timezone.utc) if last else None,
        "privacy": "Aggregate environmental indicators only; no personal or child data.",
    }


@app.get("/v1/config/risk-thresholds")
def risk_thresholds() -> dict[str, Any]:
    return get_thresholds()
