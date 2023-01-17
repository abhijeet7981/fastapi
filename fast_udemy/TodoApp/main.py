from fastapi import FastAPI,Depends,HTTPException
import models
from database import engine,SeccisonLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel,Field
from typing import Optional,List
from auth import get_current_user,get_user_exceptions



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

@app.get('/todos/user')
def read_all_by_user(user:dict=Depends(get_current_user),db:Session=Depends(get_db)):
    if user is None:
        raise get_user_exceptions()
    return db.query(models.Todo).filter(models.Todo.owner_id==user.get('id')).all()


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

@app.put('/{id}')
def update_todo(id:int,todo:Todo,db:Session=Depends(get_db)):
    db_todo=db.query(models.Todo).filter(models.Todo.id==id).first()
    if db_todo is not None:
        db_todo.title=todo.title
        db_todo.description=todo.description
        db_todo.priority=todo.priority
        db_todo.complete=todo.complete
        db.add(db_todo)
        db.commit()
        return sucessful_responce(200)
    else:
        raise http_exception()


@app.delete('/{id}')
def delete_todo(id:int,db:Session=Depends(get_db)):
    db_todo=db.query(models.Todo).filter(models.Todo.id==id).first()
    if db_todo is not None:
        db.delete(db_todo)
        db.commit()
        return {'status_code':200,'transection':'sucesfull'}
    else:
        raise http_exception()


def sucessful_responce(status_code:int):
    return {'status_code':status_code,'transection':'sucesfull'}



    
