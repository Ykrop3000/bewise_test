from typing import List

from sqlalchemy.orm import Session

from app import models, schemas


def get_question(db: Session, question_id: int):
    return db.query(models.Question).get(question_id)


def get_question_by_text(db: Session, text: str):
    return db.query(models.Question).filter(models.Question.text_question == text).first()


def get_questions_by_text(db: Session, texts: List[str]):
    return db.query(models.Question).filter(models.Question.text_question.in_ == texts)


def get_last_question(db: Session):
    return db.query(models.Question).order_by(models.Question.id.desc()).first()


def get_questions(db: Session):
    return db.query(models.Question).all()


def create_question(db: Session, question: schemas.QuestionCreate):
    db_question = models.Question(**question.model_dump())
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question


def create_questions(db: Session, questions: List[schemas.QuestionCreate]):
    db_questions = [models.Question(**question.model_dump()) for question in questions]
    db.add_all(db_questions)
    db.commit()
    return db_questions


def delete_question(db: Session, question_id: int):
    db_questions = db.query(models.Question).filter(models.Question.id == question_id).delete()
    db.commit()
