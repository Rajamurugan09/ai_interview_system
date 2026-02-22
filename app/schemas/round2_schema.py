from pydantic import BaseModel
from typing import List


class AnswerItem(BaseModel):
    question: str
    answer: str


class Round2EvaluationRequest(BaseModel):
    round_id: int
    answers: List[AnswerItem]
