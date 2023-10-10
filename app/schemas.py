import datetime
from typing import Union

from pydantic import BaseModel, field_validator


class QuestionBase(BaseModel):
    text_question: str
    text_answer: str
    created_at: datetime.datetime


class QuestionCreate(QuestionBase):
    pass

class QuestionCreatePayload(BaseModel):
    question_num: int

    @field_validator('question_num')
    def prevent_zero(cls, v):
        if v == 0:
            raise ValueError('ensure this value is not 0')
        return v

class Question(QuestionBase):
    id: int
    class Config:
        orm_mode = True

