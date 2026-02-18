from app.models.answer import Answer
from app.models.question import Question
from app.models.round import Round
from app.models.interview import Interview
from sqlalchemy.orm import Session

PASS_MARK = 60  # 60% to pass


# ✅ CREATE ROUND 1  (THIS WAS MISSING — FIXED)
def create_round1(interview_id: int, db: Session):

    interview = db.query(Interview).filter(
        Interview.id == interview_id
    ).first()

    if not interview:
        return {"error": "Interview not found"}

    round_obj = Round(
        interview_id=interview_id,
        round_number=1,
        status="InProgress"
    )

    db.add(round_obj)

    interview.status = "Round1_InProgress"

    db.commit()
    db.refresh(round_obj)

    return {
        "message": "Round 1 created successfully",
        "round_id": round_obj.id
    }


# ✅ EVALUATE ROUND 1
# ✅ EVALUATE ROUND 1 (Corrected for 20 Questions)
def evaluate_round1(data, db: Session):

    round_obj = db.query(Round).filter(
        Round.id == data.round_id
    ).first()

    if not round_obj:
        return {"error": "Round not found"}

    # Get total Round 1 questions (assuming round_type = 1)
    total_questions = db.query(Question).filter(
        Question.round_type == 1
    ).count()

    correct_count = 0

    for ans in data.answers:

        question = db.query(Question).filter(
            Question.id == ans.question_id,
            Question.round_type == 1
        ).first()

        if not question:
            continue

        # Save answer
        answer_record = Answer(
            round_id=data.round_id,
            question_id=ans.question_id,
            response=ans.response
        )
        db.add(answer_record)

        if question.correct_answer.strip().lower() == ans.response.strip().lower():
            correct_count += 1

    # Calculate score based on TOTAL 20 questions
    score_percentage = (correct_count / total_questions) * 100

    round_obj.score = score_percentage
    round_obj.status = "Completed"

    interview = db.query(Interview).filter(
        Interview.id == round_obj.interview_id
    ).first()

    if score_percentage >= PASS_MARK:
        interview.status = "Round2_Pending"
        result = "Passed - Promoted to Round 2"
    else:
        interview.status = "Rejected"
        interview.final_result = "Failed in Round 1"
        result = "Failed - Rejected"

    db.commit()

    return {
        "round_id": round_obj.id,
        "total_questions": total_questions,
        "correct_answers": correct_count,
        "score": round(score_percentage, 2),
        "result": result
    }
