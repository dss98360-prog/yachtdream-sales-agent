from datetime import datetime
from typing import Literal

from pydantic import BaseModel, EmailStr, Field, field_validator


Experience = Literal["none", "beginner", "experienced"]
Goal = Literal["captain", "cruise", "skills", "family"]
Destination = Literal["turkey", "thailand", "any"]
Season = Literal["spring", "summer", "autumn", "winter", "flexible"]
GroupType = Literal["solo", "couple", "family", "friends"]
LeadStatus = Literal["new", "contacted", "qualified", "closed"]


class QualificationRequest(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    phone: str = Field(min_length=7, max_length=30)
    experience: Experience
    goal: Goal
    destination: Destination
    season: Season
    group_type: GroupType
    comment: str | None = Field(default=None, max_length=1000)

    @field_validator("name", "phone", "comment", mode="before")
    @classmethod
    def strip_text(cls, value):
        return value.strip() if isinstance(value, str) else value

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: str) -> str:
        digits = "".join(char for char in value if char.isdigit())
        if len(digits) < 7:
            raise ValueError("Укажите корректный номер телефона")
        return value


class Recommendation(BaseModel):
    program_id: str
    title: str
    subtitle: str
    reason: str
    benefits: list[str]
    next_step: str


class QualificationResponse(BaseModel):
    lead_id: int
    recommendation: Recommendation


class LeadRead(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    experience: str
    goal: str
    destination: str
    season: str
    group_type: str
    comment: str | None
    recommended_program: str
    recommendation_reason: str
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}


class LeadStatusUpdate(BaseModel):
    status: LeadStatus


class FaqItem(BaseModel):
    question: str
    answer: str

