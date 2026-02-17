from sqlalchemy import Column, Integer, String
from app.database.base import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    round_type = Column(Integer)  # 1=MCQ, 2=Technical, 3=HR

    option_a = Column(String, nullable=True)
    option_b = Column(String, nullable=True)
    option_c = Column(String, nullable=True)
    option_d = Column(String, nullable=True)

    correct_answer = Column(String, nullable=True)
