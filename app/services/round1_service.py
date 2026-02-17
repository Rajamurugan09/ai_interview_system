from sqlalchemy.orm import Session
from app.models.round import Round
from app.models.question import Question


def create_round1(interview_id: int, db: Session):

    # Create Round 1 entry
    round1 = Round(
        interview_id=interview_id,
        round_number=1,
        status="In Progress"
    )

    db.add(round1)
    db.commit()
    db.refresh(round1)

    # Fetch 20 MCQ questions
    questions = db.query(Question).filter(
        Question.round_type == 1
    ).limit(20).all()

    return round1, questions
