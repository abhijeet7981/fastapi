from sqlalchemy import Column,Boolean,Integer,String,ForeignKey
from sqlalchemy.orm import relationship
from database import base


class Users(base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True,index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    hashed_password = Column(String(100))
    first_name=Column(String)
    last_name=Column(String)
    is_active = Column(Boolean,default=True)

    todos=relationship('Todo',back_populates='owner')

class Todo(base):
    __tablename__ = 'todos'


    id = Column(Integer, primary_key=True,index=True)
    title = Column(String(255))
    description = Column(String(255))
    priority=Column(Integer)
    complete = Column(Boolean,default=False)
    owner_id=Column(Integer,ForeignKey('users.id'))
    owner=relationship('Users',back_populates='todos')






