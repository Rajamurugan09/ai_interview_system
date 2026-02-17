from pydantic import BaseModel
from datetime import datetime


class CandidateCreate(BaseModel):
    full_name: str
    email: str
    phone: str | None = None


class CandidateResponse(BaseModel):
    id: int
    full_name: str
    email: str
    phone: str | None
    created_at: datetime

    class Config:
        from_attributes = True
