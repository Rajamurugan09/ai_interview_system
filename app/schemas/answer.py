from pydantic import BaseModel

class AnswerCreate(BaseModel):
    question_id: int
    response: str