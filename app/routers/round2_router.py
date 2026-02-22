from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.llm_service import call_llm
from app.database.session import get_db
from app.services.round2_service import (
    generate_round2_questions,
    evaluate_round2
)
from app.schemas.round2_schema import Round2EvaluationRequest
router = APIRouter()


@router.post("/generate")
def generate_questions(skill: str):
    return {"questions": generate_round2_questions(skill)}


@router.post("/evaluate")
def evaluate(data: Round2EvaluationRequest, db: Session = Depends(get_db)):
    return evaluate_round2(
        round_id=data.round_id,
        answers=[item.dict() for item in data.answers],
        db=db
    )

@router.get("/test-llm")
def test_llm():
    return {"msg": call_llm("Say hello")}

