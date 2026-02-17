from fastapi import FastAPI
from app.database.session import engine
from app.database.base import Base

# Import models here
from app.models import candidate, interview

app = FastAPI(
    title="AI Interview System",
    version="1.0.0"
)


# Create tables automatically
Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "AI Interview System Backend Running"}
