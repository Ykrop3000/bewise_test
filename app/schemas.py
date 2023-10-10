import datetime
from typing import Union

from pydantic import BaseModel


class QuestionBase(BaseModel):
    text_question: str
    text_answer: str
    created_at: datetime.datetime


class QuestionCreate(QuestionBase):
    pass

class QuestionCreatePayload(BaseModel):
    question_num: int

class Question(QuestionBase):
    id: int
    class Config:
        orm_mode = True

