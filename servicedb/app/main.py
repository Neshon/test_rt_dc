from fastapi import FastAPI
from fastapi import Depends
from .database import engine, SessionLocal
from sqlalchemy.orm import Session

from . import models, crud, schemas

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "hello world"}


@app.post('/appeal/', response_model=schemas.AppealBase)
def appeal(appeal: schemas.AppealBase, db: Session = Depends(get_db)):
    return crud.create_appeal(db, appeal)


@app.get('/appeal/')
def appeal(db: Session = Depends(get_db)):
    return crud.get_appeal(db)
