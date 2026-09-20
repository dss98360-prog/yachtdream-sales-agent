from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .db import Base


class Lead(Base):
    __tablename__ = "leads"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(254))
    phone: Mapped[str] = mapped_column(String(30))
    experience: Mapped[str] = mapped_column(String(30))
    goal: Mapped[str] = mapped_column(String(40))
    destination: Mapped[str] = mapped_column(String(40))
    season: Mapped[str] = mapped_column(String(30))
    group_type: Mapped[str] = mapped_column(String(30))
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    recommended_program: Mapped[str] = mapped_column(String(120))
    recommendation_reason: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(30), default="new")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

