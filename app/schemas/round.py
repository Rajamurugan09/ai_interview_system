from pydantic import BaseModel
from typing import List
from app.schemas.answer import AnswerCreate


class Round1Submission(BaseModel):
    round_id: int
    answers: List[AnswerCreate]
