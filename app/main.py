from fastapi import FastAPI
from app.database.session import engine
from app.database.base import Base

# Import all models
from app.models import candidate
from app.models import interview
from app.models import round
from app.models import question
from app.models import answer


app = FastAPI(
    title="AI Interview System",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "AI Interview System Backend Running"}
