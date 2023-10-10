import datetime

from fastapi import Depends, FastAPI, HTTPException, Response
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.database import SessionLocal, engine
from app.services import fetch_random_question

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/question/", response_model=schemas.Question)
async def create_question(payload: schemas.QuestionCreatePayload, db: Session = Depends(get_db)):
    candidates = await fetch_random_question(payload.question_num)

    while True:
        exist_questions = crud.get_questions_by_text(db, texts=[candidate.get('question') for candidate in candidates])
        exist_questions_count = exist_questions.count()
        if exist_questions_count == 0:
            break
        new_candidates = await fetch_random_question(exist_questions_count)
        for new_candidate in new_candidates:
            for candidate_id, candidate in enumerate(candidates):
                if candidate.get('question') in [j.text_questionq for j in exist_questions]:
                    candidates[candidate_id] = new_candidate

    questions = []
    for candidate in candidates:
        questions.append(schemas.QuestionCreate(
            text_question=candidate.get('question', ''),
            text_answer=candidate.get('answer', ''),
            created_at=datetime.datetime.strptime(candidate.get('created_at'), "%Y-%m-%dT%H:%M:%S.%fZ"),
        ))
    db_questions = crud.create_questions(db, questions=questions)

    return db_questions[-1]


@app.get("/questions/", response_model=list[schemas.Question])
def read_questions(db: Session = Depends(get_db)):
    users = crud.get_questions(db)
    return users


@app.get("/question/{question_id}", response_model=schemas.Question)
def read_question(question_id: int, db: Session = Depends(get_db)):
    db_question = crud.get_question(db, question_id=question_id)
    if db_question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return db_question

@app.delete("/question/{question_id}", response_model=schemas.Question)
def delete_question(question_id: int, db: Session = Depends(get_db)):
    db_question = crud.get_question(db, question_id=question_id)
    if db_question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    crud.delete_question(db, question_id=question_id)
    return db_question