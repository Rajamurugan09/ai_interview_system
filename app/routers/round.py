from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.round import Round1Submission
from app.services.round1_service import evaluate_round1

router = APIRouter(prefix="/rounds", tags=["Rounds"])


@router.post("/submit-round1")
def submit_round1(data: Round1Submission, db: Session = Depends(get_db)):
    return evaluate_round1(data, db)
