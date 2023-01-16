from fastapi import FastAPI,Depends
import models
from database import engine,SeccisonLocal
from sqlalchemy.orm import Session


app=FastAPI()

models.base.metadata.create_all(bind=engine)

# @app.get("/")
def get_db():
    try:
        db=SeccisonLocal()
        yield db
    finally:
        db.close()

@app.get("/")
def read_all(db:Session=Depends(get_db)):
    return db.query(models.Todo).all()