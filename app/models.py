from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    text_question = Column(String, unique=True, index=True)
    text_answer = Column(String, index=True)

    created_at = Column(DateTime)
