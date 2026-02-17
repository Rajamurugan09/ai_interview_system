from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from app.database.base import Base


class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True)
    round_id = Column(Integer, ForeignKey("rounds.id"))
    question_id = Column(Integer, ForeignKey("questions.id"))
    response = Column(String, nullable=False)

    round = relationship("Round")
    question = relationship("Question")
