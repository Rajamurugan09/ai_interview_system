from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.interview import Interview
from app.schemas.interview import InterviewCreate, InterviewResponse
from app.services.round1_service import create_round1

router = APIRouter(prefix="/interviews", tags=["Interviews"])


@router.post("/")
def create_interview(interview: InterviewCreate, db: Session = Depends(get_db)):

    db_interview = Interview(candidate_id=interview.candidate_id)
    db.add(db_interview)
    db.commit()
    db.refresh(db_interview)

    # Automatically create Round 1
    round1, questions = create_round1(db_interview.id, db)

    return {
        "interview_id": db_interview.id,
        "round1_id": round1.id,
        "round1_status": round1.status,
        "questions": questions
    }



@router.get("/", response_model=list[InterviewResponse])
def list_interviews(db: Session = Depends(get_db)):
    return db.query(Interview).all()
