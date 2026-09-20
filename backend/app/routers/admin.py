from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Lead
from ..schemas import LeadRead, LeadStatusUpdate
from ..security import require_admin_key


router = APIRouter(
    prefix="/api/admin",
    tags=["Администрирование"],
    dependencies=[Depends(require_admin_key)],
)


@router.get("/leads")
def list_leads(
    status: str | None = Query(default=None, max_length=30),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    filters = [Lead.status == status] if status else []
    total = db.scalar(select(func.count(Lead.id)).where(*filters)) or 0
    items = db.scalars(
        select(Lead)
        .where(*filters)
        .order_by(Lead.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    ).all()
    return {
        "items": [LeadRead.model_validate(item) for item in items],
        "total": total,
        "page": page,
        "page_size": page_size,
    }


@router.patch("/leads/{lead_id}", response_model=LeadRead)
def update_lead_status(
    lead_id: int,
    payload: LeadStatusUpdate,
    db: Session = Depends(get_db),
):
    lead = db.get(Lead, lead_id)
    if lead is None:
        raise HTTPException(status_code=404, detail="Заявка не найдена")
    lead.status = payload.status
    db.commit()
    db.refresh(lead)
    return lead

