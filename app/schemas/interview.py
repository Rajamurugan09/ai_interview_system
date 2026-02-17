from pydantic import BaseModel
from datetime import datetime


class InterviewCreate(BaseModel):
    candidate_id: int


class InterviewResponse(BaseModel):
    id: int
    candidate_id: int
    status: str
    final_result: str | None
    created_at: datetime

    class Config:
        from_attributes = True
