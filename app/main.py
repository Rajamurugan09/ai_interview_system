from fastapi import FastAPI
from app.database.session import engine
from app.database.base import Base

from app.models import candidate as candidate_model
from app.models import interview as interview_model
from app.models import round as round_model
from app.models import question as question_model
from app.models import answer as answer_model
from app.routers import round
from app.routers import candidate, interview
from app.routers import round2_router
app = FastAPI(
    title="AI Interview System",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)

app.include_router(candidate.router)
app.include_router(interview.router)
app.include_router(round.router)
app.include_router(round2_router.router, prefix="/round2", tags=["Round 2"])

@app.get("/")
def root():
    return {"message": "AI Interview System Backend Running"}



