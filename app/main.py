from fastapi import FastAPI
from app.database.session import engine
from app.database.base import Base

app = FastAPI(
    title="AI Interview System",
    version="1.0.0"
)


@app.get("/")
def root():
    return {"message": "AI Interview System Backend Running"}
