from fastapi import FastAPI,Depends,HTTPException
import models
from database import engine,SeccisonLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel,Field
from typing import Optional,List



app=FastAPI()

models.base.metadata.create_all(bind=engine)


def get_db():
    try:
        db=SeccisonLocal()
        yield db
    finally:
        db.close()

class Todo(BaseModel):
    title:str
    description:Optional[str]
    priority:int= Field(gt=0,lt=6,description='must be bettween 1 to 5')
    complete:bool
   
    

@app.get("/")
def read_all(db:Session=Depends(get_db)):
    return db.query(models.Todo).all()

@app.get("/todo/{id}")
def read_one(id:int,db:Session=Depends(get_db)):
    todo_model= db.query(models.Todo).filter(models.Todo.id==id).first()
    if todo_model is not None:
        return todo_model
    else:
        raise http_exception()

@app.post('/')
def create_todo(todo:Todo,db:Session=Depends(get_db)):
    db_todo=models.Todo(title=todo.title,description=todo.description,priority=todo.priority,complete=todo.complete)
    db.add(db_todo)
    db.commit()
    return {'status_code':201,'transection':'sucesfull'}

def http_exception():
    return HTTPException(status_code=404,detail="Todo not found")