from sqlalchemy.orm import Session
from app.models.round import Round
from app.models.interview import Interview
from app.models.answer import Answer
from app.services.llm_service import call_llm
import json
import re

AI_PASS_MARK = 65


def _extract_first_json_object(text: str):
    # Extract the first JSON object even if the model adds extra text or fences.
    match = re.search(r"\{[\s\S]*\}", text)
    if not match:
        return None
    try:
        return json.loads(match.group(0))
    except json.JSONDecodeError:
        return None


# 🧠 Agent 1
def generate_round2_questions(skill: str):

    prompt = f"""
    You are a senior technical interviewer.
    Generate 5 advanced {skill} interview questions.
    Only return numbered questions.
    """

    return call_llm(prompt)


# 🧠 Agent 2
def evaluate_round2(round_id: int, answers: list, db: Session):

    round_obj = db.query(Round).filter(
        Round.id == round_id,
        Round.round_number == 2
    ).first()

    if not round_obj:
        return {"error": "Round 2 not found"}

    total_score = 0
    max_score = len(answers) * 10
    evaluation_results = []

    for item in answers:

        prompt = f"""
        You are a strict technical evaluator.

        Question:
        {item["question"]}

        Answer:
        {item["answer"]}

        Return ONLY JSON (no markdown, no extra text):
        {{"score": number, "feedback": "text"}}
        """

        response = call_llm(prompt)

        parsed = _extract_first_json_object(response)
        if isinstance(parsed, dict):
            score = parsed.get("score", 0)
        else:
            score = 0
            parsed = {"score": 0, "feedback": "Invalid format"}

        total_score += score
        evaluation_results.append(parsed)

        answer_record = Answer(
            round_id=round_id,
            question_id=None,
            response=item["answer"]
        )
        db.add(answer_record)

    percentage = (total_score / max_score) * 100

    round_obj.score = percentage
    round_obj.status = "Completed"

    interview = db.query(Interview).filter(
        Interview.id == round_obj.interview_id
    ).first()

    if percentage >= AI_PASS_MARK:
        interview.status = "Round3_Pending"
        result = "Passed - Promoted to Round 3"
    else:
        interview.status = "Rejected"
        interview.final_result = "Failed in Round 2"
        result = "Failed - Rejected"

    db.commit()

    return {
        "round_id": round_id,
        "score": round(percentage, 2),
        "result": result,
        "details": evaluation_results
    }
