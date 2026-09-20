from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Lead
from ..schemas import FaqItem, QualificationRequest, QualificationResponse
from ..services.recommender import FAQ_ITEMS, PROGRAMS, recommend_program


router = APIRouter(prefix="/api", tags=["Клиентский сервис"])


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "yachtdream-sales-agent"}


@router.get("/programs")
def programs() -> list[dict]:
    return [
        {
            "id": program.id,
            "title": program.title,
            "subtitle": program.subtitle,
            "benefits": list(program.benefits),
        }
        for program in PROGRAMS.values()
    ]


@router.get("/faq", response_model=list[FaqItem])
def faq() -> list[dict]:
    return FAQ_ITEMS


@router.post(
    "/qualify",
    response_model=QualificationResponse,
    status_code=status.HTTP_201_CREATED,
)
def qualify(data: QualificationRequest, db: Session = Depends(get_db)):
    recommendation = recommend_program(data)
    lead = Lead(
        **data.model_dump(),
        recommended_program=recommendation.title,
        recommendation_reason=recommendation.reason,
    )
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return {"lead_id": lead.id, "recommendation": recommendation}

